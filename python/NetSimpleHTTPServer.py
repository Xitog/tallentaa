from http.server import BaseHTTPRequestHandler
from http.server import CGIHTTPRequestHandler
from http.server import HTTPServer
import http.server
import os # sep listdir
import urllib.parse
import socketserver
import sys
import socket
import time
import threading

import cgitb
cgitb.enable()

# SimpleHTTPRequestHandler hérite de BaseHTTPRequestHandler
# et donne un simple do_GET et do_HEAD
class HTTPHandler(CGIHTTPRequestHandler):

    def is_cgi(self):
        collapsed_path = http.server._url_collapse_path(urllib.parse.unquote(self.path))
        print('Collapsed path = ', collapsed_path)
        dir_sep = collapsed_path.find('/', 1)
        print('Dir sep = ', dir_sep)
        head, tail = collapsed_path[:dir_sep], collapsed_path[dir_sep+1:]
        print('Head = ', head)
        print('Tail = ', tail)
        self.cgi_info = head, tail
        if tail.endswith('.py'):
            return True
        else:
            return False
    
    WWW = r"C:\Users\damie_000\Desktop\Projets\Code"
    
    def do_HEAD(self):
        """Send header for a request."""
        print("do_HEAD")
        self.send_response(200)
        self.send_header("Content-type", self.mime_type)
        self.end_headers()

    def error(self):
        """Handle error."""
        print("do_ERROR for [%s]" % self.path)
        self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        print("post")
    
    def do_GET(self):
        """Answer to a GET request."""
        path = urllib.parse.unquote(self.path, encoding='utf-8')
        print("do_GET for [%s]" % path)
        # HTML return
        if path == "/": # could be set to path="/index.html"
            self.mime_type = 'text/html'
            self.do_HEAD()
            content = """<html>
                <body><h1>Hello World</h1>
                <ul>
                    <li>Path requested : %s</li>
                    <li>Path modified : %s</li>
                </ul>
                </body>
            </html>""" % (self.path, path)
            self.wfile.write(content.encode('utf-8'))
        elif path == "/list":
            self.mime_type = 'text/html'
            self.do_HEAD()
            self.wfile.write("<html><body><ul>".encode('utf-8'))
            c = os.listdir(HTTPHandler.WWW)
            for f in c:
                r = "<li>%s</li>" % (f,)
                self.wfile.write(r.encode('utf-8'))
            self.wfile.write("</ul></body></html>".encode('utf-8'))
        else:
            self.mime_type = self.get_mime_type(path)
            if self.mime_type is None:
                self.error()
            elif self.mime_type == 'cgi_python':
                #import subprocess
                #result = subprocess.run(['python', HTTPHandler.WWW + os.sep + path], stdout=subprocess.PIPE)
                #self.wfile.write(result.stdout)
                CGIHTTPRequestHandler.cgi_directories = ['/', 'Code'] # ne marche pas
                CGIHTTPRequestHandler.do_POST(self)
            else:
                try:
                    f = open(HTTPHandler.WWW + os.sep + path, 'rb') # os.curdir = '.' can be used (ou getcwd())
                    self.do_HEAD()
                    self.wfile.write(f.read())
                    f.close()
                    return
                except IOError:
                    self.error()
        
        # encoding = sys.getfilesystemencoding()
        # self.send_header("Content-type", "text/html; charset=%s" % encoding)
        # self.send_header("Content-Length", str(h))

    def get_mime_type(self, path):
        """Get the mime type from the ending of the path requested."""
        mime_type = None
        if path.endswith(".html"):
            mime_type = 'text/html'
        elif path.endswith(".jpg"):
            mime_type = 'image/jpg'
        elif path.endswith(".gif"):
            mime_type = 'image/gif'
        elif path.endswith(".js"):
            mime_type = 'application/javascript'
        elif path.endswith(".css"):
            mime_type = 'text/css'
        elif path.endswith(".png"):
            mime_type = 'image/png'
        elif path.endswith(".ico"):
            mime_type = 'image/ico'
        elif path.endswith(".pdf"):
            mime_type = 'application/pdf'
        elif path.endswith(".json"):
            mime_type = 'application/json'
        elif path.endswith(".py"):
            mime_type = 'cgi_python'
        return mime_type

def server_function(host, port, handler):
    #with HTTPServer((Host, Port), Handler) as httpd: # with ne marche pas sur le server
    httpd = HTTPServer((host, port), handler) # autre façon
    #httpd = socketserver.TCPServer((host, port), Handler)
    print("[INFO] Serving start at %s at port %s on %s " % (time.asctime(), PORT, HOST))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt: # not needed for server mode
        pass
    httpd.server_close()

PORT = 8012
HOST = socket.gethostbyname(socket.gethostname()) # or localhost
MODE = 'HTML' #'CGI' # 'HTML'

if __name__ == '__main__':
    print("Host = %s, Port = %s, Mode = %s" % (HOST, PORT, MODE))
    if MODE == 'HTML':
        Handler = HTTPHandler
        a = threading.Thread(None, server_function, "ServerThread", (HOST, PORT, Handler))
    elif MODE == 'CGI':
        Handler = CGIHTTPRequestHandler
        Handler.cgi_directories = ['/', '/Code'] # very important inside '/Code', not working :-(
        a = threading.Thread(None, server_function, "ServerThread", (HOST, PORT, Handler))
    a.start()
