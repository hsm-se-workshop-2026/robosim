@echo off
setlocal DisableDelayedExpansion

if "%~1"=="" goto usage
if not "%~3"=="" goto usage
if /I not "%~x1"==".puml" goto usage
set "format=svg"
if not "%~2"=="" (
    if /I "%~2"=="svg" (set "format=svg") else if /I "%~2"=="png" (set "format=png") else if /I "%~2"=="pdf" (set "format=pdf") else (goto usage)
)
if not exist "%~f1" (
    echo Datei nicht gefunden: "%~1" 1>&2
    exit /b 1
)
if exist "%~f1\NUL" (
    echo Keine Datei: "%~1" 1>&2
    exit /b 1
)
if "%~z1"=="0" (
    echo Die PlantUML-Datei ist leer: "%~1" 1>&2
    exit /b 1
)

set "output=%~dpn1.%format%"

:tempname
set "temporary=%~dp1.kroki-%RANDOM%-%RANDOM%.tmp"
if exist "%temporary%" goto tempname
set "hexfile=%temporary%.hex"
if exist "%hexfile%" goto tempname

echo Sende "%~1" an kroki.io ...
curl.exe --fail --silent --show-error --max-time 60 ^
    --header "Content-Type: text/plain; charset=utf-8" ^
    --data-binary "@%~f1" ^
    --output "%temporary%" ^
    "https://kroki.io/plantuml/%format%"
if errorlevel 1 (
    echo Rendern fehlgeschlagen. Die bestehende Ausgabedatei bleibt unveraendert. 1>&2
    goto failure
)

if "%format%"=="svg" goto checksvg
certutil.exe -f -encodehex "%temporary%" "%hexfile%" 12 >nul
if errorlevel 1 goto invalid
if "%format%"=="png" findstr /b /i /c:"89504e470d0a1a0a" "%hexfile%" >nul
if "%format%"=="pdf" findstr /b /i /c:"255044462d" "%hexfile%" >nul
if errorlevel 1 goto invalid
goto save

:checksvg
findstr /r /c:"<svg[ >]" "%temporary%" >nul
if errorlevel 1 goto invalid

:save
if exist "%hexfile%" del /q "%hexfile%"
move /y "%temporary%" "%output%" >nul
if errorlevel 1 (
    echo Ausgabedatei konnte nicht gespeichert werden: "%output%" 1>&2
    goto failure
)
echo Erzeugt: "%output%"
exit /b 0

:invalid
echo Keine erkennbare %format%-Datei erhalten. Die bestehende Ausgabedatei bleibt unveraendert. 1>&2

:failure
if exist "%temporary%" del /q "%temporary%"
if exist "%hexfile%" del /q "%hexfile%"
exit /b 1

:usage
echo Verwendung: scripts\render_diagram.bat DATEI.puml [svg^|png^|pdf] 1>&2
exit /b 2
