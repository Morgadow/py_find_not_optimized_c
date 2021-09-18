# -*- coding: utf-8 -*-

import time
import datetime

from __init__ import __project_name__, __version__
from ui import ui
from utils import *

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal


_accepted_optimizations = []


class Worker(QObject):
    """ for working main work """
    finished = pyqtSignal()
    progress_val = pyqtSignal(int)
    progress_info = pyqtSignal(str)

    def __init__(self, parent):
        super(Worker, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

        self._acc_opts = parent.get_accepted_opts()
        self._src_folder = parent.source_folder
        self._src_file = parent.source_file
        self._result_file = parent.result_file

    def run(self):
        """ runs task and then emits finished signal """
        try:
            self._run(self._acc_opts, self._src_folder, self._src_file, self._result_file)
        except Exception as e:
            self._logger.critical(e)
        finally:
            self.finished.emit()

    def _run(self, acc_opts, src_folder, src_file, result_file):
        """
        auxiliary function for main task to run in another thread

        :return: None
        :rtype: None
        """
        t = time.time()

        # define what optimizations are accepted
        self.progress_info.emit("Analyzing inputs")
        if not len(acc_opts):
            raise RuntimeError("At least one Optimization must be accepted!")
        for elem in acc_opts:
            if elem not in POSSIBLE_OPTIMIZATIONS:
                raise ValueError(f"Invalid optimization: {elem}!")
        if src_folder is not None and (not os.path.exists(src_folder) or not os.path.isdir(src_folder)):
            raise NotADirectoryError(f"Folder {src_folder} not found!")
        if src_file is not None and (not os.path.exists(src_file) or not os.path.isfile(src_file) or not os.path.splitext(src_file)[1] == '.c'):
            raise FileNotFoundError(f"Invalid File: {src_file}")
        if src_file is not None and src_folder is not None:
            raise RuntimeError("Internal failure! Source file and source folder defined!")
        if os.path.exists(result_file):
            raise RuntimeError("Results file already exists!")
        set_acc_opts(acc_opts)
        self.progress_val.emit(2)

        # gather files
        self.progress_info.emit("Gathering files for analysis")
        if src_folder is not None:  # use folder over file
            src_files = gather_files(src_folder, '.c', True)
        else:
            src_files = [src_file]
        self.progress_val.emit(10)

        # check every file for not optimized functions
        found_funcs, step_per_file = [], 85/len(src_files)
        for idx, file in enumerate(src_files):
            self.progress_info.emit("Analyzing file {}: {}".format(idx, file.split('\\')[-1]))
            _lines = load_file(file, '.c')
            found_funcs.extend(check_file(_lines, file))
            self.progress_val.emit(10 + step_per_file*idx)

        # create results file and write header
        self.progress_info.emit("Exporting result to {}".format(result_file.split('\\')[-1]))
        with open(result_file, 'w+', encoding='utf-8', errors='ignore') as dest:
            dest.write('##############################################################\n')
            now = datetime.datetime.now()
            dest.write("Not optimized C Functions --- {}.{}.{} at {}:{}\n\n".format(now.day, now.month, now.year, now.hour, now.minute))
            if src_folder is not None:
                dest.write(f"Searched root folder: '{src_folder}' with {len(src_files)} .c files.\n")
            if src_file is not None:
                dest.write(f"Searched in: '{src_files}'\n")
            dest.write(f"Found {len(found_funcs)} not optimized functions.\n")
            dest.write("Accepted optimizations: {}\n".format(', '.join(["'{}'".format(elem) for elem in acc_opts])))
            dest.write('##############################################################\n\n\n')
        self.progress_val.emit(98)
        export(found_funcs, self._result_file)
        self.progress_val.emit(100)
        self.progress_info.emit(f"Finished after {round(time.time()-t, 3)} seconds")


class FindNonOptimizedCFunctions:
    """
    main class holding gui and al functionality

    Note:
        This line must be added to ui.py __init__() to set correct window size:
        "MainWindow.setFixedSize(330, 194)"
        Also remove settings for minimum and maximum MainWindow size.
    """

    def __init__(self):

        self._logger = logging.getLogger(self.__class__.__name__)

        self.source_file = None
        self.source_folder = None
        self.result_file = None

        self._thread = None
        self._worker = None

        # create app
        self.__app = QtWidgets.QApplication(sys.argv)
        self.__win = QtWidgets.QMainWindow()
        self.__ui = ui.Ui_MainWindow()
        self.__ui.setupUi(self.__win)
        self.__win.show()
        self.__win.setWindowTitle(__project_name__)
        self.__win.setWindowIcon(QtGui.QIcon(resource_path(os.path.join('ui', 'icon.ico'))))

        # menu bar options defining how data is analyzed
        self._opts_menus = [
            self.__ui.actionAccept_Os,
            self.__ui.actionAccept_O0,
            self.__ui.actionAccept_O1,
            self.__ui.actionAccept_O2,
            self.__ui.actionAccept_O3,
            self.__ui.actionAccept_Ofast,
            self.__ui.actionAccept_Og,
        ]
        self._opt_menu_to_str = {
            self.__ui.actionAccept_Os: '-Os',
            self.__ui.actionAccept_O0: '-Os',
            self.__ui.actionAccept_O1: '-O1',
            self.__ui.actionAccept_O2: '-O2',
            self.__ui.actionAccept_O3: '-O3',
            self.__ui.actionAccept_Ofast: '-Ofast',
            self.__ui.actionAccept_Og: '-Og',
        }
        self._opts_all = self.__ui.actionAccept_all_Optimizations

        # add trigger to buttons
        self._opts_all.triggered.connect(self._cb_on_select_all_opts)
        for elem in self._opts_menus:
            elem.triggered.connect(self._cb_on_select_opts)
        self.__ui.folderBtn.clicked.connect(self._select_folder)
        self.__ui.fileBtn.clicked.connect(self._select_file)
        self.__ui.versionLbl.setText(__version__)
        self.__ui.startbtn.clicked.connect(self.run)

        sys.exit(self.__app.exec_())

    def _cb_on_select_all_opts(self, status):
        """
        selects all other optimizations if option "all" is selected

        :return: None
        :rtype: None
        """
        if status:
            for elem in self._opts_menus:
                elem.setChecked(False)

    def _cb_on_select_opts(self):
        """
        deselects option "all" optimizations if one optimization is deselected

        :return: None
        :rtype: None
        """
        if self._opts_all.isChecked():
            self._opts_all.setChecked(False)

    def get_accepted_opts(self):
        """
        evaluates what optimizations are allowed

        :return: list
        :rtype: list
        """
        _acc_opts = []
        for elem in self._opts_menus:
            if elem.isChecked() or self._opts_all.isChecked():
                _acc_opts.append(self._opt_menu_to_str[elem])
        return _acc_opts

    @staticmethod
    def _eval_export_file():
        """
        Evaluates to which file result is saved

        :return: file name with full path of final export file
        :rtype: str
        """
        curr_path = os.getcwd()
        if os.path.exists(os.path.join(curr_path, 'result.txt')):
            cnt = 1
            file_name = os.path.join(curr_path, 'result_' + str(cnt) + '.txt')
            while os.path.exists(file_name):
                cnt += 1
                file_name = os.path.join(curr_path, 'result_' + str(cnt) + '.txt')
            return file_name
        else:
            return os.path.join(curr_path, 'result.txt')

    def _select_folder(self):
        """
        opens file dialog window to select project folder
        :return: None
        :rtype: None
        """
        folder = QtWidgets.QFileDialog.getExistingDirectory(self.__win, 'Select project folder')
        if folder is not None and folder != "":
            self._logger.info("Selected project folder: {}".format(folder))
            self.source_folder = folder
            self.source_file = None
            self._update_lbl(self.__ui.srcEntryLbl, folder, 42, cut_end='front')
            self._enable_start_btn()

    def _select_file(self):
        """
        opens file dialog window to select start file
        :return: None
        :rtype: None
        """
        file = QtWidgets.QFileDialog.getOpenFileName(self.__win, 'Select start file', filter='C files (*.c);;All files (*.*)')[0]
        if file is not None and file != "":
            self._logger.info("Selected start file: {}".format(file))
            self.source_file = file
            self.source_folder = None
            self._update_lbl(self.__ui.srcEntryLbl, file, 42, cut_end='front')
            self._enable_start_btn()

    def _enable_start_btn(self):
        """
        enables start button if project folder and start file are set
        :return: None
        :rtype: None
        """
        self.__ui.startbtn.setEnabled(True)

    @staticmethod
    def _update_lbl(lbl, text, max_length, cut_end='front'):
        """
        updates label with new text and resizes if text to long

        :param lbl: label to update
        :type lbl: QtWidgets.QLabel
        :param text: text to display on label
        :type text: str
        :param max_length: maximum amount of digits
        :type max_length: int
        :param cut_end: either end or front, the direction the string is cut
        :type cut_end: str
        :return: None
        :rtype: None
        """
        if len(text) <= max_length:
            lbl.setText(text)
        else:
            if cut_end == 'front':  # replace front part of string
                lbl.setText('... ' + str(text)[-max_length:])
            if cut_end == "end":
                lbl.setText(str(text)[:max_length] + ' ...')

    def _enable_all_btns(self, state):
        """ helper function to act on all buttons at once """
        self.__ui.fileBtn.setEnabled(state)
        self.__ui.folderBtn.setEnabled(state)
        self.__ui.startbtn.setEnabled(state)

    def _update_info(self, text):
        """
        sets text to progress info label

        :param text: text to set
        :type text: str
        :return: None
        :rtype: None
        """
        self._update_lbl(self.__ui.infoLbl, text, 40, cut_end='back')

    def _update_progressbar(self, val):
        """
        updates progressbar

        :return: None
        :rtype: None
        """
        val = max(min(val, 100), 0)
        self.__ui.progressBar.setValue(val)

    def run(self):
        """
        execute main task in new self.thread.
        Disable all buttons for this duration.

        :return: None
        :rtype: None
        """
        try:
            t = time.time()
            self._update_progressbar(0)
            self.result_file = self._eval_export_file()

            # setup worker and thread environment
            self._thread = QThread()
            self._worker = Worker(self)

            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run)
            self._worker.finished.connect(self._thread.quit)
            self._worker.finished.connect(self._worker.deleteLater)
            self._thread.finished.connect(self._thread.deleteLater)
            self._worker.progress_val.connect(self._update_progressbar)
            self._worker.progress_info.connect(self._update_info)
            self._thread.start()

            # disable all buttons and enable after run
            self._enable_all_btns(False)
            self._thread.finished.connect(lambda: self._enable_all_btns(True))
            self._thread.finished.connect(lambda: self._logger.info(f"Finished after {round(time.time() - t, 5)} s."))

        except Exception as e:
            self._logger.critical("Internal error:", e)


if __name__ == '__main__':
    _tool = FindNonOptimizedCFunctions()
