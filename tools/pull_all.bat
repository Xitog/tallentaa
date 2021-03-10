@echo off
rem status:       lx      w8      w10     https                                   ssh
rem ash           yes     yes             https://github.com/Xitog/ash.git        git@github.com:Xitog/ash.git
rem dgx           yes     yes             https://github.com/Xitog/dgx.git        git@github.com:Xitog/dgx.git
rem hamill        yes     yes             https://github.com/Xitog/hamill.git     git@github.com:Xitog/hamill.git
rem jyx           yes     yes             https://github.com/Xitog/jyx.git        git@github.com:Xitog/jyx.git
rem tal                   yes             https://github.com/Xitog/tal.git        git@github.com:Xitog/tal.git
rem tallentaa     yes     yes             https://github.com/Xitog/tallentaa.git  git@github.com:Xitog/tallentaa.git
rem teddy         yes     yes             https://github.com/Xitog/teddy.git      git@github.com:Xitog/teddy.git
rem raycasting    yes     yes             https://github.com/Xitog/raycasting.git git@github.com:Xitog/raycasting.git
rem weyland       yes     yes             https://github.com/Xitog/weyland.git    git@github.com:Xitog/weyland.git

rem GREEN='\033[1;32m'
rem RED='\033[1;31m'
rem NC='\033[0m' # No Color

rem nb=$(find . -mindepth 1 -maxdepth 1 -type d | wc -l)
rem echo Total of local repository: $nb
rem printf "\n"

rem count=1
rem $count/$nb

for /d %%G in (*) do (
    echo ---------------------------------------------------------------
    echo Updating %%G
    echo ---------------------------------------------------------------
    cd %%G
    git pull
    git status
    git remote -v
    cd ..
)

echo ** Fin **
echo.

