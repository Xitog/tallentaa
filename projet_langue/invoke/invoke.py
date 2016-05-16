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

import sys
#import unicodedata
from invoke_data import InvokeDB, EnglishUtils
from invoke_model import RootCollection, Root, Verb
from invoke_view import VerbesAnglaisEssentielsRenderer, ConjugateTabularEnRenderer


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
        results = InvokeDB.get_all_verbs_full(db_path)
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
            verbs = InvokeDB.get_all_verbs_full(db_path, 'en', 'fr')
            roots = RootCollection()
            for verb in verbs:
                new_verb = roots.add_root(verb['root'], verb['irregular'], verb['base'], pret=verb['pret'], part=verb['part'], p3ps=verb['p3ps'], ing=verb['ing'])
                for trans in verb['trans']:
                    new_verb.add_translation(verb['trans'][trans]['base'])
            roots.build_reverse()
            ConjugateTabularEnRenderer({'verbs' : verbs, 'roots' : roots}).render('./output/output2.html')
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
