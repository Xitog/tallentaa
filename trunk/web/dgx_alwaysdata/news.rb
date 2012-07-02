#!/usr/bin/ruby

require 'cgi'

cgi = CGI.new
#puts cgi.header
puts "Content-Type: text/html; charset=utf-8\n\n"
puts

#puts "Bonjour"
#for p in cgi.keys do
#   puts "#{p}:#{cgi[p]}"
#end

if cgi.keys.include?('news') then
    if cgi['news'] == '1' then 
        puts "<h1>Bienvenue</h1>"
        puts "<p>Bienvenue dans ce nouveau site web, doté d'un design clair et léger, inspiré par le style de la page <a href=\"http://en.wikipedia.org/wiki/Palatino\">Palatino</a> de Wikipédia. Utilisant des technologies modernes comme AJAX avec la bibliothèque JQuery, ce site a pour but d'être une vitrine sur mes activités. Visiteur d'un jour ou de toujours, en espérant que vous trouverez ici des choses qui vous serons utiles, je vous salue !</p>"
    else
        puts "<h1>Hello 2</h1>"
        puts news
    end
else
    puts "<h1>Hello no news</h1>"
end
