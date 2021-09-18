# py_find_not_optimized_c

Small program that parses C code and extracts functions not already compiler optimized. 
Can be used to add missing optimizations or to replace optimizations with others.

## Usage
1) Select desired optimization which is accepted as "already set optimization" over function header by using the menu bar. As default all optimizations are accepted.
2) Then select either folder with C source code or single .c code file.
3) Start analyzing using the "_**Go**_" button
4) The result file is creating in the current working directory. This file should be opened as well.


    Important: 
        Only for GCC Compiler like optimizations with format: __attribute__((optimize("-Os"))) !
        Every other possible GCC optimization is recognized as well of course.