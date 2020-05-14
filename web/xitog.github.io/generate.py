import hamill

print(hamill.__version__)

includes = ['menu.html']

hamill.process('input', 'output', 'fr', includes)


