#!/bin/sh
cd ../../

clear

out="jyx"
origin="tallentaa/projets/jyx"

old_proxy=$https_proxy
export https_proxy=

echo -n "Publishing "
more $origin/jyx/jyx.py | grep "VERSION = " | xargs

#-----------------------
# Rebase from Tallentaa
#-----------------------

echo -n "Rebase from tallentaa? (y/n/q) : "
read yn

if [ "$yn" = "q" ] || [ "yn" = "Q" ]; then
    exit
elif [ "$yn" = "y" ] || [ "yn" = "Y" ]; then

    if [ -d $out ]; then
        echo "Suppression de $out"
        rm -f -R $out
    fi

    if [ ! -d $out ]; then
        echo "Création de $out"
        git clone https://github.com/Xitog/jyx.git
        rm -f $out/*.py
        rm -f $out/*.xmi
        rm -f $out/*.dot
        rm -f $out/LICENSE
        rm -f $out/*.md
        rm -f $out/*.sh
        rm -f $out/*.python
        rm -f $out/*.bat
        rm -f $out/*.json
        rm -f -R $out/output
        rm -f -R $out/jyx
        mkdir $out/jyx
        #mkdir $out # Github repo
        #mkdir $out/jyx # PyPI repo
    fi

    # The Github repo

    cp -v $origin/jyx.json $out/jyx.json
    cp -v $origin/publish.sh $out/publish.sh
    cp -v $origin/publish.bat $out/publish.bat
    cp -v $origin/run.py $out/run.py
    cp -v $origin/setup.py $out/setup.py
    # don't copy temp.python, model.xmi, output.dot, output/

    # The PyPI repo

    cp -Rv $origin/jyx/icons    $out/jyx/icons
    cp -v $origin/jyx/jyx.json    $out/jyx/jyx.json
    cp -v $origin/jyx/__init__.py $out/jyx/__init__.py
    cp -v $origin/jyx/jyx.py      $out/jyx/jyx.py
    cp -v $origin/jyx/readme.md   $out/jyx/readme.md
    # don't copy output.dot

    # From PyPI to Github

    cp -v $origin/jyx/readme.md   $out/README.md
    cp -v $origin/jyx/licence.txt $out/LICENSE
    cp -v $origin/jyx/jyx.desktop $out/jyx.desktop

fi

# Info

cd $out
git add .
git status

#-------------------
# Publish on GitHub
#-------------------

echo -n "Publish on Github? (y/n/q) : "
read yn

if [ "$yn" = "q" ] || [ "yn" = "Q" ]; then
    exit
elif [ "$yn" = "y" ] || [ "yn" = "Y" ]; then
    echo -n "Commit message? : "
    read msg
    git commit -m "$msg"
    git push
fi

cd ..

#-----------------
# Publish on PyPI
#-----------------

echo -n "Publish on PyPI? (y/n/q) : "
read yn

if [ "$yn" = "q" ] || [ "yn" = "Q" ]; then
    exit
elif [ "$yn" = "y" ] || [ "yn" = "Y" ]; then
    echo "Publishing on PyPI"
    cd $out

    if [ -f "build" ]; then
        rm -rf "build"
    fi
    if [ -f "dist" ]; then
        rm -rf "dist"
    fi
    python3 setup.py sdist bdist_wheel
    twine upload dist/*
    rm -rf "jyx.egg-info"
    rm -rf "build"
    rm -rf "dist"
else
    echo "No publication on PyPI"
fi

# See the results in https://pypi.org/project/jyx/

export https_proxy=$old_proxy

