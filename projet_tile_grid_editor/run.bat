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
    IF "%2"=="all" (
        ECHO [INFO] Lint on all files
        pylint editor.py > next.txt
        pylint layeredmap.py >> next.txt
        pylint tests.py >> next.txt
        pylint imgedit.py >> next.txt
        FOR /F "delims=" %%A IN (next.txt) DO CALL :action "%%A"
        GOTO :EOF
    )
    SET target=editor.py
    IF NOT "%2"=="" (
        SET target=%2
    )
    ECHO [INFO] Lint on !target!
    pylint !target! > next.txt
    ::more next.txt
    FOR /F "delims=" %%A IN (next.txt) DO CALL :action "%%A"
    GOTO :EOF
)
IF "%1"=="help" (
    ECHO nothing     = run python editor.py
    ECHO build       = python setup.py build ^> build.txt
    ECHO pylint      = run pylint editor.py ^> next.txt
    ECHO pylint file = run pylint file ^> next.txt
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
