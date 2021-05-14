#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgitb
cgitb.enable()

print "Content-Type: text/html;charset=utf-8\n\n"

f = file('./content/content.html', 'r')
s = f.read()
contents = s.split('__SPLIT__')

print '<!DOCTYPE html>'
print '<html lang="en">'

import cgi
form = cgi.FieldStorage()
if 'content' in form:
    corr = { 
        'prenoms' : ('./content/prenoms.html', 'Prénoms'),
        'langues' : ('./content/notes_langues.html', 'Langues & Langages'),
        'guide_rts' : ('./content/guide_rts.html', 'Guide RTS'),
        'projet_rts' : ('./content/projet_rts.html', 'Projet RTS'),
    }
    
    if form['content'] in corr:
        f = file(corr[form['content']], 'r')
        main_content = f.read()
        titre = titles[form['content']]
    else:
        main_content = '<h1>' + form['content'].value + '</h1>'
        titre = 'Ran'
else:
    main_content = contents[2] # default main content
    titre = 'Ran'

print contents[0].replace('__TITLE__', titre) # head

print '<body>'
print '<div id="main" class="container">'
print contents[1] # menu
print main_content
print contents[3] # footer
print '</div>'
print contents[4] # scripts
print '</body>'
print '</html>'
