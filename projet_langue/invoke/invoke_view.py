
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
    """New version of my final renderer"""


    def sub_render_menu_letters_en(self, fout, roots):
        """lettres en"""
        self.sub_render_menu_by_letters(fout, roots, 'en', 'Accès par la première lettre du verbe anglais', False)
    
    
    def sub_render_menu_letters_fr(self, fout, roots):
        """lettres fr"""
        self.sub_render_menu_by_letters(fout, roots, 'fr', 'Accès par la première lettre du verbe français', True)

        
    def sub_render_menu_by_letters(self, fout, roots, lang, text, reverse):
        """by letters"""
        dico = roots.get_reverse_by_first_letter() if reverse else roots.get_roots_by_first_letter()
        fout.write('<a name="letters_' + lang + '"></a><table class="mono"><tr class="title"><td>' + text + '</td></tr><tr><td class="trad">')
        for letter in sorted(dico):
            fout.write('<a href="#' + lang + '_' + letter + '">' + letter.capitalize() + '</a>&nbsp;&nbsp;')
        fout.write('</td></tr></table><br><br>')   
    
    
    def sub_render_menu_verbs_by_letter_en(self, fout, roots):
        """classement par lettre des verbes anglais"""
        self.sub_render_menu_verbs_by_letter(fout, roots, 'en', 'Que signifie ce verbe anglais ?', False)

        
    def sub_render_menu_verbs_by_letter_fr(self, fout, roots):
        """classement par lettre des verbes français"""
        self.sub_render_menu_verbs_by_letter(fout, roots, 'fr', 'Comment dire en anglais ?', True)
    
    
    def sub_render_menu_verbs_by_letter(self, fout, roots, lang, text, reverse):
        """classement par lettre des verbes"""
        dico = roots.get_reverse_by_first_letter() if reverse else roots.get_roots_by_first_letter()
        fout.write('<div><h2>' + text + '</h2></div>')
        for letter in sorted(dico):
            fout.write('<a name="' + lang + '_' + letter + '"></a><table class="mono"><tr class="title"><td><a href="#letters_' + lang + '">&lt;&nbsp;&nbsp;</a>' + letter + '</td></tr><tr class="trad"><td>')
            nb_on_line = 0
            for roots_of_this_letter in dico[letter]:
                if lang == 'en':
                    for base in sorted(roots_of_this_letter.get_all_verbs()):
                        verbs_of_this_letter = roots_of_this_letter.get_all_verbs()[base]
                        irr = '&nbsp;<b class="s">*</b>' if roots_of_this_letter.irregular else ''
                        nb_on_line += len(verbs_of_this_letter.base)
                        nb_on_line = (nb_on_line + 2) if irr != '' else nb_on_line
                        if nb_on_line >= 80:
                            fout.write('<br>')
                            nb_on_line = 0
                        fout.write('<a href="#' + verbs_of_this_letter.base + '">' + verbs_of_this_letter.base + '</a>' + irr + '&nbsp;&nbsp;')
                elif lang == 'fr':
                    fout.write(roots_of_this_letter + '&nbsp;:&nbsp;')
                    for verb_en in dico[letter][roots_of_this_letter]:
                        fout.write('<a href="#' + verb_en.root.root + '">' + verb_en.base + '</a> ')
                    nb_on_line += (len(roots_of_this_letter) + 3)
                    if nb_on_line >= 80:
                        fout.write('<br>')
                        nb_on_line = 0
            fout.write('</td></tr></table><br><br>')

    
    def sub_render_verbs_en(self, fout, roots):
        """Verbes anglais (1 par tableau)"""
        fout.write('<div><h2>Les verbes anglais</h2></div>')
        for root_key in sorted(roots.get_roots()):
            root = roots.get_roots()[root_key]
            fout.write('<a name="' + root.root + '"></a>' + '<table class="mono">\n')
            irr = ''
            if root.irregular:
                irr = ' <b>*</b>'
            fout.write('<tr class="title"><td colspan="5"><a href="#en_' + root.first_letter + '">&lt;&nbsp;&nbsp;</a>' + root.root + irr + '</td></tr>')
            fout.write('<tr class="temps"><td>Présent</td><td>Prétérit</td>' +
                       '<td>Participe passé</td><td>Participe présent</td>' +
                       '<td>3e pers. sing.</td></tr>')
            p3ps = root.forms['p3ps'] if root.root != 'be' else '<b class="s">' + root.forms['p3ps'] + '</b>'
            pret = root.forms['pret'] if root.root != 'be' else '<b class="s">' + root.forms['pret'] + '</b>'
            fout.write('<tr class="forms"><td>' + root.root +
                       '</td><td>' + pret + '</td><td>' + root.forms['part'] + '</td><td>' +
                       root.forms['ing'] + '</td><td>' + p3ps + '</td></tr>')
                       
            for verb_key in sorted(root.get_all_verbs()):
                verb = root.get_all_verbs()[verb_key]
                for trans_key in sorted(verb.get_all_trans()):
                    trans = verb.get_all_trans()[trans_key]
                    to = 'to ' if verb.base != 'must' else ''
                    fout.write('<tr class="trad"><td colspan="5">' + to +
                               verb.base + ' ' +
                               ' : ' + trans + '</td></tr>')
            fout.write('</table>')
            fout.write('<br><br>')
    

    def render(self, target):
        "render"
        roots = self.tables['roots']
        fout = open(target, mode='a', encoding='utf-8')
        fout.write("<div><h1>Verbes anglais essentiels</h1></div>")

  
        self.sub_render_menu_letters_en(fout, roots)
        self.sub_render_menu_letters_fr(fout, roots)
        self.sub_render_menu_verbs_by_letter_en(fout, roots)
        self.sub_render_menu_verbs_by_letter_fr(fout, roots)
        self.sub_render_verbs_en(fout, roots)
        fout.close()


class ConjugateTabularEnRenderer(AbstractRenderer):
    """
        Debug renderer : Simple tabular renderer for English in html
        Affiche tout dans un tableau avec les id.
    """

    def header(self, fout):
        "header"
        fout.write("""
            <html>
            <head>
                <meta charset="utf-8">
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
                    
                    h2 {
                        font-size: 28px;
                        font-family: Calibri;
                        color: black;
                        border-bottom: 1px solid rgb(146, 208, 80);
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
                        /*border-collapse: collapse;*/
                        border-spacing: 0;
                        border-radius: 5px;
                        /*-webkit-border-radius: 5px;*/
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

                    table.mono tr.forms td {
                        border-bottom: 1px solid rgb(91, 155, 213);
                    }

                    table.mono tr.trad td {
                        text-align: left;
                    }

                    table.mono b.s {
                        color: rgb(213,91,155);
                    }
                    
                    table td:last-child {
                        border-right: none;
                    }
                    
                </style>
            </head>
            <body>
        """)


    def footer(self, fout):
        "footer"
        fout.write("</body></html>")


    def render(self, target):
        "render"
        verbs = self.tables['verbs']

        fout = open(target, mode='w', encoding='utf-8')
        self.header(fout)
        fout.close()
        xtables = {}
        #import copy
        #xtables['verbs'] = copy.deepcopy(verbs)
        VerbesAnglaisEssentielsRenderer({'roots' : self.tables['roots']}).render(target)
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
        fout.write('<div><h1>' + str(nb_root) + ' bases, ' + str(nb_cons) + ' verbs, ' + str(nb_trad-1) +
                   ' traductions.</h1></div>')
        self.footer(fout)
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

