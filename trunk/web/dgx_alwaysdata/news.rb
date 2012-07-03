#!/usr/bin/ruby

require 'cgi'

cgi = CGI.new
#puts cgi.header
puts "Content-Type: text/html; charset=utf-8\n\n"
puts

f = File.new('news.data', 'r')
news = f.readlines

if news == nil then
  puts "! No news found"
end

#puts "Bonjour"
#for p in cgi.keys do
#   puts "#{p}:#{cgi[p]}"
#end

if cgi.keys.include?('news') then

    if cgi['news'] == 'last' then
        nb = news.length
    else
        nb = Integer(cgi['news'])
    end
    
    #puts ">>> #{cgi['news']}"
    #puts ">>> #{nb}"
    #puts ">>> #{news.length}"
    #puts news[nb-1]

    e = news[nb-1].split(':')
    
    #puts ">>> #{e}"

    puts "<h2>#{e[0].strip!}</h2>"
    puts "<p class=\"first\">#{e[1].gsub("ZX", "http\://")}</p>"
    if nb > 1 and news.length > 1 and nb < news.length then
        puts "<table width=\"100%\"><tr><td align=\"left\"><a href=\"#get_#{nb-1}\">&lt;&lt;</a></td><td align=\"right\"><a href=\"#get_#{nb+1}\">&gt;&gt;</a></td></tr></table>"
    elsif nb < news.length then
        puts "<table width=\"100%\"><tr><td align=\"left\"><a href=\"#get_#{nb+1}\">&lt;&lt;</a></td><td>&nbsp;</td></tr></table>"
    elsif nb > 1 and news.length > 1 then
        puts "<table width=\"100%\"><tr><td>&nbsp;</td><td align=\"right\"><a href=\"#get_#{nb-1}\">&gt;&gt;</a></td></tr></table>"
    end

    #if cgi['news'] == '1' then 
    #    puts "<h2>Bienvenue</h2>"
    #    puts "<p>Bienvenue dans ce nouveau site web, doté d'un design clair et léger, inspiré par le style de la page <a href=\"http://en.wikipedia.org/wiki/Palatino\">Palatino</a> de Wikipédia. Utilisant des technologies comme AJAX avec la bibliothèque JQuery, ce site a pour but d'être une vitrine de mes activités. Visiteur d'un jour ou de toujours, en espérant que vous trouverez ici des choses qui vous serons utiles, je vous salue !</p>"
    #else
    #    puts "<h1>Hello 2</h1>"
    #    puts news
    #end
else
    puts "<h1>Hello no news</h1>"
end
