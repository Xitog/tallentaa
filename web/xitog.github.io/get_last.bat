if not exist hamill (
    mkdir hamill
)
copy ..\..\projets\hamill\hamill\__init__.py  hamill\__init__.py  /B /Y
copy ..\..\projets\hamill\hamill\hamill.py    hamill\hamill.py    /B /Y
copy ..\..\projets\hamill\hamill\tokenizer.py hamill\tokenizer.py /B /Y