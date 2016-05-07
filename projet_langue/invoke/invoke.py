# ------------------------------------------------------------------------------
# Local version of Invoke
#------------------------------------------------------------------------------
#
# Handle the database of words and translations.
#
#------------------------------------------------------------------------------
#
# Commands
#  Main commands
#    help - print this help
#    exit - exit
#    create - recreate the database entirely
#    count - count the number of returned results
#    select - select all the verbs for the default language in the default order
#    select ... - select all the verbs for a given language : fr
#    stats - make various stats over the database
#    conjugate ... - conjugate the given verb (only ion French)
#    render - render the list of verbs
#  Parameter settings
#    order ... - set the order of the returned results
#    lang ... - set the lang of the returned results (for select and trans)
#    lang - get the current lang of the returned results and translation
#    to ... - set the translation of the returned results (for trans)
#    auto - switch to wait for a key or not before executing the command
#    file - switch to conjugate a verb in a file instead of displaying it
#    html - switch to output in html in the file instead of plain text
#    reset - reset the file where the conjugated verbs are stored
#    close - write the footer in the file where the conjugated verbs are stored
# Available languages are : fr, en, it, eo, de
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Import
#------------------------------------------------------------------------------

import os
import sys
import sqlite3
import unicodedata
import invoke_data

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------

def check_content_verbs(content):
    # Test de l'unicité des ids et des bases
    verbes_id = []
    verbes_base_lang = {}
    error = False
    for cc in content:
        idv = cc[0]
        if idv in verbes_id:
            print("ERROR : id 2x : " + str(idv))
            error = True
        else:
            verbes_id.append(idv)
        base = cc[2]
        if base in verbes_base_lang and verbes_base_lang[base] == cc[1]: # same base and lang
            print("ERROR : base 2x : " + base)
            error = True
        else:
            verbes_base_lang[base] = cc[1] # 'dire' : 'fr' ou 'dire' : 'it'
    if error:
        print("Errors have been found.")
        exit()
    return verbes_id


def check_content_trans(content, verbes_id):
    # Tests Foreign Key
    error = False
    for cc in content:
        de = cc[1]
        vers = cc[2]
        if de not in verbes_id or vers not in verbes_id:
            if de not in verbes_id:
                print("Unknown DE id : " + str(de) + " from " + str(cc))
                error = True
            if vers not in verbes_id:
                print("Unknown VERS id : " + str(vers) + " from " + str(cc))
                error = True
    if error:
        print("Errors have been found.")
        exit()


def create():
    try:
        os.remove('example.db')
    except FileNotFoundError:
        print("FileNotFound")

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Tables creation

    c.execute("CREATE TABLE IF NOT EXISTS voc_verbs ( id int(11) NOT NULL, lang varchar(2) NOT NULL, base varchar(50) NOT NULL, surtype varchar(30) NOT NULL, lvl int(11) DEFAULT '1', PRIMARY KEY (`id`) ) ")
    c.execute("CREATE TABLE IF NOT EXISTS voc_translate ( id int(11) NOT NULL, de int(11) NOT NULL, vers int(11) NOT NULL, sens varchar(100) DEFAULT NULL, usage varchar(100) DEFAULT NULL, PRIMARY KEY (`id`) ) ")
    c.execute("CREATE TABLE IF NOT EXISTS voc_verbs_en ( id int(11) NOT NULL, base varchar(50) NOT NULL, pret varchar(50) NOT NULL, part varchar(50) NOT NULL )")
    
    # Tables filling

    content = invoke_data.get_verbs()
    verbes_id = check_content_verbs(content)
    c.executemany('INSERT INTO voc_verbs VALUES (?,?,?,?,?)', content)
    
    content_verbs_en = invoke_data.get_irregular_verbs()
    irr_not_found = 0
    for cc in content_verbs_en:
        found = False
        for v in content:
            if cc[1] == v[2] and v[1] == 'en':
                # le verbe est dans la base et dans celle des irréguliers
                found = True
                break
        if not found:        
            # on a un irrégulier qui n'est pas dans notre base
            print(cc[1])
            irr_not_found += 1
    print("i Irregulars not found in our base :", irr_not_found)
    
    c.executemany('INSERT INTO voc_verbs_en VALUES (?,?,?,?)', content_verbs_en)

    content = invoke_data.get_traductions()
    
    check_content_trans(content, verbes_id)
    
    for i in content:
        if len(i) != 5:
            print(i)
            exit()
    
    try:
        c.executemany('INSERT INTO voc_translate VALUES (?, ?, ?, ?, ?)', content)
    except sqlite3.ProgrammingError as e:
        print('! Erreur : ' + str(e))
    
    conn.commit()

    conn.close()

    # ---

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    #c.execute("SELECT * FROM voc_verbs")
    #r = c.fetchone()
    f = open('results.txt', mode='w', encoding='utf-8')

    f.write("------------------------------------------------------------------------\n")
    f.write("Toutes les traductions\n")
    f.write("------------------------------------------------------------------------\n")
    i = 0
    for row in c.execute("SELECT fr.base, en.base, t.sens FROM voc_verbs as fr, voc_verbs as en, voc_translate as t WHERE fr.id = t.de AND en.id = t.vers AND fr.lang = 'fr' AND en.lang = 'en' ORDER BY fr.lang, fr.base"):
        i += 1
        if row[2] is not None:
            f.write(str(i) + ". " + row[0] + " --> to " + row[1] + " avec le sens de : " + row[2] +"\n") #'::'.join(row))
        else:
            f.write(str(i) + ". " + row[0] + " --> to " + row[1] + "\n") #'::'.join(row))

    f.write("\n\n\n")
    f.write("------------------------------------------------------------------------\n")
    f.write("Tous les verbes français\n")
    f.write("------------------------------------------------------------------------\n")
    i = 0
    for row in c.execute("SELECT fr.id, fr.base FROM voc_verbs as fr WHERE fr.lang = 'fr' ORDER BY fr.lang, fr.base"):
        i += 1
        f.write(str(i) + ". #" + str(row[0]) + " " + row[1] + "\n")

    f.write("\n\n\n")
    f.write("------------------------------------------------------------------------\n")
    f.write("Verbes non traduits\n")
    f.write("------------------------------------------------------------------------\n")
    i = 0
    for row in c.execute("SELECT fr.id, fr.base FROM voc_verbs as fr WHERE fr.lang = 'fr' AND fr.id NOT IN (SELECT t.de FROM voc_translate as t) ORDER BY fr.lang, fr.base"):
        i += 1
        f.write(str(i) + ". #" + str(row[0]) + " " + row[1] + "\n")

    from time import gmtime, strftime
    s = strftime("%Y-%m-%d %H:%M:%S") #, gmtime())
    f.write("\n\nLast edit on " + s)

    f.close()


def exec_stat(p_auto=False, p_debug=False):
    p_conn = sqlite3.connect('example.db')
    p_cursor = p_conn.cursor()
    dic = {'fr': 'French', 'en': 'English', 'it': 'Italian', 'eo': 'Esperanto', 'de' : 'German'}
    total = 0
    for lang in dic:
        p_string = "SELECT count(*), surtype FROM voc_verbs WHERE lang = '" + lang + "' GROUP BY surtype"
        if p_debug:
            print("% Executing : " + p_string)
        if not p_auto:
            print("% Press a key to continue")
            input()
        # res = p_cursor.execute(p_string)
        # line = res.fetchone()
        count_lang = 0
        for p_row in p_cursor.execute(p_string):
            print("i   " + dic[lang] + " " + p_row[1] + " : " + str(p_row[0]))
            count_lang += p_row[0]
        total += count_lang
        print("i " + dic[lang] + " total words : " + str(count_lang))
    print("i Total = " + str(total))
    p_cursor.close()
    p_conn.close()


def get_all_verbs_en(): # fetch irregular
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    request = "SELECT id, base, pret, part FROM voc_verbs_en"
    results = {}
    for row in cursor.execute(request):
        results[row[1]] = { 'id' : row[0], 'base' : row[1], 'pret' : row[2], 'part' : row[3] }
    return results


def get_all_verbs_full(p_lang = 'en', p_to = 'fr'): # all verbs, with translations and irregular forms
    p_conn = sqlite3.connect('example.db')
    p_cursor = p_conn.cursor()
    p_order = p_lang + '.base'
    nb = 0                           # 0                    1                    2                      3                 4                  5     6       7     8
    p_string = ("SELECT " + p_lang + ".id, " + p_lang + ".base, " + p_lang + ".surtype, " + p_lang + ".lvl, " + p_to + ".base, " + p_to + ".id, t.sens, t.id, t.usage " +
                "FROM voc_verbs as " +
                p_lang + ", voc_verbs as " + p_to + ", voc_translate as t WHERE " + p_lang + ".id = t.de AND " +
                p_to + ".id = t.vers AND " + p_lang + ".lang = '" + p_lang + "' AND " + p_to + ".lang = '" + p_to + "' AND " + p_lang + ".surtype = 'verb'" +
                " ORDER BY " + p_order)
    nb = 0
    verbs = []
    actual = None
    irregulars = get_all_verbs_en()
    #print(p_string)
    for p_row in p_cursor.execute(p_string):
        if actual is None or actual['id'] != p_row[0]:
            nb += 1
            if actual is None:
                actual = { 'nb' : nb }
            else:
                # gestion à particules
                if len(actual['base'].split(' ')) > 1:
                    actual['root_base'] = actual['base'].split(' ')[0]
                    actual['particle'] = ' ' + actual['base'].split(' ')[1]
                else:
                    actual['root_base'] = actual['base']
                    actual['particle'] = ''
                # gestion des prétérits
                if actual['root_base'] in irregulars:
                    actual['pret'] = irregulars[actual['root_base']]['pret']
                    actual['part'] = irregulars[actual['root_base']]['part']
                    actual['irregular'] = True
                else:
                    actual['irregular'] = False
                    # Building of preterit & past participe
                    if actual['root_base'][-1] == 'e':                              # change => changed
                        actual['part'] = actual['root_base'] + 'd'
                    elif actual['root_base'][-1] == 'y':
                        if actual['root_base'][-2] in ['a', 'e', 'i', 'o', 'u']:    # base (stay => stayed)
                            actual['part'] = actual['root_base'] + "ed"
                        else:
                            actual['part'] = actual['root_base'][0:-1] + "ied"      # carry => carried
                    elif actual['root_base'][-1] not in ['a', 'i', 'o', 'u']:       
                        if actual['root_base'][-2] in ['a', 'u', 'i']:              
                            if actual['root_base'][-3] in ['a', 'e', 'o', 'u'] or len(actual['root_base']) > 4:     # base (cook => cooked, wait => waited) et le cas visit => visited
                                actual['part'] = actual['root_base'] + 'ed'                                         # au lieu de la len faire juste que -3 ne soit pas i ?
                            else:                                                   # chat => chatted
                                actual['part'] = actual['root_base'] + actual['root_base'][-1] + 'ed'
                        else:
                            actual['part'] = actual['root_base'] + 'ed'             # base
                    else:
                        actual['part'] = actual['root_base'] + 'ed'                 # base
                    
                    actual['pret'] = actual['part']
                verbs.append(actual)
                actual = { 'nb' : nb }
            #print('verbe : ' + p_row[1])
            actual['id'] = p_row[0]
            actual['base'] = p_row[1]
            actual['surtype'] = p_row[2]
            actual['lvl'] = p_row[3]
            actual['trans'] = {}
            # attention parfois p_row 6 ou 8 peuvent-être None
            actual['trans'][p_row[5]] = { 'base' : p_row[4], 'sens' : p_row[6], 'usage' : p_row[8] }
        elif actual is not None:
            actual['trans'][p_row[5]] = { 'base' : p_row[4], 'sens' : p_row[6], 'usage' : p_row[8] }
    if actual is not None:
        if len(actual['base'].split(' ')) > 1:
            actual['root_base'] = actual['base'].split(' ')[0]
            actual['particle'] = ' ' + actual['base'].split(' ')[1]
        else:
            actual['root_base'] = actual['base']
            actual['particle'] = ''
        if actual['root_base'] in irregulars:
            actual['pret'] = irregulars[actual['root_base']]['pret']
            actual['part'] = irregulars[actual['root_base']]['part']
            actual['irregular'] = True
        else:
            # Building of preterit & past participe !!! DUPLICATE CODE HERE NOT UPDATED FROM UP THERE
            actual['irregular'] = False
            if actual['root_base'][-1] != 'e' and actual['root_base'][-1] != 'y':
                actual['part'] = actual['root_base'] + 'ed'
            elif actual['root_base'][-1] == 'e':
                actual['part'] = actual['root_base'] + 'd'
            elif actual['root_base'][-1] == 'y':
                actual['part'] = actual['root_base'][0:-1] + "ied"
            actual['pret'] = actual['part']
        
        verbs.append(actual)
    return verbs


#def pretty_print(verbs):
#    print(len(verbs))
#v = get_all_verbs()
#pretty_print(v)

def exec_cmd(p_main, p_lang, p_order='', p_auto=False, p_to=None, p_debug=False, display=True):
    if p_order == '':
        p_order =  p_lang + ".lang, " + p_lang + ".base"
    
    p_conn = sqlite3.connect('example.db')
    p_cursor = p_conn.cursor()
    nb = 0
    if p_main in ['select', 'trans']:
        cnt = False
    elif p_main in ['count']:
        cnt = True
    else:
        print("! Command unknown : ", p_main)
        return -1
    if p_main == 'select' or p_main == 'count':
        p_string = ("SELECT " + p_lang + ".id, " + p_lang + ".base, " + p_lang + ".surtype, " + p_lang + ".lvl" + " FROM voc_verbs as " + p_lang +
                    " WHERE " + p_lang + ".lang = '" + p_lang + "' ORDER BY " + p_order)
    elif p_main == 'trans':
        p_string = ("SELECT " + p_lang + ".id, " + p_lang + ".base, " + p_to + ".base, " + p_to + ".id, t.sens, t.id " +
                    "FROM voc_verbs as " +
                    p_lang + ", voc_verbs as " + p_to + ", voc_translate as t WHERE " + p_lang + ".id = t.de AND " +
                    p_to + ".id = t.vers AND " + p_lang + ".lang = '" + p_lang + "' AND " + p_to + ".lang = '" + p_to +
                    "' ORDER BY " + p_order)
    if p_debug:
        print("% Executing : " + p_string)
    if display:
        if not p_auto:
            print("% Press a key to continue")
            input()
        for p_row in p_cursor.execute(p_string):
            if not cnt: # si on compte pas, on affiche tout
                if p_main == 'select':
                    try:
                        print("#" + str(p_row[0]) + "  " + p_row[1] + " (" + p_row[2] + ") [" + str(p_row[3]) + "]")
                    except UnicodeEncodeError as e:
                        word = p_row[1]
                        word_modified = ''
                        for letter in word:
                            if letter == "\u0153":
                                word_modified += 'oe'
                            else:
                                word_modified += letter
                            #print('%04x' % ord(letter))
                        print("#" + str(p_row[0]) + "  " + word_modified + " (" + p_row[2] + ") [" + str(p_row[3]) + "]")
                elif p_main == 'trans':
                    sys.stdout.write("#" + str(p_row[5]) + "  " + p_row[1] + " (" + str(p_row[0]) + ")")
                    if p_row[4] is not None:
                        sys.stdout.write(" --> to " + p_row[2] + " (" + str(p_row[3]) + ") avec le sens de : " + p_row[4] +
                                         "\n")
                    else:
                        sys.stdout.write(" --> to " + p_row[2] + " (" + str(p_row[3]) + ")\n")
            nb += 1
    else: # ne marche que pour select
        verbs = []
        for p_row in p_cursor.execute(p_string):
            v = {}
            v['id'] = p_row[0]
            v['base'] = p_row[1]
            v['surtype'] = p_row[2]
            v['lvl'] = p_row[3]
            verbs.append(v)
    print("i Number of returned results = " + str(nb))    
    p_cursor.close()
    p_conn.close()
    if display:
        return nb
    else:
        return verbs

# Conjugate : new from 2/11/2015
# Il faudrait faire une option qui génère tout cela dans un fichier texte plutôt qu'en sortie console.
# Aucun test, cela ne marche que pour les verbes du 1er groupe se conjuguant avec avoir.
def conjugate(verb, lang, onfile=False, html=False):
    if lang not in ['fr', 'en']:
        print('Unknwon conjugaison for', lang)
        return
    if verb == 'all' and lang == 'en':
        # make book
        r = get_all_verbs_full()
        #print("To do for", len(r))
        nb = 0
        for v in r:
            if v['surtype'] == 'verb':
                nb += 1
                conjugate_en(v['base'], onfile, html, v, nb)
            else:
                print(v['surtype'])
        print('i Conjugaison done for', len(r), 'verbs')
    elif verb == 'all':
        r = exec_cmd('select', lang, '', False, None, False, False)
        # filter on verb
        nb = 0
        for v in r:
            if v['surtype'] == 'verb':
                if lang == 'fr':
                    conjugate_fr(v['base'], onfile, html)
                elif lang == 'en':
                    conjugate_en(v['base'], onfile, html)
                nb += 1
        print('i Conjugaison done for', nb, 'verbs')
    else:
        if lang == 'fr':
            conjugate_fr(verb, onfile, html)
        elif lang == 'en':
            conjugate_en(verb, onfile, html)

def header_en():
    f = open('output.html', mode='w', encoding='utf-8')
    
    html = open('invoke_chapters.html', mode='r', encoding='utf-8')
    html_content = html.read()
    html_parts = html_content.split('<!-- SPLIT HERE -->')
    
    verbs_en = get_all_verbs_full('en', 'fr')
    
    f.write(html_parts[0].replace('#NB#', str(len(verbs_en))))
    for v in verbs_en:
        f.write('<h3><a href="#' + str(v['id']) + '">' + str(v['nb']) + '. ' + v['root_base'] + v['particle'] + ' &nbsp;(' + v['pret'] + v['particle'] + ', ' + v['part'] + v['particle'] + ')</a>')
        if v['irregular']:
            f.write(' <b>*</b>')
        f.write('</h3>\n')
    f.write('\n\n')
    f.write('<p>Les verbes avec une ast&eacute;risque <b>*</b> sont irr&eacute;guliers.</p>')
    f.write('<mbp:pagebreak />')
    
    verbs_fr = get_all_verbs_full('fr', 'en')
    
    f.write('<h2 id="liste_fr_en">Les ' + str(len(verbs_en)) + ' verbes fondamentaux anglais à partir de leurs traductions en français</h2>')
    for v in verbs_fr:
        f.write('<h3>' + str(v['nb']) + '. ' + v['root_base'] + v['particle'] + ' : ')
        trans = ''
        nbt = 0
        for t in v['trans']:
            if nbt == 0:
                trans = '<a href="#' + str(t) + '">' + v['trans'][t]['base'] + '</a>'
                nbt += 1
            else:
                trans = trans + ', ' + '<a href="#' + str(t) + '">' + v['trans'][t]['base'] + '</a>'
            for vv in verbs_en:
                if vv['id'] == t:
                    if vv['irregular']:
                        trans = trans + ' <b>*</b>'
                    break
        f.write(trans + '</h3>\n')
    f.write('<p>Les verbes avec une ast&eacute;risque <b>*</b> sont irr&eacute;guliers.</p>')
    f.write('<mbp:pagebreak />')
    
    f.write(html_parts[1].replace('#NB#', str(len(verbs_en))))
    
    f.close()


def footer_en():
    f = open('output.html', mode='a', encoding='utf-8')
    
    html = open('invoke_chapters.html', mode='r', encoding='utf-8')
    html_content = html.read()
    html_parts = html_content.split('<!-- SPLIT HERE -->')
    
    verbs_en = get_all_verbs_full('en', 'fr')
    f.write(html_parts[2].replace('#NB#', str(len(verbs_en))))
    
    f.close()
    

def conjugate_en(verb, onfile=False, html=False, info=None, nb=None):
    if not onfile or not html or nb is None or info is None:
        print("i This function works only with onfile and html set at true")
        return

    f = open('output.html', mode='a', encoding='utf-8')
    pronoms = ['I', 'you', 'she, he, it', 'we', 'you', 'they']
    root = info['root_base']
    particle = info['particle']
    pret = info['pret']
    part = info['part']
    
    # Present 3e
    if root[-1] == 'y' and root[-2] in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']:
        pres3 = root[0:-1] + "ies"
    elif root[-1] in ['s', 'x', 'z', 'o'] or root[-2:] in ['ch', 'sh']:
        pres3 = root + '<b class="s">es</b>'
    else:
        pres3 = root + '<b class="s">s</b>'

    # ing
    if root[-1] == 'e':
        ing = root[0:-1] + 'ing'
    elif root[-1] in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z'] and root[-2] in ['a', 'e', 'i', 'o', 'u']:
        if root[-2] == 'a' and root[-3] == 'e':
            ing = root + 'ing'
        elif root[-2] == 'o' and root[-3] == 'o':
            ing = root + 'ing'
        else:
            ing = root + root[-1] + 'ing'
    else:
        ing = root + 'ing'
    
    f.write('<h2 id="' + str(info['id']) + '">' + str(nb) + '. ' + root + particle + ' &nbsp;&nbsp;(' + pret + particle + ', ' + part + particle + ')</h2>\n')
    f.write('<p><b>Sens et traduction</b> : <ul>\n')
    for t in info['trans']:
        if info['trans'][t]['usage'] is not None:
            xs = info['trans'][t]['usage'].split(',')
            for x in xs:
                f.write('\t<li>' + x + '</li>\n')
        elif info['trans'][t]['sens'] is not None:
            f.write('\t<li>' + info['trans'][t]['base'] + ' (' + info['trans'][t]['sens'] + ')</li>\n')
        else:
            f.write('\t<li>' + info['trans'][t]['base'] + '</li>\n')
    f.write('</ul></p>\n')
    
    #f.write('<p><b>Base verbale</b> : ' + root + '</p>\n')
    f.write('<p><b>Infinitif</b> : <b>to <b class="present">' + root + '</b></b></p>\n')
    f.write('<p><b>Participe passé</b> : <b class="pp">' + part + '</b></p>\n')
    f.write('<p><b>Participe présent</b> : <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('<p><b>Voix passive</b> : <b>were ' + part + '</b> (1ère et 3e pers. sing. : <b>was ' + part + '</b>)</p>\n')
    
    f.write('<h3>Indicatif</h3>\n')
    
    f.write('<div class="simple">\n')
    f.write('<p><b>Présent simple</b> :<ul>\n')
    f.write('\t<li>forme <b>affirmative</b> : <b class="present">' + root + particle + '</b> (3e pers. sing. : <b class="present">' + pres3 + particle + '</b>)</li>\n')
    f.write('\t<li>forme <b>négative</b> : <b class="present">do not ' + root + '</b> (3e pers. sing. : <b class="present">do</b><b class="s">es</b><b class="present"> not ' + root + particle + ')</b></li>\n')
    f.write('</ul></p>\n')
    f.write('<p><b>Passé simple (ou prétérit)</b> :<ul>\n')
    f.write('\t<li>forme <b>affirmative</b> : <b class="past">' + pret + particle + '</b></li>\n')
    f.write('\t<li>forme <b>négative</b> : <b class="past">did not ' + root + particle + '</b></li>\n')
    f.write('</ul></p>\n')
    f.write('<p><b>Futur simple</b> : <b class="future">will</b> <b>(not)</b> <b class="future">' + root + particle + '</b></p>\n')
    f.write('</div>\n')
    
    f.write('<div class="pp">\n')
    f.write('<p><b>Présent parfait</b> : <b class="present">have</b> <b>(not)</b> <b class="pp">' + part + particle + '</b> (3e pers. sing. : <b class="present">' + 'ha</b><b class="s">s</b> <b>(not)</b> <b class="pp">' + part + particle + '</b>)</p>\n')
    f.write('<p><b>Passé parfait</b> : <b class="past">had</b> <b>(not)</b> <b class="pp">' + part + particle + '</b></p>\n')
    f.write('<p><b>Futur parfait</b> : <b class="future">will</b> <b>(not)</b> <b class="future">have</b> <b class="pp">' + part + particle + '</b></p>\n')
    f.write('</div>\n')
    
    f.write('<div class="ing">\n')
    f.write('<p><b>Présent continu</b> : <b class="present">are</b> <b>(not)</b> <b class="ing">' + ing + particle +  '</b> (1ère et 3e pers. sing. : <b class="present">is</b> <b>(not)</b> <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('<p><b>Passé continu</b> : <b class="past">were</b> <b>(not)</b> <b class="ing">' + ing + particle +  '</b> (1ère et 3e pers. sing. : <b class="past">was</b> <b>(not)</b> <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('<p><b>Futur continu</b> : <b class="future">will be</b> <b>(not)</b> <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('</div>\n')
    
    f.write('<div class="pp">\n')
    f.write('<div class="ing">\n')
    f.write('<p><b>Présent parfait continu</b> : <b class="present">have</b> <b>(not)</b> <b class="pp">been</b> <b class="ing">' + ing + particle + '</b> (3e pers. sing. : <b class="present">' + 'ha</b><b class="s">s</b> <b>(not)</b> <b class="pp">been</b> <b class="ing">' + ing + particle + '</b>)</p>\n')
    f.write('<p><b>Passé parfait continu</b> : <b class="past">had</b> <b>(not)</b> <b class="pp">been</b> <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('<p><b>Futur parfait continu</b> : <b class="future">will</b> <b>(not)</b> <b class="future">have</b> <b class="pp">been</b> <b class="ing">' + part + particle + '</b></p>\n')
    f.write('</div>\n')
    f.write('</div>\n')
    
    f.write('<h3>Conditionnel</h3>\n')
    f.write('<p><b>Présent</b> : <b class="cond">should/would</b> <b>(not)</b> <b class="present">' + root + particle + '</b></p>\n')
    f.write('<p><b>Passé</b> : <b class="cond">should/would</b> <b>(not)</b> <b class="cond">have</b> <b class="pp">' + part + particle + '</b></p>\n')
    
    f.write('<h3>Subjonctif</h3>\n')
    f.write('<p><b>Présent</b> : <b>(not)</b> <b class="present">' + root + particle + '</b> (à <u>toutes</u> les personnes)</p>\n')
    if root == 'be':
        f.write('<p><b>Passé</b> : <b>(not)</b> <b class="past">' + pret + particle + '</b> (à <u>toutes</u> les personnes)</p>\n')
    
    f.write('<h3>Impératif</h3>\n')
    f.write('<p><b>2e pers.</b> : <b>(do not)</b> <b class="present">' + root + particle + '</b>!</p>\n')
    f.write('<p><b>1e pers. du pluriel</b> (avec deux façons d\'exprimer la négation) : <b>(do not)</b> <b class="present">let</b> \'s <b>(not)</b> <b class="present">' + root + particle + '</b>!</p>\n')
    f.write('<p><b>3e pers.</b> (avec deux façons d\'exprimer la négation) : <b>(do not)</b> <b class="present">let</b> her/him/them <b>(not)</b> <b class="present">' + root + particle + '</b>!</p>\n')
    
    #f.write('<h3>Constructions avec auxilaires</h3>\n')
    #f.write('<p>Expression d\'une <b>potentialité</b> : may/might (not) <b class="present">' + root + particle + '</b></p>\n')
    #f.write('<p>Expression d\'une <b>autorisation</b> : may (not) <b class="present">' + root + particle + '</b></p>\n')
    #f.write('<p>Expression d\'un <b>doute</b>, d\'une <b>supposition</b> ou <b>atténuation polie</b> : should (not) <b class="present">' + root + particle + '</b></p>\n')
    
    f.write('<div class="retour"><b><a href="#tous_les_verbes">Retour à la liste des verbes</a></b></div>')
    f.write('<mbp:pagebreak />')
    
    f.close()


#------------------------------------------------------------------------------
# Basic Abstract Renderer (BAR)
#------------------------------------------------------------------------------

class Renderer:

    def __init__(self, tables):
        self.tables = tables
    
    def info(self):
        print('Number of tables:', len(tables))
        for key in tables:
            print('Key:', key, 'Number of elements:', len(tables[key]))

    def render(self, target):
        raise Exception('This is an abstract class.')

#------------------------------------------------------------------------------
# Simple tabular renderer for English, html
#------------------------------------------------------------------------------

class ConjugateTabularEn(Renderer):
    
    def header(self, f):
        f.write("""
<head>
    <style type="text/css">
        table {
            border: 1px solid rgb(91, 155, 213);
            border-collapse: collapse;
            width: 18cm;
            margin: auto;
            font-size: 18px;
            font-family: Calibri;
        }
        
        td.num {
            width: 1.5cm;
            text-align: center;
        }
        
        th {
            background: rgb(91, 155, 213);
            color: rgb(255, 255, 255);
            font-weight: bold;
        }
        
        tr:nth-child(odd) {
            background: rgb(242, 242, 242);
        }
        
        span.irr {
            font-weight: bold;
            color: rgb(10, 10, 100); //rgb(146, 208, 80);
        }
    </style>
</head>
        """)
    
    def render(self, target):
        
        verbs = self.tables['verbs']
        
        f = open(target, mode='w', encoding='utf-8')
        self.header(f)
        
        f.write('<table>\n')
        f.write('<tr><th>n°</th><th>Base verbale</th><th>Prétérit</th><th>Participe passé</th><th>Traduction(s)</th></tr>\n')
        nb = 1
        previous_base = None
        for v in verbs:
            verb = v['root_base'] + ' ' + v['particle']
            if v['irregular']:
                verb_display = '<span class="irr">' + verb + '</span>'
            else:
                verb_display = verb
            pret = v['pret'] if not v['irregular'] else '<span class="irr">' + v['pret'] + '</span>'
            part = v['part'] if not v['irregular'] else '<span class="irr">' + v['part'] + '</span>'
            trans = v['trans']
            if previous_base is None or previous_base != v['root_base']:
                f.write('<tr><td class="num">' + str(nb) + '</td><td>' + verb_display + '</td><td>' + pret + '</td><td>' + part + '</td>')
            else:
                f.write('<tr><td class="num">' + str(nb) + '</td><td> ' + verb_display + '</td><td></td><td></td>')
            i = 1
            for t in trans:
                if i == 1:
                    f.write('<td>to ' + verb + ' : ' + trans[t]['base'] + '</td></tr>\n')
                elif i > 1:
                    f.write('<tr><td></td><td></td><td></td><td></td><td>to ' + verb + ' : ' + trans[t]['base'] + '</td></tr>\n')
                i+=1
            nb+=1
            previous_base = v['root_base']
        
        f.write('</table>\n')
        f.close()
        
        return nb
        
#------------------------------------------------------------------------------
# Simple renderer for French, txt or html
#------------------------------------------------------------------------------

class ConjugateFr(Renderer):

    def render(self, onfile=False, html=False):
        verbs = self.tables['verbs']
        
        if onfile:
            f = open('output.html', mode='a', encoding='utf-8')
            if not html:
                f.write('\n###################################################\n\n')
                f.write('1. Indicatif présent\n')
            else:
                f.write('\n\n<table><tbody>\n')
        pronoms = ['je', 'tu', 'elle, il', 'nous', 'vous', 'elles, ils']
        espace_pro = ['\t\t', '\t\t', '\t', '\t\t', '\t\t', '\t']
        root = verb[:-2]
        
        if not onfile: print('\n1. Indicatif présent')
        suffix = ['e', 'es', 'e', 'ons', 'ez', 'ont']
        for i, term in enumerate(suffix):
            if onfile:
                if not html:
                    f.write(pronoms[i] + espace_pro[i] + root + term + '\n')
                else:
                    f.write('\t<tr><td>' + pronoms[i] + '</td><td>' + root + term + '</td></tr>\n')
            else:
                print(pronoms[i] + espace_pro[i] + root + term)
        if onfile:
            if not html:
                f.write('\n2. Indicatif imparfait\n')
            else:
                f.write('</tbody></table>\n\n<table><tbody>\n')
        
        if not onfile: print('\n2. Indicatif imparfait')
        suffix = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
        for i, term in enumerate(suffix):
            if onfile:
                if not html:
                    f.write(pronoms[i] + espace_pro[i] + root + term + '\n')
                else:
                    f.write('\t<tr><td>' + pronoms[i] + '</td><td>' + root + term + '</td></tr>\n')
            else:
                print(pronoms[i] + espace_pro[i] + root + term)
        if onfile:
            if not html:
                f.write('\n3. Indicatif futur\n')
            else:
                f.write('</tbody></table>\n\n<table><tbody>\n')

        if not onfile: print('\n3. Indicatif futur')
        suffix = ['ai', 'as', 'a', 'ons', 'ez', 'ont']
        for i, term in enumerate(suffix):
            if onfile:
                if not html:
                    f.write(pronoms[i] + espace_pro[i] + verb + term + '\n')
                else:
                    f.write('\t<tr><td>' + pronoms[i] + '</td><td>' + verb + term + '</td></tr>\n')
            else:
                print(pronoms[i] + espace_pro[i] + verb + term)
        if onfile:
            if not html:
                f.write('\n4. Indicatif passé composé\n')
            else:
                f.write('</tbody></table>\n\n<table><tbody>\n')
        
        if not onfile: print('\n4. Indicatif passé composé')
        pronoms = ["j'", 'tu', 'elle, il', 'nous', 'vous', 'elles, ils']
        prefix = ['ai', 'as', 'a', 'avons', 'avez', 'ont']
        for i, aux in enumerate(prefix):
            if onfile:
                if not html:
                    f.write(pronoms[i] + espace_pro[i] + aux + '\t' + root + 'é' + '\n')
                else:
                    f.write('\t<tr><td>' + pronoms[i] + '</td><td>' + aux + ' ' + root + 'é' + '</td></tr>\n')
            else:
                print(pronoms[i] + espace_pro[i] + aux + '\t' + root + 'é')
        if onfile:
            if html:
                f.write('</tbody></table>\n\n')
            f.close()
            print('i file output.html extended')
        else:
            print()
        
        #f.write('4. Participe passé\n')
        #suffix_partpast = ['é', 'ée', 'és', 'ées']
        #root_pp = root
        #for index, value in enumerate(suffix_partpast):
        #    f.write('\t\t' + root_pp + value + '\n')
        #f.write('\n')
        
        #f.write('5. Participe présent\n')
        #suffix_partpresent = ['ant']
        #root_pp = root
        #f.write('\t\t' + root_pp + suffix_partpresent[0] + '\n')
        #f.write('\n')
    
#------------------------------------------------------------------------------
# Console
#------------------------------------------------------------------------------

class Console:

    def __init__(self, pre):
        self.escape = False
        self.cmd = ''
        self.cmd_lang = "fr"
        self.cmd_order = self.cmd_lang + ".lang, " + self.cmd_lang + ".base"
        self.cmd_to = "en"
        self.cmd_auto = False
        self.cmd_debug = True
        self.cmd_file = False # for conjugate
        self.cmd_html = False # for conjugate
        print("i Welcome to Invoke v1.2")
        print("i Type 'help' for help")
        print("i DEBUG is set to", self.cmd_debug)
        self.mainloop(pre)
        
    def mainloop(self, pre=[]):
        if len(pre) > 0:
            for p in pre:
                self.interpret(p)
        while not self.escape:
            self.cmd = input('>>> ')
            self.interpret()
            
    def interpret(self, pcmd=None):
        if pcmd is not None:
            self.cmd = pcmd
        
        if self.cmd == 'exit':
            print('i Goodbye!')
            exit(0)
        elif self.cmd == 'help':
            print("i Commands :")
            print("  Main commands:")
            print("    help - print this help")
            print("    exit - exit")
            print("    create - recreate the database entirely")
            print("    count - count the number of returned results")
            print("    select - select all the verbs for the default language in the default order")
            print("    select ... - select all the verbs for a given language : fr")
            print("    stats - make various stats over the database")
            print("    conjugate ... - conjugate the given verb (only ion French)")
            print("    render - render the list of verbs")
            print("  Parameter settings:")
            print("    order ... - set the order of the returned results")
            print("    lang ... - set the lang of the returned results (for select and trans)")
            print("    lang - get the current lang of the returned results and translation")
            print("    to ... - set the translation of the returned results (for trans)")
            print("    auto - switch to wait for a key or not before executing the command")
            print("    file - switch to conjugate a verb in a file instead of displaying it")
            print("    html - switch to output in html in the file instead of plain text")
            print("    reset - reset the file where the conjugated verbs are stored")
            print("    close - write the footer in the file where the conjugated verbs are stored")
            print("  Available languages are : fr, en, it, eo, de")
        elif self.cmd == 'create':
            print("i Recreating the database")
            create()
            print("i Database recreated")
        elif self.cmd == 'select':
            exec_cmd('select', self.cmd_lang, self.cmd_order, self.cmd_auto, None, self.cmd_debug)
        elif self.cmd == 'trans':
            exec_cmd('trans', self.cmd_lang, self.cmd_order, self.cmd_auto, self.cmd_to, self.cmd_debug)
        elif self.cmd == 'count':
            print("i Returned results for lang [" + self.cmd_lang + "] = " + str(exec_cmd('count', self.cmd_lang, self.cmd_order, self.cmd_auto)))
        elif self.cmd == 'auto':
            if self.cmd_auto:
                self.cmd_auto = False
            else:
                self.cmd_auto = True
            print("i Auto switch to " + str(self.cmd_auto))
        elif self.cmd == 'file':
            if self.cmd_file:
                self.cmd_file = False
            else:
                self.cmd_file = True
            print("i File switch to " + str(self.cmd_file))
        elif self.cmd == 'html':
            if self.cmd_html:
                self.cmd_html = False
            else:
                self.cmd_html = True
            print("i HTML switch to " + str(self.cmd_html))
            if not self.cmd_file:
                self.cmd_file = True
                print("i File switch to True also")
        elif self.cmd == 'reset':
            #f = open('output.html', 'w')
            #f.close()
            header_en()
            print('i file output.html reset, header written')
        elif self.cmd == 'close':
            footer_en()
            print('i footer written in file output.html')
        elif self.cmd == 'debug':
            if self.cmd_debug:
                self.cmd_debug = False
                self.cmd_auto = True
            else:
                self.cmd_debug = True
                self.cmd_auto = False
            print("i Debug switch to " + str(self.cmd_debug))
            print("i Auto switch to " + str(self.cmd_auto))
        elif self.cmd == 'lang':
            print("i Current language is [" + self.cmd_lang + "], current translation is [" + self.cmd_to + "]")
        elif self.cmd == 'stats':
            exec_stat(self.cmd_auto, self.cmd_debug)
        elif self.cmd in ['conjugate', 'conj', 'con']:
            s = input('Enter a verb : ')
            conjugate(s, self.cmd_lang, self.cmd_file, self.cmd_html)
            print("i Verb " + s + " conjugated. Results can be found in " + s.lower() + ".txt")
        elif self.cmd in ['render']: # New Architecture
            verbs = get_all_verbs_full('en', 'fr')
            ConjugateTabularEn({'verbs' : verbs}).render('output2.html')
        elif len(self.cmd.split(' ')) > 1:
            c_tab = self.cmd.split(' ')
            if c_tab[0] == 'select':
                if c_tab[1] in ['fr', 'it', 'eo', 'en', 'de']:
                    if c_tab[1] != self.cmd_lang: # order must be set to the language we call
                        exec_cmd('select', c_tab[1], c_tab[1] + ".lang, " + c_tab[1] + ".base", self.cmd_auto, None, self.cmd_debug)
                    else:
                        exec_cmd('select', c_tab[1], self.cmd_order, self.cmd_auto, None, self.cmd_debug)
                else:
                    print("! Unknown language : ", c_tab[1])
            elif c_tab[0] == 'order':
                self.cmd_order = c_tab[1]
            elif c_tab[0] == 'lang':
                if c_tab[1] in ['fr', 'it', 'eo', 'en', 'de']:
                    self.cmd_lang = c_tab[1]
                    self.cmd_order = self.cmd_lang + ".lang, " + self.cmd_lang + ".base"
                else:
                    raise Exception("Unknown lang : " + c_tab[1])
            elif c_tab[0] == 'to':
                if c_tab[1] in ['fr', 'it', 'eo', 'en', 'de']:
                    self.cmd_to = c_tab[1]
                else:
                    raise Exception("Unknown lang : " + c_tab[1])
            elif c_tab[0] in ['conjugate', 'conj','con']:
                conjugate(c_tab[1], self.cmd_lang, self.cmd_file, self.cmd_html)
                # print("i Verb " + c_tab[1] + " conjugated. Results can be found in " + c_tab[1].lower() + ".txt")
            else:
                print("! Unknown command with parameters : " + self.cmd)
        elif self.cmd == '':
            pass
        else:
            print("! Unknown command : " + self.cmd)

if __name__ == '__main__': 
    #commands = ['create', 'reset', 'html', 'lang en', 'con all', 'close', 'exit']
    commands = ['create', 'render', 'exit']
    Console(commands) #'con talk', 'con accept', 'exit'])
