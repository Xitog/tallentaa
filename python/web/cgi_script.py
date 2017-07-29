import cgi
import cgitb

cgitb.enable()                      # Detailed error reporting

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

print("<TITLE>CGI script output</TITLE>")
print("<H1>This is my first CGI script</H1>")
print("Hello, world!")
