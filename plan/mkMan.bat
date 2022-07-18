@echo off
set PYTHONHOME=C:\Users\dan_y\AppData\Local\Programs\Python\Python310
set BIN_UTIL=C:\Git\usr\bin
set module=%~n1%
if "%module%" == "" (
    set module=shareRiver
)
py %PYTHONHOME%\Lib\pydoc.py -w .\%module%.py
%BIN_UTIL%\sed.exe --in-place -e "3i <style type=""text/css"">td {font-size:16px}</style\>" %module%.html