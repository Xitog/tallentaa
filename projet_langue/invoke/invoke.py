"Local version of Invoke"

#------------------------------------------------------------------------------
# Local version of Invoke
# Handle the database of words and translations.
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
#------------------------------------------------------------------------------

import os
import sys
import sqlite3
#import unicodedata
import invoke_data


class InvokeDB:
    """
        Creation, verification of the Invoke Database
    """

    @staticmethod
    def check_content_verbs(content):
        "Test de l'unicité des ids et des bases"
        verbes_id = []
        verbes_base_lang = {}
        error = False
        for verb in content:
            idv = verb[0]
            if idv in verbes_id:
                print("ERROR : id 2x : " + str(idv))
                error = True
            else:
                verbes_id.append(idv)
            base = verb[2]
            if base in verbes_base_lang and verbes_base_lang[base] == verb[1]: # same base and lang
                print("ERROR : base 2x : " + base)
                error = True
            else:
                verbes_base_lang[base] = verb[1] # 'dire' : 'fr' ou 'dire' : 'it'
        if error:
            print("Errors have been found.")
            exit()
        return verbes_id

    @staticmethod
    def check_content_trans(content, verbes_id):
        "Tests Foreign Key"
        error = False
        for trans in content:
            origine = trans[1]
            vers = trans[2]
            if origine not in verbes_id or vers not in verbes_id:
                if origine not in verbes_id:
                    print("Unknown DE id : " + str(origine) + " from " + str(trans))
                    error = True
                if vers not in verbes_id:
                    print("Unknown VERS id : " + str(vers) + " from " + str(trans))
                    error = True
        if error:
            print("Errors have been found.")
            exit()


    @staticmethod
    def create_db(db_path):
        "Create the invoke database"
        try:
            os.remove(db_path)
        except FileNotFoundError:
            print("FileNotFound")
        conn = sqlite3.connect(db_path)
        connection = conn.cursor()

        # Tables creation
        connection.execute(invoke_data.get_create_table_verbs())
        connection.execute(invoke_data.get_create_table_trans())
        connection.execute(invoke_data.get_create_table_verbs_en())

        # Tables filling
        content = invoke_data.get_verbs()
        verbes_id = InvokeDB.check_content_verbs(content)
        connection.executemany('INSERT INTO voc_verbs VALUES (?,?,?,?,?)', content)

        content_verbs_en = invoke_data.get_irregular_verbs()
        irr_not_found = 0
        for irr_verb in content_verbs_en:
            found = False
            for verb in content:
                if irr_verb[1] == verb[2] and verb[1] == 'en':
                    # le verbe est dans la base et dans celle des irréguliers
                    found = True
                    break
            if not found:
                # on a un irrégulier qui n'est pas dans notre base
                print(irr_verb[1])
                irr_not_found += 1
        print("i Irregulars not found in our base :", irr_not_found)

        connection.executemany('INSERT INTO voc_verbs_en VALUES (?,?,?,?)', content_verbs_en)

        content = invoke_data.get_traductions()
        InvokeDB.check_content_trans(content, verbes_id)
        for i in content:
            if len(i) != 5:
                print(i)
                exit()
        try:
            connection.executemany('INSERT INTO voc_translate VALUES (?, ?, ?, ?, ?)', content)
        except sqlite3.ProgrammingError as prog_err:
            print('! Erreur : ' + str(prog_err))

        conn.commit()
        conn.close()
        InvokeDB.analyse_create(db_path)


    @staticmethod
    def analyse_create(db_path):
        "Analyse the database created"
        conn = sqlite3.connect(db_path) # réouverture
        connection = conn.cursor()
        res_file = open('./output/results.txt', mode='w', encoding='utf-8')

        res_file.write("------------------------------------------------------------------------\n")
        res_file.write("Toutes les traductions\n")
        res_file.write("------------------------------------------------------------------------\n")
        i = 0
        for row in connection.execute(invoke_data.get_select_translation_en()):
            i += 1
            if row[2] is not None:
                res_file.write(str(i) + ". " + row[0] + " --> to " + row[1] + " avec le sens de : "
                               + row[2] +"\n")
            else:
                res_file.write(str(i) + ". " + row[0] + " --> to " + row[1] + "\n") #'::'.join(row))

        res_file.write("\n\n\n")
        res_file.write("------------------------------------------------------------------------\n")
        res_file.write("Tous les verbes français\n")
        res_file.write("------------------------------------------------------------------------\n")
        i = 0
        for row in connection.execute(invoke_data.get_select_table_verbs_fr()):
            i += 1
            res_file.write(str(i) + ". #" + str(row[0]) + " " + row[1] + "\n")

        res_file.write("\n\n\n")
        res_file.write("------------------------------------------------------------------------\n")
        res_file.write("Verbes non traduits\n")
        res_file.write("------------------------------------------------------------------------\n")
        i = 0
        for row in connection.execute(invoke_data.get_select_untranslated_en()):
            i += 1
            res_file.write(str(i) + ". #" + str(row[0]) + " " + row[1] + "\n")

        from time import gmtime, strftime
        res_file.write("\n\nLast edit on " + strftime("%Y-%m-%d %H:%M:%S"))  #, gmtime())
        res_file.close()


def exec_stat(db_path, p_auto=False, p_debug=False):
    "Exec statistics on database"
    p_conn = sqlite3.connect(db_path)
    p_cursor = p_conn.cursor()
    dic = {'fr': 'French', 'en': 'English', 'it': 'Italian', 'eo': 'Esperanto', 'de' : 'German'}
    total = 0
    for lang in dic:
        p_string = "SELECT count(*), surtype FROM voc_verbs WHERE lang = '" + lang
        p_string += "' GROUP BY surtype"
        if p_debug:
            print("% Executing : " + p_string)
        if not p_auto:
            print("% Press a key to continue")
            input()
        count_lang = 0
        for p_row in p_cursor.execute(p_string):
            print("i   " + dic[lang] + " " + p_row[1] + " : " + str(p_row[0]))
            count_lang += p_row[0]
        total += count_lang
        print("i " + dic[lang] + " total words : " + str(count_lang))
    print("i Total = " + str(total))
    p_cursor.close()
    p_conn.close()


def get_all_verbs_en(db_path):
    "fetch irregular"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    request = "SELECT id, base, pret, part FROM voc_verbs_en"
    results = {}
    for row in cursor.execute(request): # base = be afraid, root = be
        results[row[1]] = {'id' : row[0], 'base' : row[1], 'pret' : row[2], 'part' : row[3]}
    return results

# Fetch all the verbs in lines with the translation
# I translate these lines into structured verb hash
# But in ConjugateTabularEn::render() I transform them in lines again!
def get_all_verbs_full(db_path, p_lang='en', p_to='fr'):
    "All verbs, with translations and irregular forms"
    p_conn = sqlite3.connect(db_path)
    p_cursor = p_conn.cursor()
    p_order = p_lang + '.base'
    counter = 0                    # 0      1        2       3     4        5     6       7     8
    p_string = ("SELECT " + p_lang + ".id, " + p_lang + ".base, " + p_lang + ".surtype, " + p_lang +
                ".lvl, " + p_to + ".base, " + p_to + ".id, t.sens, t.id, t.usage " +
                "FROM voc_verbs as " + p_lang + ", voc_verbs as " + p_to +
                ", voc_translate as t WHERE " + p_lang + ".id = t.de AND " + p_to +
                ".id = t.vers AND " + p_lang + ".lang = '" + p_lang + "' AND " + p_to +
                ".lang = '" + p_to + "' AND " + p_lang + ".surtype = 'verb'" +
                " ORDER BY " + p_order)
    verbs = []
    actual = {}
    irregulars = get_all_verbs_en(db_path)
    for p_row in p_cursor.execute(p_string):
        if actual == {} or actual['id'] != p_row[0]:
            counter += 1
            if actual == {}:
                actual = {'nb' : counter}
            else:
                # gestion à particules
                if len(actual['base'].split(' ')) > 1:
                    actual['root'] = actual['base'].split(' ')[0]
                    actual['particle'] = ' ' + actual['base'].split(' ')[1]
                else:
                    actual['root'] = actual['base']
                    actual['particle'] = ''
                # gestion des prétérits
                if actual['root'] in irregulars:
                    actual['pret'] = irregulars[actual['root']]['pret']
                    actual['part'] = irregulars[actual['root']]['part']
                    actual['irregular'] = True
                else:
                    actual['irregular'] = False
                    actual['part'] = EnglishUtils.en_make_part(actual['root'])
                    actual['pret'] = actual['part']
                verbs.append(actual)
                actual = {'nb' : counter}
            #print('verbe : ' + p_row[1])
            actual['id'] = p_row[0]
            actual['base'] = p_row[1]
            actual['surtype'] = p_row[2]
            actual['lvl'] = p_row[3]
            actual['ing'] = EnglishUtils.en_make_ing(p_row[1].split(' ')[0])
            actual['p3ps'] = EnglishUtils.en_make_pres3ps(p_row[1].split(' ')[0])
            actual['trans'] = {}
            # attention parfois p_row 6 ou 8 peuvent-être None
            # tid : translation id, tvid : translated verb id
            actual['trans'][p_row[5]] = {'base' : p_row[4], 'sens' : p_row[6], 'usage' : p_row[8],
                                         'tid' : p_row[7], 'tvid' : p_row[5]}
        elif actual is not None:
            actual['trans'][p_row[5]] = {'base' : p_row[4], 'sens' : p_row[6], 'usage' : p_row[8],
                                         'tid' : p_row[7], 'tvid' : p_row[5]}
    if actual is not None:
        if len(actual['base'].split(' ')) > 1:
            actual['root'] = actual['base'].split(' ')[0]
            actual['particle'] = ' ' + actual['base'].split(' ')[1]
        else:
            actual['root'] = actual['base']
            actual['particle'] = ''
        if actual['root'] in irregulars:
            actual['pret'] = irregulars[actual['root']]['pret']
            actual['part'] = irregulars[actual['root']]['part']
            actual['irregular'] = True
        else:
            # Building of preterit & past participe !! DUPLICATE CODE HERE NOT UPDATED FROM UP THERE
            actual['irregular'] = False
            if actual['root'][-1] != 'e' and actual['root'][-1] != 'y':
                actual['part'] = actual['root'] + 'ed'
            elif actual['root'][-1] == 'e':
                actual['part'] = actual['root'] + 'd'
            elif actual['root'][-1] == 'y':
                actual['part'] = actual['root'][0:-1] + "ied"
            actual['pret'] = actual['part']

        verbs.append(actual)
    return verbs


def exec_cmd(db_path, p_main, p_lang, p_order, p_auto, p_to='', p_debug=False, display=True):
    "Execute a command"
    if p_order == '':
        p_order = p_lang + ".lang, " + p_lang + ".base"

    p_conn = sqlite3.connect(db_path)
    p_cursor = p_conn.cursor()
    counter = 0
    if p_main in ['select', 'trans']:
        cnt = False
    elif p_main in ['count']:
        cnt = True
    else:
        print("! Command unknown : ", p_main)
        return -1
    if p_main == 'select' or p_main == 'count':
        p_string = ("SELECT " + p_lang + ".id, " + p_lang + ".base, " + p_lang + ".surtype, " +
                    p_lang + ".lvl" + " FROM voc_verbs as " + p_lang +
                    " WHERE " + p_lang + ".lang = '" + p_lang + "' ORDER BY " + p_order)
    elif p_main == 'trans':
        p_string = ("SELECT " + p_lang + ".id, " + p_lang + ".base, " + p_to + ".base, " + p_to +
                    ".id, t.sens, t.id " + "FROM voc_verbs as " +
                    p_lang + ", voc_verbs as " + p_to + ", voc_translate as t WHERE " + p_lang +
                    ".id = t.de AND " + p_to + ".id = t.vers AND " + p_lang + ".lang = '" + p_lang +
                    "' AND " + p_to + ".lang = '" + p_to + "' ORDER BY " + p_order)
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
                        print("#" + str(p_row[0]) + "  " + p_row[1] + " (" + p_row[2] + ") [" +
                              str(p_row[3]) + "]")
                    except UnicodeEncodeError:
                        word = p_row[1]
                        word_modified = ''
                        for letter in word:
                            if letter == "\u0153":
                                word_modified += 'oe'
                            else:
                                word_modified += letter
                            #print('%04x' % ord(letter))
                        print("#" + str(p_row[0]) + "  " + word_modified + " (" + p_row[2] + ") [" +
                              str(p_row[3]) + "]")
                elif p_main == 'trans':
                    sys.stdout.write("#" + str(p_row[5]) + "  " + p_row[1] + " (" + str(p_row[0]) +
                                     ")")
                    if p_row[4] is not None:
                        sys.stdout.write(" --> to " + p_row[2] + " (" + str(p_row[3]) +
                                         ") avec le sens de : " + p_row[4] + "\n")
                    else:
                        sys.stdout.write(" --> to " + p_row[2] + " (" + str(p_row[3]) + ")\n")
            counter += 1
    else: # ne marche que pour select
        verbs = []
        for p_row in p_cursor.execute(p_string):
            verb = {}
            verb['id'] = p_row[0]
            verb['base'] = p_row[1]
            verb['surtype'] = p_row[2]
            verb['lvl'] = p_row[3]
            verbs.append(verb)
    print("i Number of returned results = " + str(counter))
    p_cursor.close()
    p_conn.close()
    if display:
        return counter
    else:
        return verbs


def conjugate(db_path, verb, lang, onfile=False, html=False):
    """
        Conjugate : new from 2/11/2015
        Il faudrait faire une option qui génère tout cela dans un fichier texte plutôt qu'en sortie
        console.
        Aucun test, cela ne marche que pour les verbes du 1er groupe se conjuguant avec avoir.
    """
    if lang not in ['fr', 'en']:
        print('Unknwon conjugaison for', lang)
        return
    if verb == 'all' and lang == 'en':
        # make book
        results = get_all_verbs_full(db_path)
        counter = 0
        for res_elem in results:
            if res_elem['surtype'] == 'verb':
                counter += 1
                conjugate_en(res_elem['base'], onfile, html, res_elem, counter)
            else:
                print(res_elem['surtype'])
        print('i Conjugaison done for', len(results), 'verbs')
    elif verb == 'all':
        results = exec_cmd(db_path, 'select', lang, '', False, None, False, False)
        # filter on verb
        counter = 0
        for res_elem in results:
            if res_elem['surtype'] == 'verb':
                if lang == 'fr':
                    raise 'Not working anymore' # conjugate_fr(res_elem['base'], onfile, html)
                elif lang == 'en':
                    conjugate_en(res_elem['base'], onfile, html)
                counter += 1
        print('i Conjugaison done for', counter, 'verbs')
    else:
        if lang == 'fr':
            raise 'Not working anymore' # conjugate_fr(verb, onfile, html)
        elif lang == 'en':
            conjugate_en(verb, onfile, html)


class EnglishUtils:
    """
        Classe regroupant des méthodes statiques pour la langue anglaise.
        Comment faire automatiquement la 3e personne du singulier, le participe présent et
        le participe/prétérit pour les verbes réguliers.
    """

    @staticmethod
    def en_make_pres3ps(root):
        "3e personne du présent de l'indicatif"
        pres3 = ''
        # Present 3e
        if root == 'be':
            pres3 = 'is'
        elif root in ['must']:
            pres3 = '-'
        elif root[-1] == 'y' and root[-2] in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
                                              'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']:
            pres3 = root[0:-1] + "ies"
        elif root[-1] in ['s', 'x', 'z', 'o'] or root[-2:] in ['ch', 'sh']:
            pres3 = root + '<b class="s">es</b>'
        else:
            pres3 = root + '<b class="s">s</b>'
        return pres3

    @staticmethod
    def en_make_ing(root):
        "participe présent"
        ing = ''
        if root == 'be':
            ing = 'being'
        elif len(root) == 3 and root[-2:] == 'ie':
            ing = root[:-2] + 'ying' # die and lie
        elif root in ['must']:
            ing = '-'  # becoME => becoming (cons + E) => (cons + ing)
        elif root[-1] == 'e' and root[-2] in ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
                                              'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']:
            ing = root[:-1] + 'ing'
        elif root[-1] in ['t', 'p'] and root[-2] in ['a', 'e', 'i'] and root[-3] in ['h', 'g', 'l']:
            # cHAT => chatting (h + a + t) => (hatt + ing)
            # slip => slipping (l + i + p) => (lipp + ing)
            ing = root + root[-1] + 'ing'
        else:
            # GET => getting (g + e + t) => (gett + ing)
            ing = root + 'ing'
        return ing

    @staticmethod
    def en_make_part(root):
        "participe passé et prétérit réguliers"
        part = ''
        # Building of preterit & past participe
        if root[-1] == 'e':                              # change => changed
            part = root + 'd'
        elif root[-1] == 'y':
            if root[-2] in ['a', 'e', 'i', 'o', 'u']:    # base (stay => stayed)
                part = root + "ed"
            else:
                part = root[0:-1] + "ied"      # carry => carried
        elif root[-1] not in ['a', 'i', 'o', 'u']:
            if root[-2] in ['a', 'u', 'i']:
                if root[-3] in ['a', 'e', 'o', 'u'] or len(root) > 4:
                    # base (cook => cooked, wait => waited) et le cas visit => visited
                    # au lieu de la len faire juste que -3 ne soit pas i ?
                    part = root + 'ed'
                else:                                                   # chat => chatted
                    part = root + root[-1] + 'ed'
            else:
                part = root + 'ed'             # base
        else:
            part = root + 'ed'                 # base
        return part


def conjugate_en(verb, onfile=False, html=False, info=None, number=None):
    "Conjugue une verbe en anglais"
    if verb != info['root']:
        raise "Function Deprecated"
    if not onfile or not html or number is None or info is None:
        print("i This function works only with onfile and html set at true")
        return

    fout = open('./output/output1.html', mode='a', encoding='utf-8')
    #pronoms = ['I', 'you', 'she, he, it', 'we', 'you', 'they']
    root = info['root']
    particle = info['particle']
    pret = info['pret']
    part = info['part']

    pres3 = EnglishUtils.en_make_pres3ps(root)
    ing = EnglishUtils.en_make_ing(root)

    fout.write('<h2 id="' + str(info['id']) + '">' + str(number) + '. ' + root + particle +
               ' &nbsp;&nbsp;(' + pret + particle + ', ' + part + particle + ')</h2>\n')
    fout.write('<p><b>Sens et traduction</b> : <ul>\n')
    for trans in info['trans']:
        if info['trans'][trans]['usage'] is not None:
            usages = info['trans'][trans]['usage'].split(',')
            for usage in usages:
                fout.write('\t<li>' + usage + '</li>\n')
        elif info['trans'][trans]['sens'] is not None:
            fout.write('\t<li>' + info['trans'][trans]['base'] + ' (' + info['trans'][trans]['sens']
                       + ')</li>\n')
        else:
            fout.write('\t<li>' + info['trans'][trans]['base'] + '</li>\n')
    fout.write('</ul></p>\n')

    #f.write('<p><b>Base verbale</b> : ' + root + '</p>\n')
    fout.write('<p><b>Infinitif</b> : <b>to <b class="present">' + root + '</b></b></p>\n')
    fout.write('<p><b>Participe passé</b> : <b class="pp">' + part + '</b></p>\n')
    fout.write('<p><b>Participe présent</b> : <b class="ing">' + ing + particle + '</b></p>\n')
    fout.write('<p><b>Voix passive</b> : <b>were ' + part + '</b> (1ère et 3e pers. sing. : <b>was '
               + part + '</b>)</p>\n')

    fout.write('<h3>Indicatif</h3>\n')

    fout.write('<div class="simple">\n')
    fout.write('<p><b>Présent simple</b> :<ul>\n')
    fout.write('\t<li>forme <b>affirmative</b> : <b class="present">' + root + particle +
               '</b> (3e pers. sing. : <b class="present">' + pres3 + particle + '</b>)</li>\n')
    fout.write('\t<li>forme <b>négative</b> : <b class="present">do not ' + root +
               '</b> (3e pers. sing. : <b class="present">do</b><b class="s">es</b>' +
               '<b class="present">' + ' not ' + root + particle + ')</b></li>\n')
    fout.write('</ul></p>\n')
    fout.write('<p><b>Passé simple (ou prétérit)</b> :<ul>\n')
    fout.write('\t<li>forme <b>affirmative</b> : <b class="past">' + pret + particle +
               '</b></li>\n')
    fout.write('\t<li>forme <b>négative</b> : <b class="past">did not ' + root + particle +
               '</b></li>\n')
    fout.write('</ul></p>\n')
    fout.write('<p><b>Futur simple</b> : <b class="future">will</b> <b>(not)</b> <b class="future">'
               + root + particle + '</b></p>\n')
    fout.write('</div>\n')

    fout.write('<div class="pp">\n')
    fout.write('<p><b>Présent parfait</b> : <b class="present">have</b> <b>(not)</b> <b class="pp">'
               + part + particle + '</b> (3e pers. sing. : <b class="present">' +
               'ha</b><b class="s">s</b> <b>(not)</b> <b class="pp">' + part + particle +
               '</b>)</p>\n')
    fout.write('<p><b>Passé parfait</b> : <b class="past">had</b> <b>(not)</b> <b class="pp">' +
               part + particle + '</b></p>\n')
    fout.write('<p><b>Futur parfait</b> : <b class="future">will</b> <b>(not)</b> ' +
               '<b class="future">have</b> <b class="pp">' + part + particle + '</b></p>\n')
    fout.write('</div>\n')

    fout.write('<div class="ing">\n')
    fout.write('<p><b>Présent continu</b> : <b class="present">are</b> <b>(not)</b> ' +
               '<b class="ing">' + ing + particle +  '</b> (1ère et 3e pers. sing. : ' +
               ' <b class="present">is</b> ' + '<b>(not)</b> <b class="ing">' + ing + particle +
               '</b></p>\n')
    fout.write('<p><b>Passé continu</b> : <b class="past">were</b> <b>(not)</b> <b class="ing">' +
               ing + particle +  '</b> (1ère et 3e pers. sing. : <b class="past">was</b> ' +
               '<b>(not)</b>'+ ' <b class="ing">' + ing + particle + '</b></p>\n')
    fout.write('<p><b>Futur continu</b> : <b class="future">will be</b> <b>(not)</b> ' +
               '<b class="ing">' + ing + particle + '</b></p>\n')
    fout.write('</div>\n')

    fout.write('<div class="pp">\n')
    fout.write('<div class="ing">\n')
    fout.write('<p><b>Présent parfait continu</b> : <b class="present">have</b> <b>(not)</b> ' +
               '<b class="pp">been</b> <b class="ing">' + ing + particle +
               '</b> (3e pers. sing. : <b class="present">' + 'ha</b><b class="s">s</b> ' +
               '<b>(not)</b> <b class="pp">been</b> <b class="ing">' + ing + particle +
               '</b>)</p>\n')
    fout.write('<p><b>Passé parfait continu</b> : <b class="past">had</b> <b>(not)</b> ' +
               '<b class="pp">been</b> <b class="ing">' + ing + particle + '</b></p>\n')
    fout.write('<p><b>Futur parfait continu</b> : <b class="future">will</b> <b>(not)</b> ' +
               '<b class="future">have</b> <b class="pp">been</b> <b class="ing">' + part +
               particle + '</b></p>\n')
    fout.write('</div>\n')
    fout.write('</div>\n')

    fout.write('<h3>Conditionnel</h3>\n')
    fout.write('<p><b>Présent</b> : <b class="cond">should/would</b> <b>(not)</b> ' +
               '<b class="present">' + root + particle + '</b></p>\n')
    fout.write('<p><b>Passé</b> : <b class="cond">should/would</b> <b>(not)</b> ' +
               '<b class="cond">have</b> <b class="pp">' + part + particle + '</b></p>\n')

    fout.write('<h3>Subjonctif</h3>\n')
    fout.write('<p><b>Présent</b> : <b>(not)</b> <b class="present">' + root + particle +
               '</b> (à <u>toutes</u> les personnes)</p>\n')
    if root == 'be':
        fout.write('<p><b>Passé</b> : <b>(not)</b> <b class="past">' + pret + particle +
                   '</b> (à <u>toutes</u> les personnes)</p>\n')

    fout.write('<h3>Impératif</h3>\n')
    fout.write('<p><b>2e pers.</b> : <b>(do not)</b> <b class="present">' + root + particle +
               '</b>!</p>\n')
    fout.write('<p><b>1e pers. du pluriel</b> (avec deux façons d\'exprimer la négation) : ' +
               '<b>(do not)</b> <b class="present">let</b> \'s <b>(not)</b> <b class="present">' +
               root + particle + '</b>!</p>\n')
    fout.write('<p><b>3e pers.</b> (avec deux façons d\'exprimer la négation) : <b>(do not)</b> ' +
               '<b class="present">let</b> her/him/them <b>(not)</b> <b class="present">' + root +
               particle + '</b>!</p>\n')

    fout.write('<div class="retour"><b><a href="#tous_les_verbes">' +
               'Retour à la liste des verbes</a>' + '</b></div>')
    fout.write('<mbp:pagebreak />')
    fout.close()


class AbstractRenderer:
    """
        Basic Abstract Renderer (BAR)
    """

    def __init__(self, tables):
        self.tables = tables

    def info(self):
        "info"
        print('Number of tables:', len(self.tables))
        for key in self.tables:
            print('Key:', key, 'Number of elements:', len(self.tables[key]))

    def render(self, target):
        "render"
        raise Exception('This is an abstract class.')


class VerbesAnglaisEssentielsRenderer(AbstractRenderer):
    "New version of my final renderer"

    def sub_render_menu_letters_en(self, fout, verbs):
        """lettres en"""
        fout.write('<a name="letters_en"></a><table class="mono"><tr class="title"><td>Accès par la première lettre du verbe anglais</td></tr><tr><td class="trad">')
        letter = ''
        for verb in verbs:
            if letter == '' or letter != verb['base'][0]:
                fout.write('<a href="#' + verb['base'][0] + '">' + verb['base'][0].capitalize() + '</a>&nbsp;&nbsp;')
                letter = verb['base'][0]
        fout.write('</td></tr></table><br><br>')
    
    
    def sub_render_menu_verbs_by_letter_en(self, fout, verbs):
        """classement par lettre des verbes anglais"""
        letter = ''
        nb_on_line = 0
        for verb in verbs:
            if letter == '':
                fout.write('<a name="' + verb['base'][0] + '"></a><table class="mono"><tr class="title"><td><a href="#letters_en">&lt;&nbsp;&nbsp;</a>' + verb['base'][0] + '</td></tr><tr class="trad"><td>')
                letter = verb['base'][0]
            elif verb['base'][0] != letter:
                fout.write('</td></tr></table><br><br><a name="' + verb['base'][0] + '"></a><table class="mono"><tr class="title"><td><a href="#letters_en">&lt;&nbsp;&nbsp;</a>' + verb['base'][0] + '</td></tr><tr class="trad"><td>')
                letter = verb['base'][0]
                nb_on_line = 0
            irr = '&nbsp;<b class="s">*</b>' if verb['irregular'] else ''
            nb_on_line += len(verb['base'])
            nb_on_line = (nb_on_line + 2) if irr != '' else nb_on_line
            if nb_on_line >= 80:
                fout.write('<br>')
                nb_on_line = 0
            fout.write('<a href="#' + verb['base'] + '">' + verb['base'] + '</a>' + irr + '&nbsp;&nbsp;')
        fout.write('</td></tr></table><br><br>')
    
    
    def render(self, target):
        "render"
        verbs = self.tables['verbs']

        fout = open(target, mode='a', encoding='utf-8')
        fout.write("<div><h1>Verbes anglais essentiels</h1></div>")
        
        # Ici je regroupe les verbes
        # to be
        # to be afraid
        # ne font former plus qu'un verb, et be aura dans ses "traductions" be afraid : avoir peur.
        old = 0
        verbs2 = []
        for i in range(len(verbs)):
            #print(i, '/', len(verbs), verbs[i]['root'], old, '/', len(verbs2), verbs[old]['root'])
            for trans_elem in verbs[i]['trans']:
                verbs[i]['trans'][trans_elem]['baseEn'] = verbs[i]['base']
            
            if i > 0 and verbs[i]['root'] == verbs[old]['root']:
                verbs2[len(verbs2)-1]['trans'].update(verbs[i]['trans'])
            else:
                verbs2.append(verbs[i])
                old = i
        
        self.sub_render_menu_letters_en(fout, verbs2)
        self.sub_render_menu_verbs_by_letter_en(fout, verbs2)
        
        # verbe par verbe
        for verb in verbs2:
            fout.write('<a name="' + verb['base'] + '"></a>' + '<table class="mono">\n')
            irr = ''
            if verb['irregular']:
                irr = ' <b>*</b>'
            fout.write('<tr class="title"><td colspan="5"><a href="#' + verb['base'][0] + '">&lt;&nbsp;&nbsp;</a>' + verb['base'] + irr + '</td></tr>')
            fout.write('<tr class="temps"><td>Présent</td><td>Prétérit</td>' +
                       '<td>Participe passé</td><td>Participe présent</td>' +
                       '<td>3e pers. sing.</td></tr>')
            p3ps = verb['p3ps'] if verb['root'] != 'be' else '<b class="s">' + verb['p3ps'] + '</b>'
            pret = verb['pret'] if verb['root'] != 'be' else '<b class="s">' + verb['pret'] + '</b>'
            fout.write('<tr class="formes"><td>' + verb['root'] + ' ' + verb['particle'] + 
                       '</td><td>' + pret + '</td><td>' + verb['part'] + '</td><td>' +
                       verb['ing'] + '</td><td>' + p3ps + '</td></tr>')
            #for trans, value in verb['trans'].items():
            for trans in sorted(verb['trans']):
                value = verb['trans'][trans]
                to = 'to ' if verb['base'] != 'must' else ''
                #if verb['root'] == 'be':
                #    print(verb['trans'])
                try:
                    fout.write('<tr class="trad"><td colspan="5">' + to + 
                               value['baseEn'] + ' ' +
                               ' : ' + value['base'] + '</td></tr>')
                except Exception as e:
                    print(verb['trans'][trans])
                    print(e)
                    exit()
            fout.write('</table>')
            fout.write('<br><br>')
        
        fout.close()


class ConjugateTabularEnRenderer(AbstractRenderer):
    """
        Debug renderer : Simple tabular renderer for English in html
        Affiche tout dans un tableau avec les id.
    """

    def header(self, fout):
        "header"
        fout.write("""
            <head>
                <style type="text/css">
                    div {
                        width: 20cm;
                        margin: auto;
                        margin-bottom: 10px;
                    }
                    
                    h1 {
                        font-size: 36px;
                        font-family: Calibri;
                        color: black;
                        border-bottom: 1px solid rgb(91, 155, 213);
                        text-align: left;
                    }
                    
                    table.all {
                        border: 1px solid rgb(91, 155, 213);
                        border-collapse: collapse;
                        width: 32cm; /* 20 */
                        margin: auto;
                        font-size: 18px;
                        font-family: Calibri;
                    }

                    table.all td.num {
                        width: 1.5cm;
                        text-align: center;
                    }

                    table.all th {
                        background: rgb(91, 155, 213);
                        color: rgb(255, 255, 255);
                        font-weight: bold;
                    }

                    table.all tr:nth-child(odd) {
                        background: rgb(242, 242, 242);
                    }

                    table.all td.irr {
                        font-weight: bold;
                        color: rgb(10, 10, 100); //rgb(146, 208, 80);
                    }

                    b.s {
                        color: rgb(10, 10, 100); //rgb(146, 208, 80);
                    }
                    
                    /*h1 {
                        width: 100%;
                        text-align: center;
                    }*/
                    
                    table.mono {
                        border: 1px solid rgb(91, 155, 213);
                        border-collapse: collapse;
                        width: 20cm;
                        margin: auto;
                        font-size: 18px;
                        font-family: Calibri;
                    }
                    
                    table.mono td {
                        border-right: 1px solid rgb(91, 155, 213);
                        text-align: center;
                    }
                    
                    tr.title {
                        color: rgb(255, 255, 255);
                        background-color: rgb(91, 155, 213);
                        font-weight: bold;
                        font-size: 22px;
                    }
                    
                    tr.title a {
                        text-decoration: none;
                        color: rgb(255, 255, 255);
                    }
                    
                    table.mono tr.title td {
                        text-align: left;
                    }
                    
                    table.mono tr.temps {
                        color: rgb(255, 255, 255);
                        background-color: rgb(146, 208, 80);
                        font-size: 22px;
                    }
                    
                    table.mono tr.formes {
                        border-bottom: 1px solid rgb(91, 155, 213);
                    }
                    
                    table.mono tr.trad td {
                        text-align: left;
                    }
                    
                    table.mono b.s {
                        color: rgb(213,91,155);
                    }
                    
                </style>
            </head>
        """)

    def render(self, target):
        "render"
        verbs = self.tables['verbs']

        fout = open(target, mode='w', encoding='utf-8')
        self.header(fout)
        fout.close()
        xtables = {}
        import copy
        xtables['verbs'] = copy.deepcopy(verbs)
        VerbesAnglaisEssentielsRenderer(xtables).render(target)
        fout = open(target, mode='a', encoding='utf-8')
        fout.write('<table class="all">\n')
        fout.write("""<tr><th>nRacine</th>
                        <th>Irr</th>
                        <th>VID</th>
                        <th>Base verbale</th>
                        <th>Prétérit</th>
                        <th>Participe passé</th>
                        <th>Participe présent</th>
                        <th>3e pers. sing.</th>
                        <th>nConstruction</th>
                        <th>Construction</th>
                        <th>nTrad</th>
                        <th>TID</th>
                        <th>TVID</th>
                        <th>Traduction</th>
                        <th>Ex</th>
                        <th>Ex fr</th>
                   </tr>\n""")
        nb_root = 0
        nb_cons = 0
        nb_trad = 0
        previous_base = None
        previous_cons = None
        for verb in verbs:
            vid = verb['id']
            base = verb['root']
            particle = verb['particle']
            irregular = verb['irregular']
            pret = verb['pret']
            part = verb['part']
            trans = verb['trans']
            ing = verb['ing']
            p3ps = verb['p3ps']

            if base not in ['must']:
                if particle is not None and particle != '':
                    cons = 'to ' + base + ' ' + particle
                else:
                    cons = 'to ' + base
            else:
                cons = 'must'

            irr = 'class="irr"' if irregular else ''
            str_irr = 'True' if irregular else 'False'

            if previous_base is None or previous_base != base:
                nb_root += 1
                cpt_cons = 0
            str_nb_root = str(nb_root)
            if previous_base == base:
                str_nb_root = ''
                str_irr = ''
                #vid = ''
                base = ''
                pret = ''
                part = ''
                ing = ''
                p3ps = ''
            if previous_cons is None or previous_cons != cons:
                nb_cons += 1
                cpt_cons += 1
            str_nb_cons = str(nb_cons) + ' [' + str(cpt_cons) + ']'

            cpt_trad = 0
            for trans_elem in trans:
                nb_trad += 1
                cpt_trad += 1
                fout.write('<tr><td class="num">' + str_nb_root + '</td><td ' + irr + '>' +
                           str_irr + '</td><td>' + str(vid) + '</td><td ' + irr + '>' + base +
                           '</td><td ' + irr + '>' + pret + '</td><td ' + irr + '>' + part +
                           '</td><td>' + ing + '</td><td>' + p3ps + '</td><td class="num">' +
                           str_nb_cons + '</td><td>' + cons + '</td><td class="num">' + str(nb_trad)
                           + ' [' + str(cpt_trad) + ']' + '</td><td>' +
                           str(trans[trans_elem]['tid']) + '</td><td>' +
                           str(trans[trans_elem]['tvid']) + '</td><td>' +
                           trans[trans_elem]['base'] +
                           '</td><td></td><td></td></tr>\n')
                if cpt_trad > 0:
                    str_irr = ''
                    #vid = ''
                    base = ''
                    pret = ''
                    part = ''
                    ing = ''
                    p3ps = ''
                    str_nb_root = ''
                    str_nb_cons = ''
                    cons = ''
            previous_base = verb['root']
            if particle is not None and particle != '':
                previous_cons = 'to ' + verb['root'] + ' ' + particle
            else:
                previous_cons = verb['root']

        fout.write('</table>\n')
        fout.write('<h1>' + str(nb_root) + ' bases, ' + str(nb_cons) + ' verbs, ' + str(nb_trad-1) +
                   ' traductions.</h1>')
        fout.close()

        return nb_cons


class ConjugateFrRenderer(AbstractRenderer):
    """
        Simple renderer for French, txt or html
    """

    #def render(self, onfile=False, html=False):
    def render(self, target):
        onfile = True
        html = True
        verbs = self.tables['verbs']
        verb = verbs[0] # NOT FUNCTIONNAL
        if onfile:
            fout = open('./output/output1.html', mode='a', encoding='utf-8')
            if not html:
                fout.write('\n###################################################\n\n')
                fout.write('1. Indicatif présent\n')
            else:
                fout.write('\n\n<table><tbody>\n')
        pronoms = ['je', 'tu', 'elle, il', 'nous', 'vous', 'elles, ils']
        espace_pro = ['\t\t', '\t\t', '\t', '\t\t', '\t\t', '\t']
        root = verb[:-2]

        if not onfile:
            print('\n1. Indicatif présent')
        suffix = ['e', 'es', 'e', 'ons', 'ez', 'ont']
        for i, term in enumerate(suffix):
            if onfile:
                if not html:
                    fout.write(pronoms[i] + espace_pro[i] + root + term + '\n')
                else:
                    fout.write('\t<tr><td>' + pronoms[i] + '</td><td>' + root + term +
                               '</td></tr>\n')
            else:
                print(pronoms[i] + espace_pro[i] + root + term)
        if onfile:
            if not html:
                fout.write('\n2. Indicatif imparfait\n')
            else:
                fout.write('</tbody></table>\n\n<table><tbody>\n')

        if not onfile:
            print('\n2. Indicatif imparfait')
        suffix = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
        for i, term in enumerate(suffix):
            if onfile:
                if not html:
                    fout.write(pronoms[i] + espace_pro[i] + root + term + '\n')
                else:
                    fout.write('\t<tr><td>' + pronoms[i] + '</td><td>' + root + term +
                               '</td></tr>\n')
            else:
                print(pronoms[i] + espace_pro[i] + root + term)
        if onfile:
            if not html:
                fout.write('\n3. Indicatif futur\n')
            else:
                fout.write('</tbody></table>\n\n<table><tbody>\n')

        if not onfile:
            print('\n3. Indicatif futur')
        suffix = ['ai', 'as', 'a', 'ons', 'ez', 'ont']
        for i, term in enumerate(suffix):
            if onfile:
                if not html:
                    fout.write(pronoms[i] + espace_pro[i] + verb + term + '\n')
                else:
                    fout.write('\t<tr><td>' + pronoms[i] + '</td><td>' + verb + term +
                               '</td></tr>\n')
            else:
                print(pronoms[i] + espace_pro[i] + verb + term)
        if onfile:
            if not html:
                fout.write('\n4. Indicatif passé composé\n')
            else:
                fout.write('</tbody></table>\n\n<table><tbody>\n')

        if not onfile:
            print('\n4. Indicatif passé composé')
        pronoms = ["j'", 'tu', 'elle, il', 'nous', 'vous', 'elles, ils']
        prefix = ['ai', 'as', 'a', 'avons', 'avez', 'ont']
        for i, aux in enumerate(prefix):
            if onfile:
                if not html:
                    fout.write(pronoms[i] + espace_pro[i] + aux + '\t' + root + 'é' + '\n')
                else:
                    fout.write('\t<tr><td>' + pronoms[i] + '</td><td>' + aux + ' ' + root + 'é' +
                               '</td></tr>\n')
            else:
                print(pronoms[i] + espace_pro[i] + aux + '\t' + root + 'é')
        if onfile:
            if html:
                fout.write('</tbody></table>\n\n')
            fout.close()
            print('i file output.html extended')
        else:
            print()


class ConjugateOldRenderer(AbstractRenderer):
    "Very Old Rendered, Deprecated"

    def header_en(self, db_path):
        "Header"
        fout = open('./output/output1.html', mode='w', encoding='utf-8')
        html = open('invoke_chapters.html', mode='r', encoding='utf-8')
        html_content = html.read()
        html_parts = html_content.split('<!-- SPLIT HERE -->')

        verbs_en = get_all_verbs_full(db_path, 'en', 'fr')

        fout.write(html_parts[0].replace('#NB#', str(len(verbs_en))))
        for verb in verbs_en:
            fout.write('<h3><a href="#' + str(verb['id']) + '">' + str(verb['nb']) + '. ' +
                       verb['root'] + verb['particle'] + ' &nbsp;(' + verb['pret'] +
                       verb['particle'] + ', ' + verb['part'] + verb['particle'] + ')</a>')
            if verb['irregular']:
                fout.write(' <b>*</b>')
            fout.write('</h3>\n')
        fout.write('\n\n')
        fout.write('<p>Les verbes avec une ast&eacute;risque <b>*</b> sont irr&eacute;guliers.</p>')
        fout.write('<mbp:pagebreak />')

        verbs_fr = get_all_verbs_full(db_path, 'fr', 'en')

        fout.write('<h2 id="liste_fr_en">Les ' + str(len(verbs_en)) +
                   ' verbes fondamentaux anglais à partir de leurs traductions en français</h2>')
        for verb in verbs_fr:
            fout.write('<h3>' + str(verb['nb']) + '. ' + verb['root'] + verb['particle'] +
                       ' : ')
            trans = ''
            nb_trans = 0
            for atrans in verb['trans']:
                if nb_trans == 0:
                    trans = ('<a href="#' + str(atrans) + '">' + verb['trans'][atrans]['base'] +
                             '</a>')
                    nb_trans += 1
                else:
                    trans = (trans + ', ' + '<a href="#' + str(atrans) + '">' +
                             verb['trans'][atrans]['base'] + '</a>')
                for verb_en in verbs_en:
                    if verb_en['id'] == atrans:
                        if verb_en['irregular']:
                            trans = trans + ' <b>*</b>'
                        break
            fout.write(trans + '</h3>\n')
        fout.write('<p>Les verbes avec une ast&eacute;risque <b>*</b> sont irr&eacute;guliers.</p>')
        fout.write('<mbp:pagebreak />')

        fout.write(html_parts[1].replace('#NB#', str(len(verbs_en))))

        fout.close()


    def footer_en(self, db_path):
        "Footer"
        fout = open('./output/output1.html', mode='a', encoding='utf-8')

        html = open('invoke_chapters.html', mode='r', encoding='utf-8')
        html_content = html.read()
        html_parts = html_content.split('<!-- SPLIT HERE -->')

        verbs_en = get_all_verbs_full(db_path, 'en', 'fr')
        fout.write(html_parts[2].replace('#NB#', str(len(verbs_en))))

        fout.close()


class Console:
    """
        Console
    """

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

    def mainloop(self, pre=None):
        "Mainloop"
        if pre is not None:
            if len(pre) > 0:
                for pre_com in pre:
                    self.interpret(pre_com)
        while not self.escape:
            self.cmd = input('>>> ')
            self.interpret()

    def interpret(self, pcmd=None):
        "Interpret"
        db_path = './output/example.db'

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
            InvokeDB.create_db(db_path)
            print("i Database recreated")
        elif self.cmd == 'select':
            exec_cmd(db_path, 'select', self.cmd_lang, self.cmd_order, self.cmd_auto, None,
                     self.cmd_debug)
        elif self.cmd == 'trans':
            exec_cmd(db_path, 'trans', self.cmd_lang, self.cmd_order, self.cmd_auto, self.cmd_to,
                     self.cmd_debug)
        elif self.cmd == 'count':
            print("i Returned results for lang [" + self.cmd_lang + "] = " +
                  str(exec_cmd(db_path, 'count', self.cmd_lang, self.cmd_order, self.cmd_auto)))
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
            #f = open('./output/output1.html', 'w')
            #f.close()
            # DEPRECATED ConjugateOldRenderer().header_en(db_path)
            print('i file output.html reset, header written')
        elif self.cmd == 'close':
            #DEPRECATED ConjugateOldRenderer().footer_en(db_path)
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
            print("i Current language is [" + self.cmd_lang + "], current translation is [" +
                  self.cmd_to + "]")
        elif self.cmd == 'stats':
            exec_stat(self.cmd_auto, self.cmd_debug)
        elif self.cmd in ['conjugate', 'conj', 'con']:
            guess = input('Enter a verb : ')
            conjugate(db_path, guess, self.cmd_lang, self.cmd_file, self.cmd_html)
            print("i Verb " + guess + " conjugated. Results can be found in " + guess.lower() +
                  ".txt")
        elif self.cmd in ['render']: # New Architecture
            verbs = get_all_verbs_full(db_path, 'en', 'fr')
            ConjugateTabularEnRenderer({'verbs' : verbs}).render('./output/output2.html')
        elif len(self.cmd.split(' ')) > 1:
            c_tab = self.cmd.split(' ')
            if c_tab[0] == 'select':
                if c_tab[1] in ['fr', 'it', 'eo', 'en', 'de']:
                    if c_tab[1] != self.cmd_lang: # order must be set to the language we call
                        exec_cmd(db_path, 'select', c_tab[1],
                                 (c_tab[1] + ".lang, " + c_tab[1] + ".base"), self.cmd_auto, None,
                                 self.cmd_debug)
                    else:
                        exec_cmd(db_path, 'select', c_tab[1], self.cmd_order, self.cmd_auto, None,
                                 self.cmd_debug)
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
            elif c_tab[0] in ['conjugate', 'conj', 'con']:
                conjugate(db_path, c_tab[1], self.cmd_lang, self.cmd_file, self.cmd_html)
                # print("i Verb " + c_tab[1] + " conjugated. Results can be found in "
                # + c_tab[1].lower() + ".txt")
            else:
                print("! Unknown command with parameters : " + self.cmd)
        elif self.cmd == '':
            pass
        else:
            print("! Unknown command : " + self.cmd)


if __name__ == '__main__':
    #commands = ['create', 'reset', 'html', 'lang en', 'con all', 'close', 'exit']
    COMMANDS = ['create', 'render', 'exit']
    Console(COMMANDS) #'con talk', 'con accept', 'exit'])
