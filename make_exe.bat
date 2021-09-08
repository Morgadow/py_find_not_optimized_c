@echo off & setlocal

pyinstaller --name optimize^
   --paths "%cd%"^
   --onefile ^
   --clean ^
   --noconsole ^
   --add-data "%cd%\ui";"ui" ^
   --add-data "%cd%\ui\icon.ico";"ui/" ^
   --icon "%cd%\ui\icon.ico" ^
   .\main.py
   
   
 pyinstaller --name optimize_DEBUG^
   --paths "%cd%"^
   --onefile ^
   --clean ^
   --debug=all ^
   --add-data "%cd%\ui";"ui" ^
   --add-data "%cd%\ui\icon.ico";"ui/" ^
   --icon "%cd%\ui\icon.ico" ^
   .\main.py
   
   
if exist %cd%\build rmdir /s /q %cd%\build 
if exist optimize.spec del optimize.spec
if exist optimize_DEBUG.spec del optimize_DEBUG.spec