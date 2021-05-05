#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

import logging
import os.path
import hamill
jp = os.path.join

#-------------------------------------------------------------------------------

includes = ['menu.html']

def do(filepath, lang='fr'):
    hamill.process_file(jp('input', *filepath.split('/')), 
                        jp('output', *filepath.split('/'))[:-4] + '.html',
                        lang,
                        includes)

print('Using Hamill:', hamill.__version__)

# Get the last version of Hamill
#import os
#if refresh_hamill:
#    os.system('get_last.bat')

logging.getLogger().setLevel(logging.DEBUG)

# Full
#hamill.process('input', 'output', 'fr', includes)

# Mono

#do('index.hml')

#hamill.process_file(r'input\informatique\json.hml', r'output\informatique\json.html', 'fr', includes)
#hamill.process_file(jp('input', 'informatique', 'bnf.hml'), jp('output', 'informatique', 'bnf.html'), 'fr', includes)
#hamill.process_file(r'input\informatique\hamill.hml', r'output\informatique\hamill.html', 'fr', includes)
#hamill.process_file(r'input\informatique\tools_langs.hml', r'output\informatique\tools_langs.html', 'fr', includes)
#hamill.process_file(r'input\informatique\ash_guide.hml', r'output\informatique\ash_guide.html', 'fr', includes)
#do('informatique/lua.hml')
#do('informatique/python.hml')

#hamill.process_file(r'input\passetemps\tech_dialogues.hml', r'output\passetemps\tech_dialogues.html', 'fr', includes)
#hamill.process_file(r'input\passetemps\tech_transitions.hml', r'output\passetemps\tech_transitions.html', 'fr', includes)

#do('passetemps/pres_jeux.hml')
#do('passetemps/pres_favoris.hml')
do('passetemps/pres_jeuxvideo.hml')
#hamill.process_file(r'input\passetemps\tech_raycasting_fr.hml', r'output\passetemps\tech_raycasting_fr.html', 'fr', includes)

#hamill.process_file(jp('input', 'passetemps', 'history_fps_tables_en.hml'), jp('output', 'passetemps', 'history_fps_tables_en.html'), 'fr', includes)
#hamill.process_file(jp('input', 'passetemps', 'history_fps_references_en.hml'), jp('output', 'passetemps', 'history_fps_references_en.html'), 'fr', includes)

#hamill.process_file(jp('input', 'histoire', 'bibliographie.hml'), jp('output', 'histoire', 'bibliographie.html'), 'fr', includes)
#hamill.process_file(jp('input', 'tests.hml'), jp('output', 'tests.html'), 'fr', includes)
