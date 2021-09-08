# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import subprocess


_log = logging.getLogger(__file__)


FUNCTION_DECLARATION = re.compile(r'[ \t]*(\bextern\b|\bstatic\b)?[ \t]*\w+[ \t]+\w+\([\w \t,]+[,){]$')  # func start, body and end of line is checked
OPTIMIZE = re.compile(r'__attribute__\(\(optimize\("-O(.){0,4}"\)\)\)')  # can contain any optimization
POSSIBLE_OPTIMIZATIONS = ('-O', '-O1', '-O2', '-O3', '-O0', '-O1', '-Os', '-Ofast', '-Og')
ACCEPTED_OPTIMIZATIONS = []


class Function:

    def __init__(self, name, line, file):
        self.name = name
        self.line = line
        self.file = file

    def __str__(self):
        return "{} | Name: {}, Line: {}, File: {}".format(self.__class__.__name__, self.name, self.line, self.file.split('\\')[-1])

    def __repr__(self):
        return '\n' + self.__str__() + '\n'


def set_acc_opts(acc_opts):
    """
    setter function for setting accepted optimizations

    :param acc_opts: accepted optimizations
    :type acc_opts: list
    :return: None
    :rtype: None
    """
    global ACCEPTED_OPTIMIZATIONS
    ACCEPTED_OPTIMIZATIONS = acc_opts


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def gather_files(folder, ext='.c', incl_subfolder=True):
    """
    Returns list with all trace files found in folder

    :param folder: path to search for trace files
    :type folder: str or path
    :param ext: file extension to search for
    :type ext: str
    :param incl_subfolder: if set subfolders are searched as well
    :type incl_subfolder: bool
    :return: all trace files found in given path
    :rtype: list
    """
    _files = []
    for elem in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, elem)) and incl_subfolder:
            _files.extend(gather_files(os.path.join(folder, elem)))
        else:
            if os.path.splitext(elem)[1] == ext:
                _files.append(os.path.join(folder, elem))
    return _files


def clean_line(line):
    """
    deletes all comments, trailing  from c code line

    :param line: code line to delete all comments from
    :type line: str
    :return: line without comments
    :rtype: str
    """
    inline_comment = re.compile(r'(/\*.*\*/)')  # cut out comment strings: /* ... */
    multiline_comment = re.compile(r'[ \t]*\*')  # cut out multiline comment strings:  * ... (only if not followed by slash)
    line_comment = re.compile(r'//')  # cut out comment strings: // ...

    if bool(re.search(inline_comment, line)):
        res = re.search(inline_comment, line)
        line = line[:res.start()] + line[res.end():]

    if bool(re.search(multiline_comment, line)):
        line = line[:re.search(multiline_comment, line).start()]

    if bool(re.search(line_comment, line)):
        line = line[:re.search(line_comment, line).start()]

    return line.lstrip().rstrip()


def has_func_dec(line):
    """
    checks if line has a function declaration

    :param line: line of valid c code
    :type line: str
    :return: True if line has function declaration
    :rtype: bool
    """
    if re.match(r'^[ \t]*#', line):
        return False
    match = re.search(FUNCTION_DECLARATION, line)
    return match is not None and match.group(0) is not None


def has_optimize(line):
    """
    checks if line of code contains any optimization

    :param line:
    :type line: str
    :return: True if line has optimisation
    :rtype: bool
    """
    line = clean_line(line)
    match = re.search(OPTIMIZE, line)
    if match is not None and match.group(0) is not None:
        otype = line.split('"')[1]
        if otype not in POSSIBLE_OPTIMIZATIONS:
            _log.warning(f"Invalid optimization: {otype}")
        if otype not in ACCEPTED_OPTIMIZATIONS:
            return False
        return True
    return False


def extract_func_name(line):
    """
    Extracts function name from line of valid c code

    Note:
        Check before if line contains function declaration!

    :param line: line of valid c code
    :type line: str
    :return: function name
    :rtype: str
    """
    try:
        line = line.lstrip().rstrip()  # remove dust
        name = re.search(r'\(', line)
        return line[:name.start()].split(' ')[-1]  # remove parameter input part
    except Exception as e:
        _log.critical(e)


def load_file(file, ext='.c'):
    """
    load file content into ram

    :param file: full file path of file to load
    :type file: str
    :param ext: extension which must match to file, is not checked if set to None
    :type ext: str
    :return:
    :rtype:
    """
    if ext is not None and not os.path.splitext(file)[-1] == ext:
        return None
    with open(file, 'r', encoding='utf-8', errors='ignore') as src:
        return src.readlines()


def export(funcs, file):
    """
    Exports result to text file

    :param funcs: not optimized functions
    :type funcs: list
    :param file: text file the result is exported to
    :type file: str
    :return: None
    :rtype: None
    """
    with open(file, 'a', encoding='utf-8', errors='ignore') as dest:
        dest.writelines(["{}\n".format(str(elem)) for elem in funcs])
    try:
        subprocess.Popen([str(file)], shell=True)
    except Exception as e:
        _log.critical(e)


def check_file(lines, file):
    """
    checks all lines for functions with missing optimizations

    :param lines:
    :type lines: list
    :param file: file name, just for exporting reasons
    :type file: str
    :return: list with all functions not optimized yet
    :rtype: list
    """
    _found_funcs = []
    for idx, line in enumerate(lines):
        line = clean_line(line)
        if has_func_dec(line):
            if idx > 0:
                if not has_optimize(lines[idx-1]):
                    _found_funcs.append(Function(name=extract_func_name(line), line=idx, file=file))
    return _found_funcs
