#import hamill
#import sys
#sys.path.append(r"C:\Users\damie_000\Documents\GitHub\tallentaa\projet_format\hamill\hamill")

# COPY FIRST THE LATEST VERSION OF THE HAMILL PACKAGE IN THIS DIRECTORY
import hamill

print(hamill.__version__)

includes = ['menu.html']

hamill.process('input', 'output', 'fr', includes)

#hamill.process_file(r'input\tests.hml', r'output\tests.html', 'fr', includes)

