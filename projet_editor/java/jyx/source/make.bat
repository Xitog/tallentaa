@echo off

set arg1=%1

set JAVA_HOME="C:\Program Files (x86)\Dev\sun-jdk-5-win32-x86-1.5.0.12"
set SOURCE_DIR="C:\Users\damie_000\Documents\GitHub\tallentaa\java\jyx"
set DESTINATION_DIR="C:\Users\damie_000\Documents\GitHub\jyx"

rem Clean
cd %DESTINATION_DIR%
del jyx.jar >NUL 2>&1
cd %SOURCE_DIR%
del ..\jyx.jar >NUL 2>&1

if "%arg1%"=="clean" (
    echo Files cleaned.
    goto :exit
)

if not "%arg1%"=="build" (
    echo Usage:
    echo - make.bat clean : clean files.
    echo - make.bat build : build a new version.
    goto :exit
)

rem Compile
cd %SOURCE_DIR%
%JAVA_HOME%\bin\javac.exe -encoding UTF-8 *.java
rem Make Jar
cd ..
%JAVA_HOME%\bin\jar.exe cfm jyx.jar jyx\manifest.txt jyx\*.class

rem Deploy
cd %SOURCE_DIR%
copy /Y *.java /B %DESTINATION_DIR%\src\jyx\ >NUL
copy /Y *.class /B %DESTINATION_DIR%\bin\jyx\ >NUL
copy /Y manifest.txt /B %DESTINATION_DIR%\ >NUL
cd ..
copy /Y jyx.jar /B  %DESTINATION_DIR%\ >NUL

rem Launch
cd %DESTINATION_DIR%
%JAVA_HOME%\bin\java.exe -jar jyx.jar -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true

:exit

rem Back to basic
cd %~dp0
