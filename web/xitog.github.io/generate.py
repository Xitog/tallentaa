#import hamill
#import sys
#sys.path.append(r"C:\Users\damie_000\Documents\GitHub\tallentaa\projet_format\hamill\hamill")

# COPY FIRST THE LATEST VERSION OF THE HAMILL PACKAGE IN THIS DIRECTORY
import hamill

print(hamill.__version__)

includes = ['menu.html']

# Full
hamill.process('input', 'output', 'fr', includes)

# Mono
#hamill.process_file(r'input\passetemps\pres_jeux.hml', r'output\passetemps\pres_jeux.html', 'fr', includes)
#hamill.process_file(r'input\histoire\bibliographie.hml', r'output\histoire\bibliographie.html', 'fr', includes)
#hamill.process_file(r'input\tests.hml', r'output\tests.html', 'fr', includes)

