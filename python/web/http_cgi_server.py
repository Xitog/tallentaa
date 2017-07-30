from http.server import CGIHTTPRequestHandler, HTTPServer
import socketserver
import sys
import os
import os.path

PORT = 8013

# 16h47 ok

#class HTTPHandler(http.server.SimpleHTTPRequestHandler):
class HTTPHandler(CGIHTTPRequestHandler):

    def serve(self, content, content_type):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Length", str(content))
        self.end_headers()
        self.wfile.write(content)
        
    def serve_default(self):
        "Basic HTML return"
        content = "<html><body><h1>Hello World</h1></body></html>"
        typ = 'text/html'
        encoding = sys.getfilesystemencoding()
        content = content.encode(encoding)
        content_type = f"{typ}; charset={encoding}"
        self.serve(content, content_type)

    def serve_file(self, target):
        ext = os.path.splitext(target)[1]
        if ext in ['.html', '.css', '.js', '.htm']:
            if ext == '.html':
                typ = 'text/html'
            elif ext == '.css':
                typ = 'text/css'
            elif ext == '.js':
                typ = 'application/javascript'
            f = open(target, 'r')
            content = f.read()
            f.close()
            encoding = sys.getfilesystemencoding() # 'utf-8'
            content = content.encode(encoding)
            content_type = f"{typ}; charset={encoding}"
            self.serve(content, content_type)
        elif ext in ['.jpeg', '.jpg', '.png', '.gif', '.ico']:
            if ext == '.png':
                typ = 'image/png'
            elif ext == '.gif':
                typ = 'image/gif'
            elif ext == '.ico':
                typ = 'image/x-icon'
            f = open(target, 'rb')
            content = f.read()
            f.close()
            content_type = f"{typ}"
            self.serve(content, content_type)
    
    def do_GET(self):
        current_dir = os.getcwd()
        target = os.path.join(current_dir, self.path[1:])
        # Debug
        print('Path:', self.path)
        print('Could be:', target)
        # File requested?
        if os.path.isfile(target):
            # CGI script requested?
            if os.path.splitext(target)[1] == '.py':
                CGIHTTPRequestHandler.do_GET(self)
                return
            # no CGI
            else:
                self.serve_file(target)
        # no file
        else:
            self.serve_default()

handler = HTTPHandler
handler.cgi_directories = ["/"]

httpd = HTTPServer(("", PORT), handler)
#old: httpd = socketserver.TCPServer(("", PORT), handler)

print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()

