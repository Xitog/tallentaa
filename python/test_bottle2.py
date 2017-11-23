from bottle import Bottle, route, run, template, request, static_file

#-----------------------------------------------------------
# Avec une fonction
#-----------------------------------------------------------

#@route('/hello/<name>')
#def index(name):
#    if name == "pipo":
#        print("ahah")
#    return template('<b>Hello {{name}}</b>!', name=name)

#run(host='localhost', port=8080)

#-----------------------------------------------------------
# Avec une application
#-----------------------------------------------------------

app = Bottle()

@app.route('/')
def hello():
    return "zorba"

@app.route('/hello/<name>')
def greetings(name):
    return "hello " + name

@app.route('/param')
def param():
    if len(request.params) > 0:
        s = 'Parameters:<ul>'
        for par in request.params:
            s += '<li>' + par + '</li>'
        s += '</ul>'
    else:
        s = 'No parameter'
    return s

@app.route('/image/<filename:path>')
def server_static(filename):
    return static_file(filename, root=r'D:\Users\gouteud\Desktop')

run(app, host='localhost', port=8080)
