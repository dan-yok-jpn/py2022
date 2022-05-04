: @echo off

if "%1"=="" (
    set src=guideline.md
    set dst=guideline.tex
) else (
    set src=%1
    set dst=%~n1%.tex
)
set pandoc=C:\Users\nkmanager\AppData\Local\Pandoc\pandoc.exe

echo \documentclass{jsarticle} > %dst%
echo \usepackage[dvipdfmx]{hyperref} >> %dst%
echo \usepackage{pxjahyper} >> %dst%
echo \usepackage{longtable} >> %dst%
echo \usepackage{booktabs} >> %dst%
echo \providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}} >> %dst%
echo \begin{document} >> %dst%
%pandoc% -f markdown -t latex %src% >> %dst%
echo \end{document} >> %dst%