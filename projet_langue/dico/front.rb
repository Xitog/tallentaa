#!/usr/bin/ruby

require "mots"
require "cgi"

b = Base.new()

cgi = CGI.new

puts "Content-type: text/html"
puts
puts '''<!DOCTYPE html>
<html>
<head>
    <title>Mots</title>
    <meta charset="utf-8">
    <style type="text/css">
        <!--
        body {background-color: #111111; color: #EEEEEE;}
         
        tbody tr:nth-child(odd) { background-color: #222222; }
         
        tbody tr:nth-child(2n) { background-color: #111111; }
         
        a { color: #00FF00; }
         
        a:hover {
        background-color: #FF0000;
        color: White;
        }
         
        p { border-top: 1px solid red;
        border-bottom: 1px solid red;
        color: red;
        text-align: center;
        }
         
        div { width: 80%;
        margin: auto;
        background-color: #010101;
        border: 1px solid #FF0000;
        }
         
        table { width: 98%;
        margin: auto;
        }
         
        center {
        padding-top: 3px;
        }
        
        -->
    </style>
</head>
<body>
    <div>
        <center>
            <form method="get" action="http://www.google.com/search">
                <input type="text" name="q" size="31" maxlength="255" value="" />
                <input type="submit" value="Google Search" />
                <input type="radio" name="sitesearch" value="" /> The Web
                <input type="radio" name="sitesearch" value="ran.alwaysdata.net" checked /> Local search<br />
            </form>
        </center>
        <p>Filters: <a href="liens.rb">none</a> | <a href="liens.rb?best">***</a></p>
        <table>
'''

for w in b.words do
    puts '<tr><td>' + w.base + '</td><td>' + w.kind + '</td><td>' + w.cat + '</td></tr>'
end

puts """</table>
<p>#{b.words.length} links</p>
</div>
</body>
</html>
"""
