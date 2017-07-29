from http.server import CGIHTTPRequestHandler, HTTPServer
import socketserver
import sys
import os
import os.path

PORT = 8013

# 16h47 ok

#class HTTPHandler(http.server.SimpleHTTPRequestHandler):
class HTTPHandler(CGIHTTPRequestHandler):
    
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
            else:
                f = open(target, 'r')
                content = f.read()
                f.close()
        # Basic HTML return
        else:
            content = "<html><body><h1>Hello World</h1></body></html>"
        content = content.encode('utf-8')
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(content))
        self.end_headers()
        self.wfile.write(content)

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

