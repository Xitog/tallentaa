@ECHO OFF

rem display the last line of the pylint file
rem use !var! for safe echo and for /F

SETLOCAL EnableDelayedExpansion
IF "%1"=="" (
    python editor.py
    GOTO :EOF
) 
IF "%1"=="build" (
    python setup.py build > build.txt
    GOTO :EOF
)
IF "%1"=="pylint" (
    pylint editor.py > next.txt
    ::more next.txt
    FOR /F "delims=" %%A IN (next.txt) DO CALL :action "%%A"
    GOTO :EOF
)
IF "%1"=="help" (
    ECHO nothing = run python editor.py
    ECHO build   = python setup.py build ^> build.txt
    ECHO pylint  = run pylint editor.py ^> next.txt
    GOTO :EOF
) 
ECHO Unknown command: %1
GOTO :EOF

:action
SET PARAMETER=%~1
SET START=%PARAMETER:~0,9%
IF "%START%"=="Your code" (
    ECHO !PARAMETER!
)
GOTO :EOF

:EOF
