if "%1"=="build" (
    python setup.py sdist bdist_wheel
)
if "%1"=="upload" (
    twine upload dist\*
)
