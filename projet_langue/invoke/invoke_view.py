import locale
locale.setlocale(locale.LC_ALL, '') #"fr_FR.UTF-8")

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
        fout.write('<a name="letters_' + lang + '"></a><table class="mono" id="index_' + lang + '"><tr class="title"><td>' + text + '</td></tr><tr><td class="trad">')
        for letter in sorted(dico, key=locale.strxfrm):
            fout.write('<a href="#' + lang + '_' + letter + '">' + letter.capitalize() + '</a>&nbsp;&nbsp;')
        fout.write('</td></tr></table><br><br>')   
    
    
    def sub_render_menu_verbs_by_letter_en(self, fout, roots):  # group verbs by letter
        """classement par lettre des verbes anglais"""
        self.sub_render_menu_verbs_by_letter(fout, roots, 'en', 'Que signifie ce verbe anglais ?', False)

        
    def sub_render_menu_verbs_by_letter_fr(self, fout, roots): # group verbs by letter
        """classement par lettre des verbes français"""
        self.sub_render_menu_verbs_by_letter(fout, roots, 'fr', 'Comment dire en anglais ?', True)
    
    
    def sub_render_menu_verbs_by_letter(self, fout, roots, lang, text, reverse):  # group verbs by letter
        """classement par lettre des verbes"""
        dico = roots.get_reverse_by_first_letter() if reverse else roots.get_roots_by_first_letter()
        fout.write('<div><h2 id="t' + lang + '">' + text + '</h2></div>')
        if lang == 'en': self.sub_render_menu_letters_en(fout, roots)
        elif lang == 'fr' : self.sub_render_menu_letters_fr(fout, roots)
        for letter in sorted(dico):
            fout.write('<a name="' + lang + '_' + letter + '"></a><table class="mono"><tr class="title"><td><a href="#letters_' + lang + '">&lt;&nbsp;&nbsp;</a>' + letter + '</td></tr><tr class="trad"><td>')
            nb_on_line = 0
            for roots_of_this_letter in sorted(dico[letter]): # on trie les roots
                if lang == 'en':
                    for base in sorted(roots_of_this_letter.get_all_verbs()):
                        verbs_of_this_letter = roots_of_this_letter.get_all_verbs()[base]
                        irr = '&nbsp;<b>*</b>' if roots_of_this_letter.irregular else ''
                        nb_on_line += len(verbs_of_this_letter.base)
                        nb_on_line = (nb_on_line + 2) if irr != '' else nb_on_line
                        if nb_on_line >= 80:
                            fout.write('<br>')
                            nb_on_line = 0
                        fout.write('<a href="#' + verbs_of_this_letter.base + '">' + verbs_of_this_letter.base + '</a>' + irr + '&nbsp;&nbsp;')
                elif lang == 'fr': # fr => en
                    fout.write(roots_of_this_letter + '&nbsp;:&nbsp;')
                    for verb_en in sorted(dico[letter][roots_of_this_letter]): # on trie les traductions chasser : drive out, hunt
                        fout.write('<a href="#' + verb_en.root.root + '">' + verb_en.base + '</a> ')
                    nb_on_line += (len(roots_of_this_letter) + 3)
                    if nb_on_line >= 80:
                        fout.write('<br>')
                        nb_on_line = 0
            fout.write('</td></tr></table><br><br>')

    
    def sub_render_verbs_en(self, fout, roots):
        """Verbes anglais (1 par tableau)"""
        fout.write('<div><h2 id="tverbes">Les verbes anglais</h2></div>')
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
            p3ps = root.forms['p3ps'] if root.root != 'be' else '<b>' + root.forms['p3ps'] + '</b>'
            pret = root.forms['pret'] if root.root != 'be' else '<b>' + root.forms['pret'] + '</b>'
            fout.write('<tr class="forms"><td>' + root.root +
                       '</td><td>' + pret + '</td><td>' + root.forms['part'] + '</td><td>' +
                       root.forms['ing'] + '</td><td>' + p3ps + '</td></tr>')
                       
            for verb_key in sorted(root.get_all_verbs()):
                verb = root.get_all_verbs()[verb_key]
                for trans_key in sorted(verb.get_all_trans()):
                    trans = verb.get_all_trans()[trans_key]
                    to = 'to ' if verb.base != 'must' else ''
                    str_trans = trans.get_target() + '<i> (' + trans.get_sens() + ')</i>' if trans.get_sens() is not None else trans.get_target()
                    fout.write('<tr class="trad"><td colspan="5">' + to +
                               verb.base + ' ' +
                               ' : ' + str_trans + '</td></tr>')
            fout.write('</table>')
            fout.write('<br><br>')
    

    def render(self, target):
        "render"
        roots = self.tables['roots']
        fout = open(target, mode='a', encoding='utf-8')
        fout.write("<div><h1>Verbes anglais essentiels</h1></div>")
        
        fout.write("<div><h2>Sommaire</h2></div>")
        fout.write("""
            <div><ol>
                <!--<li><a href="#tindex">Index des verbes</a></li>-->
                <li><a href="#tpronoms">Pronoms anglais</a></li>
                <li><a href="#tsyntaxe">Constructions syntaxiques du groupe verbal anglais</a></li>
                <li><a href="#tabreviations">Abréviations des verbes anglais</a></li>
                <li><a href="#tnegations">Constructions contractées de la négation</a></li>
                <li><a href="#ten">Que signifie ce verbe anglais ?</a></li>
                <li><a href="#tfr">Comment dire en anglais ?</a></li>
                <li><a href="#tverbes">Les verbes anglais</a></li>
            </ol></div>
                   """)
        #fout.write('<div><h2 id="tindex">Index des verbes</h2></div>')
        
        fout.write(self.get_table_pronoms())
        fout.write(self.get_table_constructions())
        fout.write(self.get_table_abreviations())
        fout.write(self.get_table_negations())
        self.sub_render_menu_verbs_by_letter_en(fout, roots)
        self.sub_render_menu_verbs_by_letter_fr(fout, roots)
        self.sub_render_verbs_en(fout, roots)
        fout.close()


    def get_table_constructions(self):
        c = """
            <div><h2 id="tsyntaxe">Constructions syntaxiques du groupe verbal anglais</h2></div>
            <table class="mono" id="cons">
                <tr><th>Construction</th><th>Forme</th><th>Exemple</th></tr>
                <tr><td>Présent</td><td>base verbale ou 3<sup>e</sup> pers. sing.</td><td>They talk. She talks to Samantha.</td></tr>
                <tr><td>Prétérit</td><td>prétérit</td><td>She talked to Samantha.</td></tr>
                <tr><td>Futur</td><td>will / shall + base verbale</td><td>She will talk to Samantha.</td></tr>
                <tr><td>Continu</td><td>be + participe présent</td><td>She is talking to Samantha.</td></tr>
                <tr><td>Parfait</td><td>have + participe passé</td><td>She have talked to Samantha.</td></tr>
                <tr><td>Passif</td><td>be + participe passé</td><td>The letter is written by Jack.</td></tr>
                <tr><td>Autres</td><td>would / should + base verbale<br>may + base verbale<br>might + base verbale<br>can + base verbale<br>could + base verbale</td><td>She should talk to Samantha.<br>She may talk to Samantha.<br>She might talk to Samantha.<br>She can talk to Samantha.<br>She could talk to Samantha.</td></tr>
            </table>
            <br><br>
            <div><h2>Constructions des 5 formes des verbes anglais</h2></div>
            <table class="mono" id="forms">
                <tr><th>Forme</th><th>Construction</th><th>Exemple</th></tr>
                <tr><td>Présent, sauf 3<sup>e</sup> pers. sing.</td><td>base verbale</td><td>talk &#8594; talk</td></tr>
                <tr><td>Présent, 3<sup>e</sup> pers. sing.</td><td>base verbale +s</td><td>talk &#8594; talks</td></tr>
                <tr><td>Prétérit</td><td>base verbale +ed</td><td>talk &#8594; talked</td></tr>
                <tr><td>Participe passé</td><td>base verbale +ed</td><td>talk &#8594; talked</td></tr>
                <tr><td>Participe présent</td><td>base verbale +ing</td><td>talk &#8594; talking</td></tr>
            </table>
            <br><br>
        """
        return c


    def get_table_pronoms(self):
        c = """
        <div><h2 id="tpronoms">Pronoms anglais</h2></div>
        <table class="mono" id="pronoms">
            <thead>
                <tr><th>Personne, nombre et genre</th><th>Sujet</th><th>Objet</th><th>Possessif</th></tr>
            </thead>
            <tbody>
                <tr><td>1<sup>ère</sup> personne du singulier</td><td>I <i>(je)</i></td><td>me <i>(moi)</i></td><td>mine <i>(le mien)</i></td></tr>
                <tr><td>2<sup>e</sup> personne du singulier</td><td>you <i>(tu)</i></td><td>you <i>(toi)</i></td><td>yours <i>(le tien)</i></td></tr>
                <tr><td>3<sup>e</sup> personne du singulier, féminin</td><td>she <i>(elle)</i></td><td>her <i>(la)</i></td><td>hers <i>(le sien)</i></td></tr>
                <tr><td>3<sup>e</sup> personne du singulier, masculin</td><td>he <i>(il)</i></td><td>him <i>(le)</i></td><td>his <i>(le sien)</i></td></tr>
                <tr><td>3<sup>e</sup> personne du singulier, neutre</td><td>it</td><td>it</td><td>its own <i>(le sien)</i></td></tr>
                <tr><td>1<sup>ère</sup> personne du pluriel</td><td>we <i>(nous)</i></td><td>us <i>(nous)</i></td><td>ours <i>(le nôtre)</i></td></tr>
                <tr><td>2<sup>e</sup> personne du pluriel</td><td>you <i>(vous)</i></td><td>you <i>(vous)</i></td><td>yours <i>(le vôtre)</i></td></tr>
                <tr><td>3<sup>e</sup> personne du pluriel</td><td>they <i>(elles ou ils)</i></td><td>them <i>(les)</i></td><td>theirs <i>(les leur)</i></td></tr>
                <tr><td>pronom indéfini</td><td>one <i>(on)</i></td><td>one</td><td>one's own</td></tr>
            </tbody>
        </table>
        <br><br>
        """
        return c
        
    
    def get_table_abreviations(self):
        c = """
        <div><h2 id="tabreviations">Abréviations des verbes anglais</h2></div>
        <table class="mono" id="abreviations">
            <thead>
                <tr><th>Construction simple</th><th>Construction contractée</th></tr>
            </thead>
            <tbody>
                <tr><td>am</td><td>'m</td></tr>
                <tr><td>is</td><td><b>'s</b></td></tr>
                <tr><td>are</td><td>'re</td></tr>
                <tr><td>have</td><td>'ve</td></tr>
                <tr><td>has</td><td><b>'s</b></td></tr>
                <tr><td>had</td><td><b>'d</b></td></tr>
                <tr><td>will</td><td><b>'ll</b></td></tr>
                <tr><td>shall</td><td><b>'ll</b></td></tr>
                <tr><td>would</td><td><b>'d</b></td></tr>
            </tbody>
        </table>
        <br><br>
        """
        return c
        
    
    def get_table_negations(self):
        c = """
        <div><h2 id="tnegations">Constructions contractées de la négation</h2></div>
        <table class="mono" id="negations">
            <thead>
                <tr><th>Construction simple</th><th>Construction contractée</th></tr>
            </thead>
            <tbody>
                <tr><td>do not</td><td>don't</td></tr>
                <tr><td>does not</td><td>doesn't</td></tr>
                <tr><td>did not</td><td>didn't</td></tr>
                <tr><td>has not</td><td>hasn't</td></tr>
                <tr><td>have not</td><td>haven't</td></tr>
                <tr><td>will not</td><td><b>won't</b></td></tr>
                <tr><td>would not</td><td>wouldn't</td></tr>
                <tr><td>shall not</td><td><b>shan't</b></td></tr>
                <tr><td>should not</td><td>shouldn't</td></tr>
                <tr><td>are not</td><td>aren't</td></tr>
                <tr><td>was not</td><td>wasn't</td></tr>
                <tr><td>were not</td><td>weren't</td></tr>
                <tr><td><b>cannot</b></td><td><b>can't</b></td></tr>
                <tr><td>might not</td><td>mightn't</td></tr>
                <tr><td>need not</td><td>needn't</td></tr>
            </tbody>
        </table>
        <br><br>
        """
        return c
        
    
    def get_table_sens_emplois(self):
        c = """
        """
        return c
        
    
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
                <title>Verbes anglais essentiels</title>
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
                    
                    table {
                        border: 1px solid rgb(91, 155, 213);
                        /*border-collapse: collapse;*/
                        border-spacing: 0;
                        border-radius: 5px;
                        
                        font-size: 18px;
                        font-family: Calibri;
                    }
                    
                    table.all {
                        width: 32cm; /* 20 */
                        margin: auto;
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

                    b {
                        color: rgb(213,91,155);
                    }

                    ol {
                        font-size: 18px;
                        font-family: Calibri;
                    }
                    
                    table.mono {
                        width: 20cm;
                        margin: auto;
                    }
                    
                    table.mono td {
                        border-right: 1px solid rgb(91, 155, 213);
                        text-align: center;
                    }
                    
                    table.mono th, tr.title {
                        color: rgb(255, 255, 255);
                        background-color: rgb(91, 155, 213);
                        font-weight: bold;
                        font-size: 22px;
                    }
                    
                    #index_en tr.title td, #index_fr tr.title {
                        background-color: rgb(146, 208, 80);
                    }
                    
                    #index_en, #index_fr {
                        border: 1px solid rgb(146, 208, 80);
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
                    
                    table td:last-child {
                        border-right: none;
                    }
                    
                    /* construction table */
                    
                    #cons, #forms {
                        border: 1px solid rgb(91, 155, 213);
                    }
                    
                    #cons td, #forms td {
                        border-right: 1px solid rgb(91, 155, 213);
                        text-align: left;
                    }
                    
                    #cons tr td:last-child , #forms tr td:last-child {
                        border-right: none;
                        font-style: italic;
                    }
                    
                    #cons th, #forms th {
                        text-align: center;
                        font-size: 22px;
                        font-weight: bold;
                        background-color: rgb(91, 155, 213);
                        color: white;
                    }
                    
                    #cons tr td:first-child, #forms tr td:first-child {
                        font-size: 22px;
                    }
                    
                    #cons tr:nth-child(2n+1) , #forms tr:nth-child(2n+1), #pronoms tr:nth-child(2n+1), #abreviations tr:nth-child(2n+1), #negations tr:nth-child(2n+1) {
                        background-color: rgb(146, 208, 80); /*rgb(213,91,94);*/
                        color: white;
                    }
                    
                    #pronoms td:first-child {
                        text-align: left;
                        padding-left: 4em;
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


    def conjugate(self, db_path, verb, lang, onfile=False, html=False):
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


    def conjugate_en(self, verb, onfile=False, html=False, info=None, number=None):
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

