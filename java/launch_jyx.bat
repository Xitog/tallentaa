@echo off

set REPO=C:\Users\damie_000\Documents\GitHub\jyx\
set JAVA_HOME=C:\Program Files (x86)\Dev\sun-jdk-5-win32-x86-1.5.0.12
set BACK=%~dp0

cd %REPO%
start /B "" "%JAVA_HOME%\bin\javaw.exe" -jar jyx.jar
cd %BACK%
