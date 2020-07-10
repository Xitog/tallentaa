#import hamill
#import sys
#sys.path.append(r"C:\Users\damie_000\Documents\GitHub\tallentaa\projet_format\hamill\hamill")

refresh_hamill = False

import os
import logging

# Get the last version of Hamill
if refresh_hamill:
    os.system('get_last.bat')

# COPY FIRST THE LATEST VERSION OF THE HAMILL PACKAGE IN THIS DIRECTORY
import hamill

print(hamill.__version__)

includes = ['menu.html']

logging.getLogger().setLevel(logging.DEBUG)

# Full
hamill.process('input', 'output', 'fr', includes)

# Mono

#hamill.process_file(r'input\index.hml', r'output\index.html', 'fr', includes)

#hamill.process_file(r'input\informatique\json.hml', r'output\informatique\json.html', 'fr', includes)
#hamill.process_file(r'input\informatique\bnf.hml', r'output\informatique\bnf.html', 'fr', includes)
#hamill.process_file(r'input\informatique\hamill.hml', r'output\informatique\hamill.html', 'fr', includes)
#hamill.process_file(r'input\informatique\tools_langs.hml', r'output\informatique\tools_langs.html', 'fr', includes)
#hamill.process_file(r'input\informatique\ash_guide.hml', r'output\informatique\ash_guide.html', 'fr', includes)

#hamill.process_file(r'input\passetemps\tech_transitions.hml', r'output\passetemps\tech_transitions.html', 'fr', includes)
#hamill.process_file(r'input\passetemps\pres_jeux.hml', r'output\passetemps\pres_jeux.html', 'fr', includes)
#hamill.process_file(r'input\passetemps\pres_jeuxvideo.hml', r'output\passetemps\pres_jeuxvideo.html', 'fr', includes)
#hamill.process_file(r'input\passetemps\tech_raycasting_fr.hml', r'output\passetemps\tech_raycasting_fr.html', 'fr', includes)

#hamill.process_file(r'input\histoire\bibliographie.hml', r'output\histoire\bibliographie.html', 'fr', includes)#hamill.process_file(r'input\tests.hml', r'output\tests.html', 'fr', includes)
