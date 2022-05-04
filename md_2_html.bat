@echo off

if "%1"=="" (
    set src=guideline.md
    set dst=guideline.html
) else (
    set src=%1
    set dst=%~n1%.html
)
set pandoc=C:\Users\nkmanager\AppData\Local\Pandoc\pandoc.exe

echo ^<html^>^<head^>^<style^> > %dst%
echo table{border-collapse:collapse;} >> %dst%
echo th,td{border:1px black solid;padding:5px 10px;} >> %dst%
echo th{text-align:center;background-color:lightgray;} >> %dst%
echo ^</style^>^</head^>^<body^> >> %dst%
%pandoc% -f markdown -t html %src% >> %dst%
echo ^</body^>^</html^> >> %dst%