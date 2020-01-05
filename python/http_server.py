# Created ‎mardi ‎10 ‎juillet ‎2018

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from http.server import *
from os import curdir, sep
import urllib.parse
import socket
import time
import threading

#-------------------------------------------------------------------------------
# Request Handler
#-------------------------------------------------------------------------------

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        """Header for a request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        """Respond to a GET request."""
        path = urllib.parse.unquote(self.path, encoding='utf-8')
        print("GET :[%s]" % path) 
        
        if path == "/":
            self.send_response(200)
            self.send_header('Content-Type','text/html')
            self.end_headers()
            msg = "<html><head><title>Test : %s</title></head><body><h1>Path : %s</h1></body></html>" % (self.path, self.path)
            self.wfile.write(msg.encode())
            return
            #path="/index.html"
        
        mime_type = 'text/html'
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
        else:
            print("Type not found for %s" % path)
            self.send_error(404,'File Not Found: %s' % path)
            return
        
        try:
            docpath = r"C:\mydir"
            f = open(docpath + sep + path, 'rb') # curdir = '.' can be used (ou getcwd())
            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def server_function(host, port, handler):
    #with HTTPServer((Host, Port), Handler) as httpd: # with ne marche pas sur le server
    print("Creating HTTP Request Handler...")
    httpd = HTTPServer((host, port), handler)
    print(time.asctime(), "Server Starts - %s:%s" % (host, port))
    try:
        print("Serving...")
        httpd.serve_forever()
    except KeyboardInterrupt: # not needed for server mode
        pass

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    mode = 'HTML' # 'CGI'
    Host = socket.gethostbyname(socket.gethostname())
    print("Host : ", Host)
    Port = 8012
    print("Port : ", Port)
    if mode == 'CGI':
        Handler = CGIHTTPRequestHandler
        Handler.cgi_directories = ['/'] # very important
    else:
        Handler = MyRequestHandler
    print("Creating thread...")
    a = threading.Thread(None, server_function, "ServerThread", (Host, Port, Handler))
    print("Starting thread...")
    a.start()

    #with HTTPServer((Host, Port), Handler) as httpd:
    #    print(time.asctime(), "Server Starts - %s:%s" % (Host, Port))
    #    print("Listening on port: ", Port)
    #    try:
    #        httpd.serve_forever()
    #    except KeyboardInterrupt:
    #        pass
            
