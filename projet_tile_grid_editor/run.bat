@echo off
IF "%1"=="" (
    python editor.py
) ELSE IF "%1"=="pylint" (
    pylint editor.py > next.txt
    more next.txt
) ELSE IF "%1"=="help" (
    ECHO nothing = run python editor.py
    ECHO pylint  = run pylint editor.py ^> next.txt
) ELSE (
    ECHO Unknown command: %1
)
