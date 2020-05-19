if "%1"=="build" (
    rmdir dist /S /Q
    python setup.py sdist bdist_wheel
)
if "%1"=="upload" (
    twine upload dist\*
)
if "%1"=="all" (
    rmdir dist /S /Q
    python setup.py sdist bdist_wheel
    twine upload dist\*
)
