# Test of Bottle 0.12.13
# http://bottlepy.org/docs/dev/tutorial.html <3
# Initiated the : ‎jeudi ‎24 ‎août ‎2017
# Modified the : jeudi 31 août 2017

import sys
import os.path
sys.path.append(os.path.join(sys.path[0], "bottle"))  

from bottle import Bottle, route, run, template

app = Bottle()

@app.route('/hello/<name>')
def hello(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@app.route('/')
def index():
    return "<h1>Hello Bottle World!</h1>"

#@route('/hello/<name>')
#def index(name):
#    return template('<b>Hello {{name}}</b>!', name=name)

run(app, host='localhost', port=8080)
