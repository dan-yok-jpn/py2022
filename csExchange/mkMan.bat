@echo off
set PYTHONHOME=%USERPROFILE%\AppData\Local\Programs\Python\Python310
set module=%~n1%
if "%module%" == "" (
    set module=csExchange
)
py %PYTHONHOME%\Lib\pydoc.py -w .\%module%.py
sed.exe --in-place -e "3i <style type=""text/css"">td {font-size:16px}</style\>" %module%.html