# status:       lx      w8      w10     https                                   ssh
# ash           yes     yes             https://github.com/Xitog/ash.git        git@github.com:Xitog/ash.git
# dgx           yes     yes             https://github.com/Xitog/dgx.git        git@github.com:Xitog/dgx.git
# hamill        yes     yes             https://github.com/Xitog/hamill.git     git@github.com:Xitog/hamill.git
# jyx           yes     yes             https://github.com/Xitog/jyx.git        git@github.com:Xitog/jyx.git
# tal                   yes             https://github.com/Xitog/tal.git        git@github.com:Xitog/tal.git
# tallentaa     yes     yes             https://github.com/Xitog/tallentaa.git  git@github.com:Xitog/tallentaa.git
# teddy         yes     yes             https://github.com/Xitog/teddy.git      git@github.com:Xitog/teddy.git
# raycasting    yes     yes             https://github.com/Xitog/raycasting.git git@github.com:Xitog/raycasting.git
# weyland       yes     yes             https://github.com/Xitog/weyland.git    git@github.com:Xitog/weyland.git

GREEN='\033[1;32m'
RED='\033[1;31m'
NC='\033[0m' # No Color

nb=$(find . -mindepth 1 -maxdepth 1 -type d | wc -l)
echo Total of local repository: $nb
printf "\n"

count=1
ok=0

for file in */
do
    name=${file%*/} 
    echo ---------------------------------------------------------------
    echo Updating "$name" $count/$nb
    echo ---------------------------------------------------------------
    cd $file
    output="$(git pull)"
    if [ "$output" = "Déjà à jour." ]
    then
        echo -e "${GREEN}$output${NC}"
        ok=1
    fi
    if [ "$output" = "Already up to date." ]
    then
        echo -e "${GREEN}$output${NC}"
        ok=1
    fi
    if [ ok = 0 ]
    then
        echo -e "${RED}$output${NC}"
    fi
    git status
    git remote -v
    cd ..
    printf "\n"
    let "count+=1"
done

printf "** Fin **\n"

