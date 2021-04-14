# See the results in https://pypi.org/project/<PROJECT>/
echo "------------------------"
echo "Publishing $1"
echo "------------------------"

if [ $1 = "ash" ]; then
    egg="ashlang"
else
    egg=$1
fi

cd $1
echo "Working in $PWD"

if [ -f "build" ]; then
    rm -rf "build"
fi
if [ -f "dist" ]; then
    rm -rf "dist"
fi

python setup.py sdist bdist_wheel

twine upload dist/*

rm -rf "$egg.egg-info"
rm -rf "build"
rm -rf "dist"

cd ..
