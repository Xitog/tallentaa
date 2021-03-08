# status:       lx      w8      w10     https                                   ssh
# ash                   yes             https://github.com/Xitog/ash.git        git@github.com:Xitog/ash.git
# dgx           yes     yes             https://github.com/Xitog/dgx.git        git@github.com:Xitog/dgx.git
# hamill                yes             https://github.com/Xitog/hamill.git     git@github.com:Xitog/hamill.git
# jyx           yes     yes             https://github.com/Xitog/jyx.git        git@github.com:Xitog/jyx.git
# tal                   yes             https://github.com/Xitog/tal.git        git@github.com:Xitog/tal.git
# tallentaa     yes     yes             https://github.com/Xitog/tallentaa.git  git@github.com:Xitog/tallentaa.git
# teddy         yes     yes             https://github.com/Xitog/teddy.git      git@github.com:Xitog/teddy.git
# raycasting            yes             https://github.com/Xitog/raycasting.git git@github.com:Xitog/raycasting.git
# weyland       yes     yes             https://github.com/Xitog/weyland.git    git@github.com:Xitog/weyland.git

GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m' # No Color

for file in */
do
    name=${file%*/} 
    echo ---------------------------------------------------------------
    echo Updating "$name";
    echo ---------------------------------------------------------------
    cd $file
    output="$(pull)"
    if [ "$output" = "Déjà à jour." ]
    then
        echo -e "${GREEN}$output${NC}"
    fi
    if [ "$output" != "Déjà à jour." ]
    then
        echo -e "${RED}$output${NC}"
    fi
    git status
    git remote -v
    cd ..
    printf "\n"
done

printf "** Fin **\n"

