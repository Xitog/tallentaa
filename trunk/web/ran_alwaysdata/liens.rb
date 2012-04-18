#!/usr/bin/ruby

f = File.open('data.txt', 'r')
lines = f.readlines
#lines = "pipo"

puts "Content-type: text/html"
puts
puts '''<!DOCTYPE html>
<html>
<head>
  <title>Links</title>
  <meta charset="utf-8">
</head>
<body>
  <center>
    <form method="get" action="http://www.google.com/search">
      <input type="text"   name="q" size="31" maxlength="255" value="" />
      <input type="submit" value="Google Search" />
      <input type="radio"  name="sitesearch" value="" /> The Web
      <input type="radio"  name="sitesearch" value="ran.alwaysdata.net" checked /> Local search<br />
    </form>
  </center>
  <table>
'''

old = ''
for line in lines do
    #puts line.chomp
    before, after = line.split('http://')
    if before != nil and after != nil
        before.strip!
        tags = before.split(',')
        for t in tags do
            t.strip!
        end
        # separator
        if tags.length > 0 and tags[0] != old then
            puts '<tr><td>&nbsp;</td><td>&nbsp;</td></tr>'
            old = tags[0]
        end
        after.strip!
        puts '<tr><td>' + before + '</td><td><a href="http://' + after + '">http://' + after + '</a></td></tr>'
    end
end

puts '''</table>
</body>
</html>
'''

