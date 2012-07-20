#!/usr/bin/ruby

require "mots"
require "cgi"

b = WordList.load("base.data")

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
'''

# nouveau protocole mobile
if cgi.keys.include?('wcat') then
    if cgi['wcat'] == 'w' then
        puts '<h1>' + cgi['w'] + '</h1>'
    elsif cgi['wcat'] == 'a' then
    elsif cgi['wcat'] == 'c' then
    end
end

puts '<p>Filters: <a href="front.rb">tous</a> |'
for c in b.cats do
    puts  '<a href="front.rb?cat=' + c + '">' + c + '</a>'
    if c != b.cats[-1] then puts ' | ' end
end
puts '</p>'
puts   '<table>'

i = 0
for w in b.words do
    if !cgi.keys.include?('cat') or cgi['cat'] == 'none' or cgi['cat'] == w.cat then
        puts '<tr><td>' + w.val + '</td><td>' + w.kind + '</td><td>' + w.subkind + '</td><td>' + w.cat + '</td></tr>'
        i+=1
    end
end

puts """</table>
<p>#{i} mots</p>
</div>
</body>
</html>
"""
