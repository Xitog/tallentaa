import os
import sqlite3

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
        connection.execute(get_create_table_verbs())
        connection.execute(get_create_table_trans())
        connection.execute(get_create_table_verbs_en())

        # Tables filling
        content = get_verbs()
        verbes_id = InvokeDB.check_content_verbs(content)
        connection.executemany('INSERT INTO voc_verbs VALUES (?,?,?,?,?)', content)

        content_verbs_en = get_irregular_verbs()
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

        content = get_traductions()
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
        for row in connection.execute(get_select_translation_en()):
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
        for row in connection.execute(get_select_table_verbs_fr()):
            i += 1
            res_file.write(str(i) + ". #" + str(row[0]) + " " + row[1] + "\n")

        res_file.write("\n\n\n")
        res_file.write("------------------------------------------------------------------------\n")
        res_file.write("Verbes non traduits\n")
        res_file.write("------------------------------------------------------------------------\n")
        i = 0
        for row in connection.execute(get_select_untranslated_en()):
            i += 1
            res_file.write(str(i) + ". #" + str(row[0]) + " " + row[1] + "\n")

        from time import gmtime, strftime
        res_file.write("\n\nLast edit on " + strftime("%Y-%m-%d %H:%M:%S"))  #, gmtime())
        res_file.close()
        
    @staticmethod
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
    @staticmethod
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
        irregulars = InvokeDB.get_all_verbs_en(db_path)
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

    
def get_create_table_verbs():
    c = "CREATE TABLE IF NOT EXISTS voc_verbs ( id int(11) NOT NULL, lang varchar(2) NOT NULL, base varchar(50) NOT NULL, surtype varchar(30) NOT NULL, lvl int(11) DEFAULT '1', PRIMARY KEY (`id`) ) "
    return c

def get_create_table_trans():
    c = "CREATE TABLE IF NOT EXISTS voc_translate ( id int(11) NOT NULL, de int(11) NOT NULL, vers int(11) NOT NULL, sens varchar(100) DEFAULT NULL, usage varchar(100) DEFAULT NULL, PRIMARY KEY (`id`) ) "
    return c
    
def get_create_table_verbs_en():
    c = "CREATE TABLE IF NOT EXISTS voc_verbs_en ( id int(11) NOT NULL, base varchar(50) NOT NULL, pret varchar(50) NOT NULL, part varchar(50) NOT NULL )"
    return c
    
def get_select_translation_en():
    c = "SELECT fr.base, en.base, t.sens FROM voc_verbs as fr, voc_verbs as en, voc_translate as t WHERE fr.id = t.de AND en.id = t.vers AND fr.lang = 'fr' AND en.lang = 'en' ORDER BY fr.lang, fr.base"
    return c
    
def get_select_untranslated_en():
    c = "SELECT fr.id, fr.base FROM voc_verbs as fr WHERE fr.lang = 'fr' AND fr.id NOT IN (SELECT t.de FROM voc_translate as t) ORDER BY fr.lang, fr.base"
    return c

def get_select_table_verbs_fr():
    c = "SELECT fr.id, fr.base FROM voc_verbs as fr WHERE fr.lang = 'fr' ORDER BY fr.lang, fr.base"
    return c

def get_verbs():

    content = [
        # VAGUE 1
        (1, 'fr', 'ouvrir', 'verb', 1),
        (2, 'fr', 'voyager', 'verb', 1),
        (3, 'fr', 'vouloir', 'verb', 1),
        (5, 'fr', 'voler', 'verb', 1),
        (6, 'fr', 'voir', 'verb', 1),
        (7, 'fr', 'vivre', 'verb', 1),
        (8, 'fr', 'visiter', 'verb', 1),
        (9, 'fr', 'venir', 'verb', 1),
        (10, 'fr', 'vendre', 'verb', 1),
        (11, 'fr', 'utiliser', 'verb', 1),
        (12, 'fr', 'trouver', 'verb', 1),
        (13, 'fr', 'travailler', 'verb', 1),
        (14, 'fr', 'traduire', 'verb', 1),
        (15, 'fr', 'tourner', 'verb', 1),
        (16, 'fr', 'toucher', 'verb', 1),
        (17, 'fr', 'tomber', 'verb', 1),
        (26, 'fr', 'raconter', 'verb', 1),
        (27, 'fr', 'recevoir', 'verb', 1),
        (28, 'fr', 'regarder', 'verb', 1),
        (29, 'fr', 'remercier', 'verb', 1),
        (30, 'fr', 'rencontrer', 'verb', 1),
        (31, 'fr', 'répondre', 'verb', 1),
        (32, 'fr', 'rester', 'verb', 1),
        (33, 'fr', 'réussir', 'verb', 1),
        (34, 'fr', 'réveiller (se)', 'verb', 1),
        (35, 'fr', 'rire', 'verb', 1),
        (36, 'fr', 'occuper (s\')', 'verb', 1),
        (37, 'fr', 'sauter', 'verb', 1),
        (38, 'fr', 'savoir', 'verb', 1),
        (39, 'fr', 'reposer (se)', 'verb', 1),
        (40, 'fr', 'souvenir (se)', 'verb', 1),
        (41, 'fr', 'sentir', 'verb', 1),
        (42, 'fr', 'souffrir', 'verb', 1),
        (43, 'fr', 'souhaiter', 'verb', 1),
        (44, 'fr', 'suivre', 'verb', 1),
        (45, 'fr', 'tenir', 'verb', 1),
        (46, 'fr', 'tirer', 'verb', 1),
        (47, 'fr', 'mettre', 'verb', 1),
        (48, 'fr', 'montrer', 'verb', 1),
        (49, 'fr', 'mourir', 'verb', 1),
        (50, 'fr', 'nager', 'verb', 1),
        (51, 'fr', 'naître', 'verb', 1),
        (52, 'fr', 'oublier', 'verb', 1),
        (53, 'fr', 'pardonner', 'verb', 1),
        (54, 'fr', 'parler', 'verb', 1),
        (55, 'fr', 'partir', 'verb', 1),
        (56, 'fr', 'passer', 'verb', 1),
        (57, 'fr', 'payer', 'verb', 1),
        (58, 'fr', 'penser', 'verb', 1),
        (59, 'fr', 'perdre', 'verb', 1),
        (60, 'fr', 'permettre', 'verb', 1),
        (61, 'fr', 'plaire', 'verb', 1),
        (62, 'fr', 'pleurer', 'verb', 1),
        (63, 'fr', 'porter', 'verb', 1),
        (64, 'fr', 'pouvoir', 'verb', 1),
        (65, 'fr', 'prendre', 'verb', 1),
        (66, 'fr', 'présenter (se)', 'verb', 1),
        (67, 'fr', 'promettre', 'verb', 1),
        (68, 'fr', 'quitter', 'verb', 1),
        (69, 'fr', 'marcher', 'verb', 1),
        (70, 'fr', 'manquer', 'verb', 1),
        (71, 'fr', 'manger', 'verb', 1),
        (72, 'fr', 'lire', 'verb', 1),
        (73, 'fr', 'lever (se)', 'verb', 1),
        (74, 'fr', 'laver', 'verb', 1),
        (75, 'fr', 'jouer', 'verb', 1),
        (76, 'fr', 'jeter', 'verb', 1),
        (77, 'fr', 'inviter', 'verb', 1),
        (78, 'fr', 'habiter', 'verb', 1),
        (79, 'fr', 'habiller (s\')', 'verb', 1),
        (80, 'fr', 'goûter', 'verb', 1),
        (81, 'fr', 'gagner', 'verb', 1),
        (82, 'fr', 'finir', 'verb', 1),
        (83, 'fr', 'fermer', 'verb', 1),
        (84, 'fr', 'faire', 'verb', 1),
        (85, 'fr', 'étudier', 'verb', 1),
        (86, 'fr', 'être', 'verb', 1),
        (87, 'fr', 'essayer', 'verb', 1),
        (88, 'fr', 'espérer', 'verb', 1),
        (89, 'fr', 'envoyer', 'verb', 1),
        (90, 'fr', 'entendre', 'verb', 1),
        (91, 'fr', 'enseigner', 'verb', 1),
        (92, 'fr', 'écrire', 'verb', 1),
        (93, 'fr', 'écouter', 'verb', 1),
        (94, 'fr', 'dormir', 'verb', 1),
        (95, 'fr', 'dire', 'verb', 1),
        (96, 'fr', 'devoir', 'verb', 1),
        (97, 'fr', 'demander', 'verb', 1),
        (98, 'fr', 'danser', 'verb', 1),
        (99, 'fr', 'cuire', 'verb', 1),
        (100, 'fr', 'croire', 'verb', 1),
        (101, 'fr', 'crier', 'verb', 1),
        (102, 'fr', 'créer', 'verb', 1),
        (103, 'fr', 'coûter', 'verb', 1),
        (104, 'fr', 'courir', 'verb', 1),
        (105, 'fr', 'construire', 'verb', 1),
        (106, 'fr', 'connaître', 'verb', 1),
        (107, 'fr', 'conduire', 'verb', 1),
        (108, 'fr', 'compter', 'verb', 1),
        (109, 'fr', 'comprendre', 'verb', 1),
        (110, 'fr', 'commencer', 'verb', 1),
        (111, 'fr', 'choisir', 'verb', 1),
        (112, 'fr', 'chercher', 'verb', 1),
        (113, 'fr', 'chanter', 'verb', 1),
        (114, 'fr', 'changer', 'verb', 1),
        (115, 'fr', 'casser', 'verb', 1),
        (116, 'fr', 'cacher', 'verb', 1),
        (117, 'fr', 'brûler', 'verb', 1),
        (118, 'fr', 'bouger', 'verb', 1),
        (119, 'fr', 'boire', 'verb', 1),
        (120, 'fr', 'bavarder', 'verb', 1),
        (121, 'fr', 'avoir peur', 'verb', 1),
        (122, 'fr', 'avoir confiance', 'verb', 1),
        (123, 'fr', 'avoir besoin', 'verb', 1),
        (124, 'fr', 'avoir', 'verb', 1),
        (125, 'fr', 'attendre', 'verb', 1),
        (126, 'fr', 'arriver', 'verb', 1),
        (127, 'fr', 'arrêter', 'verb', 1),
        (128, 'fr', 'apprendre', 'verb', 1),
        (129, 'fr', 'apprécier', 'verb', 1),
        (130, 'fr', 'appeler', 'verb', 1),
        (132, 'fr', 'aimer', 'verb', 1),
        (133, 'fr', 'acheter', 'verb', 1),
        (134, 'fr', 'aider', 'verb', 1),
        (135, 'fr', 'donner', 'verb', 1),
        (136, 'fr', 'revenir', 'verb', 1),
        (137, 'fr', 'aller', 'verb', 1),
        (138, 'fr', 'sortir', 'verb', 1),
        (139, 'fr', 'entrer', 'verb', 1),
        (140, 'fr', 'allumer', 'verb', 1),
        (141, 'fr', 'éteindre', 'verb', 1),
        (142, 'fr', 'proposer', 'verb', 1),
        (143, 'fr', 'décider', 'verb', 1),
        (144, 'fr', 'poser', 'verb', 1),
        (145, 'fr', 'réduire', 'verb', 1),
        (146, 'fr', 'remplir', 'verb', 1),
        (147, 'fr', 'monter', 'verb', 1),
        (148, 'fr', 'descendre', 'verb', 1),
        (150, 'fr', 'asseoir (s\')', 'verb', 1),
        (151, 'fr', 'enlever', 'verb', 1),

        # VAGUE 2
        (152, 'fr', 'ajouter', 'verb', 2),
        (153, 'fr', 'attraper', 'verb', 2),
        (154, 'fr', 'augmenter', 'verb', 2),
        (155, 'fr', 'briller', 'verb', 2),
        (156, 'fr', 'chasser', 'verb', 2),
        (158, 'fr', 'bâtir', 'verb', 2),
        (159, 'fr', 'découvrir', 'verb', 2),
        (160, 'fr', 'désirer', 'verb', 2),
        (161, 'fr', 'deviner', 'verb', 2),
        (162, 'fr', 'diminuer', 'verb', 2),
        (163, 'fr', 'discuter', 'verb', 2),
        (164, 'fr', 'disparaître', 'verb', 2),
        (165, 'fr', 'durer', 'verb', 2),
        (166, 'fr', 'être d\'accord', 'verb', 2),
        (167, 'fr', 'gémir', 'verb', 2),
        (168, 'fr', 'glisser', 'verb', 2),
        (169, 'fr', 'intéresser', 'verb', 2),
        (170, 'fr', 'lever', 'verb', 2),
        (171, 'fr', 'louer', 'verb', 2),
        (172, 'fr', 'nourrir', 'verb', 2),
        (173, 'fr', 'partager', 'verb', 2),
        (174, 'fr', 'pendre', 'verb', 2),
        (175, 'fr', 'plier', 'verb', 2),
        (176, 'fr', 'plonger', 'verb', 2),
        (177, 'fr', 'pousser', 'verb', 2),
        (178, 'fr', 'prêter', 'verb', 2),
        (179, 'fr', 'produire', 'verb', 2),
        (180, 'fr', 'réfléchir', 'verb', 2),
        (181, 'fr', 'retenir', 'verb', 2),
        (182, 'fr', 'rêver', 'verb', 2),
        (183, 'fr', 'valoir', 'verb', 2),
        (184, 'fr', 'vider', 'verb', 2),
        (185, 'fr', 'devenir', 'verb', 2),
        (186, 'fr', 'lancer', 'verb', 2),
        (187, 'fr', 'apporter', 'verb', 2),
        
        # VAGUE 3 : d'après la liste des verbes irréguliers
        (188, 'fr', 'couper', 'verb', 2),
        (189, 'fr', 'dessiner', 'verb', 2),
        (190, 'fr', 'garder', 'verb', 2),
        (191, 'fr', 'mener', 'verb', 2),
        (192, 'fr', 'laisser', 'verb', 2),
        (193, 'fr', 'mentir', 'verb', 2),
        (194, 'fr', 'signifier', 'verb', 2),
        (195, 'fr', 'dépenser', 'verb', 2),
        (196, 'fr', 'être debout', 'verb', 2),
        (197, 'fr', 'être assis', 'verb', 2),
        # VAGUE 4
        (201, 'fr', 'tuer', 'verb', 4),
        (202, 'fr', 'blesser', 'verb', 4),
        (203, 'fr', 'combattre', 'verb', 4),
        
        (100001, 'en', 'open', 'verb', 1),
        (100002, 'en', 'travel', 'verb', 1),
        (100003, 'en', 'want', 'verb', 1),
        (100005, 'en', 'fly', 'verb', 1),
        (100006, 'en', 'see', 'verb', 1),
        (100007, 'en', 'live', 'verb', 1),
        (100008, 'en', 'visit', 'verb', 1),
        (100009, 'en', 'come', 'verb', 1),
        (100010, 'en', 'sell', 'verb', 1),
        (100011, 'en', 'use', 'verb', 1),
        (100012, 'en', 'find', 'verb', 1),
        (100013, 'en', 'work', 'verb', 1),
        (100014, 'en', 'translate', 'verb', 1),
        (100015, 'en', 'turn', 'verb', 1),
        (100016, 'en', 'touch', 'verb', 1),
        (100017, 'en', 'fall', 'verb', 1),
        (100026, 'en', 'tell', 'verb', 1),
        (100027, 'en', 'receive', 'verb', 1),
        (100028, 'en', 'watch', 'verb', 1),

        (190028, 'en', 'look at', 'verb', 1),

        (100029, 'en', 'thank', 'verb', 1),
        (100030, 'en', 'meet', 'verb', 1),
        (100031, 'en', 'answer', 'verb', 1),
        (100032, 'en', 'stay', 'verb', 1),
        (100033, 'en', 'success', 'verb', 1),
        (100034, 'en', 'wake up', 'verb', 1),
        (100035, 'en', 'laugh', 'verb', 1),
        (100036, 'en', 'take care', 'verb', 1),
        (100037, 'en', 'jump', 'verb', 1),
        (100038, 'en', 'know', 'verb', 1),
        (100039, 'en', 'rest', 'verb', 1),
        (100040, 'en', 'remember', 'verb', 1),
        (100041, 'en', 'smell', 'verb', 1),
        (100042, 'en', 'suffer', 'verb', 1),
        (100043, 'en', 'wish', 'verb', 1),
        (100044, 'en', 'follow', 'verb', 1),
        (100045, 'en', 'hold', 'verb', 1),
        (100046, 'en', 'pull', 'verb', 1),
        (100047, 'en', 'put', 'verb', 1),
        (100048, 'en', 'show', 'verb', 1),
        (100049, 'en', 'die', 'verb', 1),
        (100050, 'en', 'swim', 'verb', 1),
        (100051, 'en', 'be born', 'verb', 1),
        (100052, 'en', 'forget', 'verb', 1),
        (100053, 'en', 'forgive', 'verb', 1),
        (100054, 'en', 'speak', 'verb', 1),
        (190054, 'en', 'talk', 'verb', 1),
        (100055, 'en', 'go', 'verb', 1),
        (100056, 'en', 'pass', 'verb', 1),
        (100057, 'en', 'pay', 'verb', 1),
        (100058, 'en', 'think', 'verb', 1),
        (100059, 'en', 'lose', 'verb', 1),
        (100060, 'en', 'allow', 'verb', 1),
        (100061, 'en', 'please', 'verb', 1),
        (100062, 'en', 'cry', 'verb', 1),
        (100063, 'en', 'carry', 'verb', 1),
        (100064, 'en', 'can', 'verb', 1),
        (100065, 'en', 'take', 'verb', 1),
        (100066, 'en', 'introduce', 'verb', 1),
        (100067, 'en', 'pledge', 'verb', 1),
        (100068, 'en', 'leave', 'verb', 1),
        (100069, 'en', 'walk', 'verb', 1),
        (100070, 'en', 'miss', 'verb', 1),
        (100071, 'en', 'eat', 'verb', 1),
        (100072, 'en', 'read', 'verb', 1),
        (100073, 'en', 'stand up', 'verb', 1),

        (190073, 'en', 'rise', 'verb', 1),

        (100074, 'en', 'wash', 'verb', 1),
        (100075, 'en', 'play', 'verb', 1),
        (100076, 'en', 'throw', 'verb', 1),
        (100077, 'en', 'invite', 'verb', 1),
        (100078, 'en', 'live in', 'verb', 1),
        (100079, 'en', 'dress', 'verb', 1),
        (100080, 'en', 'taste', 'verb', 1),
        (100081, 'en', 'win', 'verb', 1),
        (100082, 'en', 'finish', 'verb', 1),
        (100083, 'en', 'close', 'verb', 1),
        (100084, 'en', 'do', 'verb', 1),

        (190084, 'en', 'make', 'verb', 1),

        (100085, 'en', 'study', 'verb', 1),
        (100086, 'en', 'be', 'verb', 1),
        (100087, 'en', 'try', 'verb', 1),
        (100088, 'en', 'hope', 'verb', 1),
        (100089, 'en', 'send', 'verb', 1),
        (100090, 'en', 'hear', 'verb', 1),
        (100091, 'en', 'teach', 'verb', 1),
        (100092, 'en', 'write', 'verb', 1),
        (100093, 'en', 'listen', 'verb', 1),
        (100094, 'en', 'sleep', 'verb', 1),
        (100095, 'en', 'say', 'verb', 1),
        (100096, 'en', 'must', 'verb', 1),
        (100097, 'en', 'ask', 'verb', 1),
        (100098, 'en', 'dance', 'verb', 1),
        (100099, 'en', 'cook', 'verb', 1),
        (100100, 'en', 'believe', 'verb', 1),
        (100101, 'en', 'shout', 'verb', 1),
        (100102, 'en', 'create', 'verb', 1),
        (100103, 'en', 'cost', 'verb', 1),
        (100104, 'en', 'run', 'verb', 1),
        (100105, 'en', 'build', 'verb', 1),
        (100107, 'en', 'drive', 'verb', 1),
        (100108, 'en', 'count', 'verb', 1),
        (100109, 'en', 'understand', 'verb', 1),
        (100110, 'en', 'begin', 'verb', 1),
        (100111, 'en', 'choose', 'verb', 1),
        (100112, 'en', 'look for', 'verb', 1),
        (100113, 'en', 'sing', 'verb', 1),
        (100114, 'en', 'change', 'verb', 1),
        (100115, 'en', 'break', 'verb', 1),
        (100116, 'en', 'hide', 'verb', 1),
        (100117, 'en', 'burn', 'verb', 1),
        (100118, 'en', 'move', 'verb', 1),
        (100119, 'en', 'drink', 'verb', 1),
        (100120, 'en', 'chat', 'verb', 1),
        (100121, 'en', 'be afraid', 'verb', 1),
        (100122, 'en', 'trust', 'verb', 1),
        (100123, 'en', 'need', 'verb', 1),
        (100124, 'en', 'have', 'verb', 1),
        (100125, 'en', 'wait', 'verb', 1),
        (100126, 'en', 'arrive', 'verb', 1),
        (100127, 'en', 'stop', 'verb', 1),
        (100128, 'en', 'learn', 'verb', 1),
        (100129, 'en', 'like', 'verb', 1),
        (100130, 'en', 'call', 'verb', 1),
        (100132, 'en', 'love', 'verb', 1),
        (100133, 'en', 'buy', 'verb', 1),
        (100134, 'en', 'help', 'verb', 1),
        (100135, 'en', 'give', 'verb', 1),
        (100136, 'en', 'come back', 'verb', 1),
        #(100137, 'en', 'go', 'verb', 1), # ERROR doublon avec : (10055, 'en', 'go', 'verb', 1),
        (100138, 'en', 'go out', 'verb', 1),
        (100139, 'en', 'go in', 'verb', 1),
        (100140, 'en', 'turn on', 'verb', 1),
        (100141, 'en', 'turn off', 'verb', 1),
        (100142, 'en', 'suggest', 'verb', 1),
        (100143, 'en', 'decide', 'verb', 1),
        #(100144, 'en', 'put', 'verb', 1), # ERROR doublon avec : (10047, 'en', 'put', 'verb', 1),
        (100145, 'en', 'reduce', 'verb', 1),
        (100146, 'en', 'fill', 'verb', 1),
        (100147, 'en', 'go up', 'verb', 1),
        (100148, 'en', 'go down', 'verb', 1),
        (100150, 'en', 'sit down', 'verb', 1),
        (100151, 'en', 'remove', 'verb', 1),
        (180138, 'en', 'take out', 'verb', 1),
        (180139, 'en', 'enter', 'verb', 1),
        (190005, 'en', 'steal', 'verb', 1),
        (190041, 'en', 'feel', 'verb', 1),
        (190046, 'en', 'shoot', 'verb', 1),
        (190138, 'en', 'come out', 'verb', 1),
        (190139, 'en', 'come in', 'verb', 1),
        (190147, 'en', 'come up', 'verb', 1),
        (190148, 'en', 'come down', 'verb', 1),
        
        # VAGUE 2 complément
        (190126, 'en', 'happen', 'verb', 2),
        (100152, 'en', 'add', 'verb', 2),
        (100153, 'en', 'catch', 'verb', 2),
        (100154, 'en', 'increase', 'verb', 2),
        (100155, 'en', 'shine', 'verb', 2),
        (100156, 'en', 'hunt', 'verb', 2),
        (190156, 'en', 'drive out', 'verb', 2),
        (100159, 'en', 'discover', 'verb', 2),
        (100160, 'en', 'desire', 'verb', 2),
        (100161, 'en', 'guess', 'verb', 2),
        (100162, 'en', 'decrease', 'verb', 2),
        (100163, 'en', 'discuss', 'verb', 2),
        (100164, 'en', 'disappear', 'verb', 2),
        (100165, 'en', 'last', 'verb', 2),
        (100166, 'en', 'agree', 'verb', 2),
        (100167, 'en', 'moan', 'verb', 2),
        (100168, 'en', 'slip', 'verb', 2),
        (190168, 'en', 'glide', 'verb', 2),
        (100169, 'en', 'interest', 'verb', 2),
        (190169, 'en', 'concern', 'verb', 2),
        (100170, 'en', 'raise', 'verb', 2),
        (190170, 'en', 'lift', 'verb', 2),
        (100171, 'en', 'rent', 'verb', 2),
        (190171, 'en', 'hire', 'verb', 2),
        (180171, 'en', 'lease', 'verb', 2),
        (100172, 'en', 'feed', 'verb', 2),
        (100173, 'en', 'share', 'verb', 2),
        (100174, 'en', 'hang', 'verb', 2),
        (100175, 'en', 'fold', 'verb', 2),
        (100176, 'en', 'dive', 'verb', 2),
        (100177, 'en', 'push', 'verb', 2),
        (100178, 'en', 'lend', 'verb', 2),
        (100179, 'en', 'produce', 'verb', 2),
        (100182, 'en', 'dream', 'verb', 2),
        (100183, 'en', 'be worth', 'verb', 2),
        (100184, 'en', 'empty', 'verb', 2),
        (100185, 'en', 'become', 'verb', 2),
        (100187, 'en', 'bring', 'verb', 2),
        
        # VAGUE 3 compléments
        (100188, 'en', 'cut', 'verb', 2),
        (100189, 'en', 'draw', 'verb', 2),
        (100190, 'en', 'keep', 'verb', 2),
        (100191, 'en', 'lead', 'verb', 2),
        (100192, 'en', 'let', 'verb', 2),
        (100193, 'en', 'lie', 'verb', 2),
        (100194, 'en', 'mean', 'verb', 2),
        (100195, 'en', 'spend', 'verb', 2),
        (190063, 'en', 'wear', 'verb', 2),
        (100196, 'en', 'stand', 'verb', 2),
        (100197, 'en', 'sit', 'verb', 2),
        (100199, 'en', 'get', 'verb', 2),
        (100200, 'en', 'set', 'verb', 2),
        
        # VAGUE 4 compléments
        (100201, 'en', 'kill', 'verb', 4),
        (100202, 'en', 'hurt', 'verb', 4),
        (100203, 'en', 'fight', 'verb', 4),
        
        # VAGUE 5
        (100204, 'en', 'ask out', 'verb', 5),
        (100205, 'en', 'add up', 'verb', 5),
        #(90152, 'fr', 'additionner', 'verb', 2), # se monter à ?
        (100206, 'en', 'bear', 'verb', 5),
        
        (100207, 'en', 'beat', 'verb', 5),
        (207, 'fr', 'battre', 'verb', 5),
        
        (100208, 'en', 'bend', 'verb', 5),
        (100209, 'en', 'bet', 'verb', 5),
        (100210, 'en', 'bid', 'verb', 5),
        
        (100211, 'en', 'bind', 'verb', 5),
        (211, 'fr', 'attacher', 'verb', 5),
        (90211, 'fr', 'lier', 'verb', 5),
        (100212, 'en', 'bite', 'verb', 5),
        (212, 'fr', 'mordre', 'verb', 5),
        (100213, 'en', 'bleed', 'verb', 5),
        (213, 'fr', 'saigner', 'verb', 5),
        (100214, 'en', 'blow', 'verb', 5), # souffler
        (214, 'fr', 'souffler', 'verb', 5),
        
        (100215, 'en', 'breed', 'verb', 5),
        (100216, 'en', 'broadcast', 'verb', 5),
        (100217, 'en', 'blow up', 'verb', 5),
        (100218, 'en', 'break down', 'verb', 5),
        (100219, 'en', 'break in', 'verb', 5),
        (100220, 'en', 'break up', 'verb', 5),
        (100221, 'en', 'break out', 'verb', 5),
        (100222, 'en', 'bring up', 'verb', 5),
        (100223, 'en', 'cast', 'verb', 5),
        
        (100224, 'en', 'call back', 'verb', 5),
        
        (190225, 'en', 'call off', 'verb', 5),
        (225, 'fr', 'annuler', 'verb', 5),
        (100225, 'en', 'cancel', 'verb', 5),
        
        (100226, 'en', 'calm down', 'verb', 5),
        
        (100227, 'en', 'check', 'verb', 5),
        (227, 'fr', 'vérifier', 'verb', 5),
        
        (100228, 'en', 'check in', 'verb', 5),
        (100229, 'en', 'check out', 'verb', 5),
        (100230, 'en', 'cheer up', 'verb', 5),
        (100231, 'en', 'come across', 'verb', 5),
        (100232, 'en', 'come forward', 'verb', 5),
        (100233, 'en', 'count on', 'verb', 5),
        (100234, 'en', 'cross out', 'verb', 5),
        (100235, 'en', 'deal', 'verb', 5),
        (100236, 'en', 'dig', 'verb', 5),
        (100237, 'en', 'dwell', 'verb', 5),
        (100238, 'en', 'drop in', 'verb', 5),
        (100239, 'en', 'drop off', 'verb', 5),
        (100240, 'en', 'drop out', 'verb', 5),
        (100241, 'en', 'end up', 'verb', 5),
        (100242, 'en', 'flee', 'verb', 5),
        (100243, 'en', 'fling', 'verb', 5),
        (100244, 'en', 'forbid', 'verb', 5),
        (100245, 'en', 'foresee', 'verb', 5),
        (100246, 'en', 'forsake', 'verb', 5),
        (100247, 'en', 'freeze', 'verb', 5),
        (100248, 'en', 'fall apart', 'verb', 5),
        (100249, 'en', 'fall down', 'verb', 5),
        (100250, 'en', 'figure out', 'verb', 5),
        (100251, 'en', 'find out', 'verb', 5),
        (100252, 'en', 'going in', 'verb', 5),
        (100253, 'en', 'grow', 'verb', 5),
        (100254, 'en', 'get along', 'verb', 5),
        (100255, 'en', 'get back', 'verb', 5),
        (100256, 'en', 'get up', 'verb', 5),
        (100257, 'en', 'give in', 'verb', 5),
        (100258, 'en', 'give up', 'verb', 5),
        (100259, 'en', 'go ahead', 'verb', 5),
        (100260, 'en', 'go back', 'verb', 5),
        (100261, 'en', 'go by', 'verb', 5),
        (100262, 'en', 'go out with', 'verb', 5),
        (100263, 'en', 'grow back', 'verb', 5),
        (100264, 'en', 'grow up', 'verb', 5),
        (100265, 'en', 'hit', 'verb', 5),
        (100266, 'en', 'hand down', 'verb', 5),
        (100267, 'en', 'hand over', 'verb', 5),
        (100268, 'en', 'hang up', 'verb', 5),
        (100269, 'en', 'hold back', 'verb', 5),
        (100270, 'en', 'hold on', 'verb', 5),
        (100271, 'en', 'hold on to', 'verb', 5),
        (100272, 'en', 'keep on', 'verb', 5),
        (100273, 'en', 'lay', 'verb', 5),
        (100274, 'en', 'lean', 'verb', 5),
        (100275, 'en', 'leap', 'verb', 5),
        (100276, 'en', 'light', 'verb', 5),
        (100277, 'en', 'let down', 'verb', 5),
        (100278, 'en', 'let in', 'verb', 5),
        (100279, 'en', 'log', 'verb', 5),
        (100280, 'en', 'log in', 'verb', 5),
        (100281, 'en', 'log out', 'verb', 5),
        (100282, 'en', 'look after', 'verb', 5),
        (100283, 'en', 'look forward', 'verb', 5),
        (100284, 'en', 'look into', 'verb', 5),
        (100285, 'en', 'look out', 'verb', 5),
        (100286, 'en', 'make up', 'verb', 5),
        (100287, 'en', 'offset', 'verb', 5),
        (100288, 'en', 'partake', 'verb', 5),
        (100289, 'en', 'plead', 'verb', 5),
        (100290, 'en', 'prove', 'verb', 5),
        (100291, 'en', 'pass away', 'verb', 5),
        (100292, 'en', 'pass out', 'verb', 5),
        (100293, 'en', 'pay back', 'verb', 5),
        (100294, 'en', 'pick out', 'verb', 5),
        (100295, 'en', 'quit', 'verb', 5),
        (100296, 'en', 'relay', 'verb', 5),
        (100297, 'en', 'rid', 'verb', 5),
        (100298, 'en', 'ride', 'verb', 5),
        (100299, 'en', 'ring', 'verb', 5),
        (100300, 'en', 'run away', 'verb', 5),
        (100301, 'en', 'run out', 'verb', 5),
        (100302, 'en', 'seek', 'verb', 5),
        (100303, 'en', 'shake', 'verb', 5),
        (100304, 'en', 'shed', 'verb', 5),
        (100305, 'en', 'shut', 'verb', 5),
        (100306, 'en', 'sink', 'verb', 5),
        (100307, 'en', 'speed', 'verb', 5),
        (100308, 'en', 'spell', 'verb', 5),
        (100309, 'en', 'spill', 'verb', 5),
        (100310, 'en', 'spin', 'verb', 5),
        (100311, 'en', 'spit', 'verb', 5),
        (100312, 'en', 'split', 'verb', 5),
        (100313, 'en', 'spoil', 'verb', 5),
        (100314, 'en', 'spread', 'verb', 5),
        (100315, 'en', 'stick', 'verb', 5),
        (100316, 'en', 'string', 'verb', 5),
        (100317, 'en', 'stink', 'verb', 5),
        (100318, 'en', 'strew', 'verb', 5),
        (100319, 'en', 'strike', 'verb', 5),
        (100320, 'en', 'swear', 'verb', 5),
        (100321, 'en', 'sweat', 'verb', 5),
        (100322, 'en', 'sweep', 'verb', 5), # stand for
        (100323, 'en', 'swell', 'verb', 5),
        (100324, 'en', 'swing', 'verb', 5),
        (100325, 'en', 'send back', 'verb', 5),
        (100326, 'en', 'set up', 'verb', 5),
        (100327, 'en', 'shop around', 'verb', 5),
        (100328, 'en', 'show off', 'verb', 5),
        (100329, 'en', 'sleep over', 'verb', 5),
        (100330, 'en', 'stick to', 'verb', 5),
        (100331, 'en', 'tear', 'verb', 5),
        (100332, 'en', 'tread', 'verb', 5),
        (100334, 'en', 'take off', 'verb', 5),
        (100335, 'en', 'land', 'verb', 5),
        (100336, 'en', 'throw away', 'verb', 5),
        (100337, 'en', 'turn down', 'verb', 5),
        #(100338, 'en', 'turn off', 'verb', 5),
        #(100339, 'en', 'turn on', 'verb', 5),
        (100340, 'en', 'turn up', 'verb', 5),
        (100341, 'en', 'try out', 'verb', 5),
        (100342, 'en', 'undergo', 'verb', 5),
        (100343, 'en', 'wake', 'verb', 5),
        (100344, 'en', 'weep', 'verb', 5),
        (100345, 'en', 'wet', 'verb', 5),
        (100346, 'en', 'wind', 'verb', 5),
        (100347, 'en', 'withdraw', 'verb', 5),
        (100348, 'en', 'wring', 'verb', 5),
        (100349, 'en', 'warm up', 'verb', 5),
        (100350, 'en', 'wear off', 'verb', 5),
        (100351, 'en', 'work out', 'verb', 5),
        (100352, 'en', 'mislay', 'verb', 5),
        (100353, 'en', 'mislead', 'verb', 5),
        (100354, 'en', 'mistake', 'verb', 5),
        (100355, 'en', 'misunderstand', 'verb', 5),
        (100356, 'en', 'outrun', 'verb', 5),
        (100357, 'en', 'overcome', 'verb', 5),
        (100358, 'en', 'overdo', 'verb', 5),
        (100359, 'en', 'overhear', 'verb', 5),
        (100360, 'en', 'overlay', 'verb', 5),
        (100361, 'en', 'override', 'verb', 5),
        (100362, 'en', 'overrun', 'verb', 5),
        (100363, 'en', 'oversee', 'verb', 5),
        (100364, 'en', 'oversleep', 'verb', 5),
        (100365, 'en', 'overtake', 'verb', 5),
        (100366, 'en', 'overthrow', 'verb', 5),
        (100367, 'en', 'rebuild', 'verb', 5),
        (100368, 'en', 'redo', 'verb', 5),
        (100369, 'en', 'regrow', 'verb', 5),
        (100370, 'en', 'relight', 'verb', 5),
        (100371, 'en', 'remake', 'verb', 5),
        (100372, 'en', 'reset', 'verb', 5),
        (100373, 'en', 'retake', 'verb', 5),
        (100374, 'en', 'rewind', 'verb', 5),
        (100375, 'en', 'undo', 'verb', 5),
        (100376, 'en', 'unwind', 'verb', 5),
        (100377, 'en', 'underlie', 'verb', 5),
        (100378, 'en', 'load', 'verb', 5),
        # VAGUE 6 : verb irr not in list
        (100379, 'en', 'abide', 'verb', 6),
        (100380, 'en', 'arise', 'verb', 6),
        (100381, 'en', 'awake', 'verb', 6),
        (100382, 'en', 'beget', 'verb', 6),
        (100383, 'en', 'bereave', 'verb', 6),
        (100384, 'en', 'burst', 'verb', 6),
        (100385, 'en', 'chide', 'verb', 6),
        (100386, 'en', 'cling', 'verb', 6),
        (100387, 'en', 'clothe', 'verb', 6),
        (100388, 'en', 'creep', 'verb', 6),
        (100389, 'en', 'forecast', 'verb', 6),
        (100390, 'en', 'grind', 'verb', 6),
        (100391, 'en', 'kneel', 'verb', 6),
        (100392, 'en', 'mow', 'verb', 6),
        (100393, 'en', 'preset', 'verb', 6),
        (100394, 'en', 'rend', 'verb', 6),
        (100395, 'en', 'saw', 'verb', 6),
        (100396, 'en', 'shoe', 'verb', 6),
        (100397, 'en', 'slay', 'verb', 6),
        (100398, 'en', 'slide', 'verb', 6),
        (100399, 'en', 'slink', 'verb', 6),
        (100400, 'en', 'slit', 'verb', 6),
        (100401, 'en', 'sow', 'verb', 6),
        (100402, 'en', 'sting', 'verb', 6),
        (100403, 'en', 'strive', 'verb', 6),
        (100404, 'en', 'thrive', 'verb', 6),
        (100405, 'en', 'thrust', 'verb', 6),
        (100406, 'en', 'typeset', 'verb', 6),
        # VAGUE 7 : vus et entendus
        (100407, 'en', 'return', 'verb', 7),
        (100408, 'en', 'fire', 'verb', 7),
        (100409, 'en', 'worry', 'verb', 7),
        (100410, 'en', 'defeat', 'verb', 7),
        (100411, 'en', 'avoid', 'verb', 7),
        (100412, 'en', 'obey', 'verb', 7),
        (100413, 'en', 'save', 'verb', 7),
        (100414, 'en', 'surprise', 'verb', 7),
        
        # to turn traitor : trahir (devenir traître)
        # to stand by : attendre
        # to fallback : se replier
        # take (back to?) your seat : regagner 
        # to take out sone : neutraliser
        # clear off the area : évacuer
        
        #(100, 'en', '', 'verb', 5),
        
        #
        # Verbes italiens
        #
        (200001, 'it', 'aprire', 'verb', 1),
        (200002, 'it', 'viaggiare', 'verb', 1),
        (200003, 'it', 'volere', 'verb', 1),
        (200005, 'it', 'volare', 'verb', 1),
        (200006, 'it', 'vedere', 'verb', 1),
        (200007, 'it', 'vivere', 'verb', 1),
        (200008, 'it', 'visitare', 'verb', 1),
        (200009, 'it', 'venire', 'verb', 1),
        (200010, 'it', 'vendere', 'verb', 1),
        (200011, 'it', 'utilizzare', 'verb', 1),
        (200012, 'it', 'trovare', 'verb', 1),
        (200013, 'it', 'lavorare', 'verb', 1),
        (200014, 'it', 'tradurre', 'verb', 1),
        (200015, 'it', 'girare', 'verb', 1),
        (200016, 'it', 'toccare', 'verb', 1),
        (200017, 'it', 'cadere', 'verb', 1),
        (200026, 'it', 'raccontare', 'verb', 1),
        (200027, 'it', 'ricevere', 'verb', 1),
        (200028, 'it', 'guardare', 'verb', 1),
        (200029, 'it', 'ringraziare', 'verb', 1),
        (200030, 'it', 'incontrare', 'verb', 1),
        (200031, 'it', 'rispondere', 'verb', 1),
        (200032, 'it', 'rimanere', 'verb', 1),
        (200033, 'it', 'riuscire', 'verb', 1),
        (200034, 'it', 'svegliarsi', 'verb', 1),
        (200035, 'it', 'ridere', 'verb', 1),
        (200036, 'it', 'occuparsi', 'verb', 1),
        (200037, 'it', 'saltare', 'verb', 1),
        (200038, 'it', 'sapere', 'verb', 1),
        (200039, 'it', 'riposarsi', 'verb', 1),
        (200040, 'it', 'ricordarsi', 'verb', 1),
        (200041, 'it', 'sentire', 'verb', 1),
        (200042, 'it', 'soffrire', 'verb', 1),
        (200043, 'it', 'augurare', 'verb', 1),
        (200044, 'it', 'seguire', 'verb', 1),
        (200045, 'it', 'tenere', 'verb', 1),
        (200046, 'it', 'tirare', 'verb', 1),
        (200047, 'it', 'mettere', 'verb', 1),
        (200048, 'it', 'mostrare', 'verb', 1),
        (200049, 'it', 'morire', 'verb', 1),
        (200050, 'it', 'nuotare', 'verb', 1),
        (200051, 'it', 'nascere', 'verb', 1),
        (200052, 'it', 'dimenticare', 'verb', 1),
        (200053, 'it', 'perdonare', 'verb', 1),
        (200054, 'it', 'parlare', 'verb', 1),
        (200055, 'it', 'partire', 'verb', 1),
        (200056, 'it', 'passare', 'verb', 1),
        (200057, 'it', 'pagare', 'verb', 1),
        (200058, 'it', 'pensare', 'verb', 1),
        (200059, 'it', 'perdere', 'verb', 1),
        (200060, 'it', 'permettere', 'verb', 1),
        (200061, 'it', 'piacere', 'verb', 1),
        (200062, 'it', 'piangere', 'verb', 1),
        (200063, 'it', 'portare', 'verb', 1),
        (200064, 'it', 'potere', 'verb', 1),
        (200065, 'it', 'prendere', 'verb', 1),
        (200066, 'it', 'presentarsi', 'verb', 1),
        (200067, 'it', 'promettere', 'verb', 1),
        (200068, 'it', 'lasciare', 'verb', 1),
        (200069, 'it', 'camminare', 'verb', 1),
        (200070, 'it', 'mancare', 'verb', 1),
        (200071, 'it', 'mangiare', 'verb', 1),
        (200072, 'it', 'leggere', 'verb', 1),
        (200073, 'it', 'alzarsi', 'verb', 1),
        (200074, 'it', 'lavare', 'verb', 1),
        (200075, 'it', 'giocare', 'verb', 1),
        (200076, 'it', 'buttare', 'verb', 1),
        (200077, 'it', 'invitare', 'verb', 1),
        (200078, 'it', 'abitare', 'verb', 1),
        (200079, 'it', 'vestirsi', 'verb', 1),
        (200080, 'it', 'assaggiare', 'verb', 1),
        (200081, 'it', 'guadagnare', 'verb', 1),
        (200082, 'it', 'finire', 'verb', 1),
        (200083, 'it', 'chiudere', 'verb', 1),
        (200084, 'it', 'fare', 'verb', 1),
        (200085, 'it', 'studiare', 'verb', 1),
        (200086, 'it', 'essere', 'verb', 1),
        (200087, 'it', 'provare', 'verb', 1),
        (200088, 'it', 'sperare', 'verb', 1),
        (200089, 'it', 'spedire', 'verb', 1),
        (200091, 'it', 'insegnare', 'verb', 1),
        (200092, 'it', 'scrivere', 'verb', 1),
        (200093, 'it', 'ascoltare', 'verb', 1),
        (200094, 'it', 'dormire', 'verb', 1),
        (200095, 'it', 'dire', 'verb', 1),
        (200096, 'it', 'dovere', 'verb', 1),
        (200097, 'it', 'chiedere', 'verb', 1),
        (200098, 'it', 'ballare', 'verb', 1),
        (200099, 'it', 'cuocere', 'verb', 1),
        (200100, 'it', 'credere', 'verb', 1),
        (200101, 'it', 'gridare', 'verb', 1),
        (200102, 'it', 'creare', 'verb', 1),
        (200103, 'it', 'costare', 'verb', 1),
        (200104, 'it', 'correre', 'verb', 1),
        (200105, 'it', 'costruire', 'verb', 1),
        (200106, 'it', 'conoscere', 'verb', 1),
        (200107, 'it', 'guidare', 'verb', 1),
        (200108, 'it', 'contare', 'verb', 1),
        (200109, 'it', 'capire', 'verb', 1),
        (200110, 'it', 'cominciare', 'verb', 1),
        (200111, 'it', 'scegliere', 'verb', 1),
        (200112, 'it', 'cercare', 'verb', 1),
        (200113, 'it', 'cantare', 'verb', 1),
        (200114, 'it', 'cambiare', 'verb', 1),
        (200115, 'it', 'rompere', 'verb', 1),
        (200116, 'it', 'nascondere', 'verb', 1),
        (200117, 'it', 'bruciare', 'verb', 1),
        (200118, 'it', 'spostare', 'verb', 1),
        (200119, 'it', 'bere', 'verb', 1),
        (200120, 'it', 'chiacchierare', 'verb', 1),
        (200121, 'it', 'avere paura', 'verb', 1),
        (200122, 'it', 'avere fiducia', 'verb', 1),
        (200123, 'it', 'avere bisogno', 'verb', 1),
        (200124, 'it', 'avere', 'verb', 1),
        (200125, 'it', 'aspettare', 'verb', 1),
        (200126, 'it', 'arrivare', 'verb', 1),
        (200127, 'it', 'fermare', 'verb', 1),
        (200128, 'it', 'imparare', 'verb', 1),
        (200129, 'it', 'apprezzare', 'verb', 1),
        (200130, 'it', 'chiamare', 'verb', 1),
        (200132, 'it', 'amare', 'verb', 1),
        (200133, 'it', 'comprare', 'verb', 1),
        (200134, 'it', 'aiutare', 'verb', 1),
        (200135, 'it', 'dare', 'verb', 1),
        (200136, 'it', 'ritornare', 'verb', 1),
        (200137, 'it', 'andare', 'verb', 1),
        (200138, 'it', 'uscire', 'verb', 1),
        (200139, 'it', 'entrare', 'verb', 1),
        (200140, 'it', 'accendere', 'verb', 1),
        (200141, 'it', 'spegnere', 'verb', 1),
        (200142, 'it', 'proporre', 'verb', 1),
        (200143, 'it', 'decidere', 'verb', 1),
        (200144, 'it', 'posare', 'verb', 1),
        (200145, 'it', 'ridurre', 'verb', 1),
        (200146, 'it', 'riempire', 'verb', 1),
        (200147, 'it', 'salire', 'verb', 1),
        (200148, 'it', 'scendere', 'verb', 1),
        (200150, 'it', 'sedersi', 'verb', 1),
        (200151, 'it', 'togliere', 'verb', 1),
        (280075, 'it', 'suonare', 'verb', 1),
        (290005, 'it', 'rubare', 'verb', 1),
        (290075, 'it', 'recitare', 'verb', 1),
        (290086, 'it', 'stare', 'verb', 1),

        (300001, 'de', 'öffnen', 'verb', 1),

        (400001, 'eo', 'malfermi', 'verb', 1),
        (400002, 'eo', 'vojaĝi', 'verb', 1),
        (400003, 'eo', 'voli', 'verb', 1),
        (400005, 'eo', 'flugi', 'verb', 1),
        (400006, 'eo', 'vidi', 'verb', 1),
        (400007, 'eo', 'vivi', 'verb', 1),
        (400008, 'eo', 'viziti', 'verb', 1),
        (400009, 'eo', 'veni', 'verb', 1),
        (400010, 'eo', 'vendi', 'verb', 1),
        (400011, 'eo', 'uzi', 'verb', 1),
        (400012, 'eo', 'trovi', 'verb', 1),
        (400013, 'eo', 'labori', 'verb', 1),
        (400014, 'eo', 'traduki', 'verb', 1),
        (400015, 'eo', 'turni', 'verb', 1),
        (400016, 'eo', 'tuŝi', 'verb', 1),
        (400017, 'eo', 'fali', 'verb', 1),
        (400026, 'eo', 'rakonti', 'verb', 1),
        (400027, 'eo', 'ricevi', 'verb', 1),
        (400028, 'eo', 'rigardi', 'verb', 1),
        (400029, 'eo', 'danki', 'verb', 1),
        (400030, 'eo', 'renkonti', 'verb', 1),
        (400031, 'eo', 'respondi', 'verb', 1),
        (400032, 'eo', 'resti', 'verb', 1),
        (400033, 'eo', 'sukcesi', 'verb', 1),
        (400034, 'eo', 'veki', 'verb', 1),
        (400035, 'eo', 'ridi', 'verb', 1),
        (400036, 'eo', 'zorgi', 'verb', 1),
        (400037, 'eo', 'salti', 'verb', 1),
        (400038, 'eo', 'scii', 'verb', 1),
        (400039, 'eo', 'ripozi', 'verb', 1),
        (400040, 'eo', 'memori', 'verb', 1),
        (400041, 'eo', 'odori', 'verb', 1),
        (400042, 'eo', 'suferi', 'verb', 1),
        (400043, 'eo', 'deziri', 'verb', 1),
        (400044, 'eo', 'sekvi', 'verb', 1),
        (400045, 'eo', 'teni', 'verb', 1),
        (400046, 'eo', 'tiri', 'verb', 1),
        (400047, 'eo', 'meti', 'verb', 1),
        (400048, 'eo', 'montri', 'verb', 1),
        (400049, 'eo', 'morti', 'verb', 1),
        (400050, 'eo', 'naĝi', 'verb', 1),
        (400051, 'eo', 'naskiĝi', 'verb', 1),
        (400052, 'eo', 'forgesi', 'verb', 1),
        (400053, 'eo', 'pardoni', 'verb', 1),
        (400054, 'eo', 'paroli', 'verb', 1),
        (400055, 'eo', 'ekiri', 'verb', 1),
        (400056, 'eo', 'pasi', 'verb', 1),
        (400057, 'eo', 'pagi', 'verb', 1),
        (400058, 'eo', 'pensi', 'verb', 1),
        (400059, 'eo', 'perdi', 'verb', 1),
        (400060, 'eo', 'permesi', 'verb', 1),
        (400061, 'eo', 'plaĉi', 'verb', 1),
        (400062, 'eo', 'plori', 'verb', 1),
        (400063, 'eo', 'porti', 'verb', 1),
        (400064, 'eo', 'povi', 'verb', 1),
        (400065, 'eo', 'preni', 'verb', 1),
        (400066, 'eo', 'prezenti', 'verb', 1),
        (400067, 'eo', 'promesi', 'verb', 1),
        (400068, 'eo', 'forlasi', 'verb', 1),
        (400069, 'eo', 'marŝi', 'verb', 1),
        (400070, 'eo', 'manki', 'verb', 1),
        (400071, 'eo', 'manĝi', 'verb', 1),
        (400072, 'eo', 'legi', 'verb', 1),
        (400073, 'eo', 'levi', 'verb', 1),
        (400074, 'eo', 'lavi', 'verb', 1),
        (400075, 'eo', 'ludi', 'verb', 1),
        (400076, 'eo', 'ĵeti', 'verb', 1),
        (400077, 'eo', 'inviti', 'verb', 1),
        (400078, 'eo', 'loĝi', 'verb', 1),
        (400079, 'eo', 'vesti', 'verb', 1),
        (400080, 'eo', 'gustumi', 'verb', 1),
        (400081, 'eo', 'gajni', 'verb', 1),
        (400082, 'eo', 'fini', 'verb', 1),
        (400083, 'eo', 'fermi', 'verb', 1),
        (400084, 'eo', 'fari', 'verb', 1),
        (400085, 'eo', 'studi', 'verb', 1),
        (400086, 'eo', 'esti', 'verb', 1),
        (400087, 'eo', 'provi', 'verb', 1),
        (400088, 'eo', 'esperi', 'verb', 1),
        (400089, 'eo', 'sendi', 'verb', 1),
        (400090, 'eo', 'aŭdi', 'verb', 1),
        (400091, 'eo', 'instrui', 'verb', 1),
        (400092, 'eo', 'skribi', 'verb', 1),
        (400093, 'eo', 'aŭskulti', 'verb', 1),
        (400094, 'eo', 'dormi', 'verb', 1),
        (400095, 'eo', 'diri', 'verb', 1),
        (400096, 'eo', 'devi', 'verb', 1),
        (400097, 'eo', 'demandi', 'verb', 1),
        (400098, 'eo', 'danci', 'verb', 1),
        (400099, 'eo', 'kuiri', 'verb', 1),
        (400100, 'eo', 'kredi', 'verb', 1),
        (400101, 'eo', 'krii', 'verb', 1),
        (400102, 'eo', 'krei', 'verb', 1),
        (400103, 'eo', 'kosti', 'verb', 1),
        (400104, 'eo', 'kuri', 'verb', 1),
        (400105, 'eo', 'konstrui', 'verb', 1),
        (400107, 'eo', 'stiri', 'verb', 1),
        (400108, 'eo', 'kalkuli', 'verb', 1),
        (400109, 'eo', 'kompreni', 'verb', 1),
        (400110, 'eo', 'komenci', 'verb', 1),
        (400111, 'eo', 'elekti', 'verb', 1),
        (400112, 'eo', 'serĉi', 'verb', 1),
        (400113, 'eo', 'kanti', 'verb', 1),
        (400114, 'eo', 'ŝanĝi', 'verb', 1),
        (400115, 'eo', 'rompi', 'verb', 1),
        (400116, 'eo', 'kaŝi', 'verb', 1),
        (400117, 'eo', 'bruli', 'verb', 1),
        (400118, 'eo', 'moviĝi', 'verb', 1),
        (400119, 'eo', 'trinki', 'verb', 1),
        (400120, 'eo', 'babili', 'verb', 1),
        (400121, 'eo', 'timi', 'verb', 1),
        (400122, 'eo', 'fidi', 'verb', 1),
        (400123, 'eo', 'bezoni', 'verb', 1),
        (400124, 'eo', 'havi', 'verb', 1),
        (400125, 'eo', 'atendi', 'verb', 1),
        (400126, 'eo', 'alveni', 'verb', 1),
        (400127, 'eo', 'ĉesigi', 'verb', 1),
        (400128, 'eo', 'lerni', 'verb', 1),
        (400129, 'eo', 'aprezi', 'verb', 1),
        (400130, 'eo', 'voki', 'verb', 1),
        (400132, 'eo', 'ami', 'verb', 1),
        (400133, 'eo', 'aĉeti', 'verb', 1),
        (400134, 'eo', 'helpi', 'verb', 1),
        (400135, 'eo', 'doni', 'verb', 1),
        (400136, 'eo', 'reveni', 'verb', 1),
        (400137, 'eo', 'iri', 'verb', 1),
        (400138, 'eo', 'eliri', 'verb', 1),
        (400139, 'eo', 'eniri', 'verb', 1),
        (400140, 'eo', 'ŝalti', 'verb', 1),
        (400141, 'eo', 'elŝalti', 'verb', 1),
        (400142, 'eo', 'proponi', 'verb', 1),
        (400143, 'eo', 'decidi', 'verb', 1),
        # (400144, 'eo', 'meti', 'verb', 1), # ERROR doublon avec (40047, 'eo', 'meti', 'verb', 1),
        (400145, 'eo', 'redukti', 'verb', 1),
        (400146, 'eo', 'plenigi', 'verb', 1),
        (400147, 'eo', 'supreniri', 'verb', 1),
        (400148, 'eo', 'malsupreniri', 'verb', 1),
        (400150, 'eo', 'sidiĝi', 'verb', 1),
        (400151, 'eo', 'elpreni', 'verb', 1),
        (490005, 'eo', 'ŝteli', 'verb', 1),
        (490041, 'eo', 'senti', 'verb', 1),
        (490046, 'eo', 'pafi', 'verb', 1),
        # (490046, 'xy', 'xxxx', 9)

        # INSERT NOUNS
        (21000, 'fr', 'livre', 'noun', 1), (11000, 'en', 'book', 'noun', 1),
        (21001, 'fr', 'lit', 'noun', 1), (11001, 'en', 'bed', 'noun', 1),
        (21002, 'fr', 'père', 'noun', 1), (11002, 'en', 'father', 'noun', 1),
        (21003, 'fr', 'mère', 'noun', 1), (11003, 'en', 'mother', 'noun', 1),
        (21004, 'fr', 'frère', 'noun', 1), (11004, 'en', 'brother', 'noun', 1),
        (21005, 'fr', 'sœur', 'noun', 1), (11005, 'en', 'sister', 'noun', 1),
        (21006, 'fr', 'fils', 'noun', 1), (11006, 'en', 'son', 'noun', 1),
        (21007, 'fr', 'fille', 'noun', 1), (11007, 'en', 'daughter', 'noun', 1),
        (18007, 'en', 'girl', 'noun', 1),
        (21008, 'fr', 'garçon', 'noun', 1), (11008, 'en', 'boy', 'noun', 1),
        
        (121009, 'en', 'parent', 'noun', 1),
        (121010, 'en', 'person', 'noun', 1),
        (121011, 'en', 'friend', 'noun', 1),

        (121012, 'en', 'mouth', 'noun', 1),

        (121013, 'en', 'season', 'noun', 1),
        (121014, 'en', 'summer', 'noun', 1),
        (121015, 'en', 'spring', 'noun', 1),
        (121016, 'en', 'winter', 'noun', 1),
        (121017, 'en', 'autumn', 'noun', 1),
        # (121018, 'en', 'fall', 'noun', 1), doublon avc le verbe !
        (121019, 'en', 'day', 'noun', 1),
        (121020, 'en', 'week', 'noun', 1),
        (121021, 'en', 'time', 'noun', 1),

        (121022, 'en', 'morning', 'noun', 1),
        (121023, 'en', 'afternoon', 'noun', 1),
        (121024, 'en', 'evening', 'noun', 1),

        (121025, 'en', 'old', 'adjective', 1),
        (121026, 'en', 'new', 'adjective', 1),
        (121027, 'en', 'long', 'adjective', 1),
        (121028, 'en', 'short', 'adjective', 1),
        (121029, 'en', 'fast', 'adjective', 1),
        (121030, 'en', 'slow', 'adjective', 1),
        (121031, 'en', 'big', 'adjective', 1),
        (121032, 'en', 'small', 'adjective', 1),
        (121033, 'en', 'little', 'adjective', 1),
        (121034, 'en', 'great', 'adjective', 1),
        (121035, 'en', 'fat', 'adjective', 1),
        (121036, 'en', 'slim', 'adjective', 1),
        (121037, 'en', 'thick', 'adjective', 1),
        (121038, 'en', 'good', 'adjective', 1),
        (121039, 'en', 'well', 'adjective', 1),
        (121040, 'en', 'bad', 'adjective', 1),
        (121041, 'en', 'hard', 'adjective', 1),
        (121042, 'en', 'easy', 'adjective', 1),
        (121043, 'en', 'difficult', 'adjective', 1),
        (121044, 'en', 'simple', 'adjective', 1),
        (121045, 'en', 'low', 'adjective', 1),
        (121046, 'en', 'high', 'adjective', 1),
        (121047, 'en', 'large', 'adjective', 1),

        (120001, 'en', 'I', 'pronoun', 1),
        (120002, 'en', 'you', 'pronoun', 1),
        (120003, 'en', 'he', 'pronoun', 1),
        (120004, 'en', 'she', 'pronoun', 1),
        (120005, 'en', 'it', 'pronoun', 1),
        (120006, 'en', 'we', 'pronoun', 1),
        (120007, 'en', 'they', 'pronoun', 1),
        (120008, 'en', 'my', 'pronoun', 1),
        (120009, 'en', 'your', 'pronoun', 1),
        (120010, 'en', 'his', 'pronoun', 1),
        (120011, 'en', 'her', 'pronoun', 1),
        (120012, 'en', 'its', 'pronoun', 1),
        (120013, 'en', 'our', 'pronoun', 1),
        (120014, 'en', 'their', 'pronoun', 1),
        (120015, 'en', 'him', 'pronoun', 1),

        (120016, 'en', 'in', 'prep', 1),
        (120017, 'en', 'for', 'prep', 1),
        (120018, 'en', 'but', 'prep', 1),
        (120019, 'en', 'from', 'prep', 1),
        (120020, 'en', 'or', 'prep', 1),
        (120021, 'en', 'and', 'prep', 1),
        (120022, 'en', 'of', 'prep', 1),
        (120023, 'en', 'to', 'prep', 1),
        (120024, 'en', 'at', 'prep', 1),
        (120025, 'en', 'by', 'prep', 1),
        (120026, 'en', 'with', 'prep', 1),

        (120027, 'en', 'the', 'article,', 1),
        (120028, 'en', 'a', 'article,', 1),

        (120029, 'en', 'not', 'adverb', 1),

        (120830, 'en', 'that', '?', 1),
        (120831, 'en', 'those', '?', 1),
    ]
    return content
    

def get_irregular_verbs():
    content = [
        (68, 'abide', 'abode', 'abode'),
        (69, 'arise', 'arose', 'arisen'),
        (70, 'awake', 'awoke', 'awoken'),
        (1, 'be', 'was / were', 'been'),
        (71, 'bear', 'bore', 'borne/born'),
        (72, 'beat', 'beat', 'beaten'),
        (54, 'become', 'became', 'become'),
        (73, 'beget', 'begat/begot', 'begotten'),
        (2, 'begin', 'began', 'begun'),
        (74, 'bend', 'bent', 'bent'),
        (75, 'bereave', 'bereft/bereaved', 'bereft/bereaved'),
        (76, 'bet', 'bet', 'bet'),
        (77, 'bid', 'bid/bade', 'bid/bidden'),
        (178, 'bind', 'bound', 'bound'),
        (177, 'bite', 'bit', 'bitten'),
        (78, 'bleed', 'bled', 'bled'),
        (79, 'blow', 'blew', 'blown'),
        (3, 'break', 'broke', 'broken'),
        (80, 'breed', 'bred', 'bred'),
        (4, 'bring', 'brought', 'brought'),
        (81, 'broadcast', 'broadcast', 'broadcast'),
        (6, 'build', 'built', 'built'),
        (55, 'burn', 'burned/burnt', 'burned/burnt'),
        (82, 'burst', 'burst', 'burst'),
        (5, 'buy', 'bought', 'bought'),
        (59, 'can', 'could', 'could'),
        (83, 'cast', 'cast', 'cast'),
        (84, 'catch', 'caught', 'caught'),
        (85, 'chide', 'chid', 'chiden'),
        (7, 'choose', 'chose', 'chosen'),
        (86, 'cling', 'clung', 'clung'),
        (87, 'clothe', 'clad/clothed', 'clad/clothed'),
        (8, 'come', 'came', 'come'),
        (9, 'cost', 'cost', 'cost'),
        (88, 'creep', 'crept', 'crept'),
        (10, 'cut', 'cut', 'cut'),
        (89, 'deal', 'dealt', 'dealt'),
        (90, 'dig', 'dug', 'dug'),
        (91, 'dive', 'dived', 'dived/dove'),
        (11, 'do', 'did', 'done'),
        (12, 'draw', 'drew', 'drawn'),
        (92, 'dream', 'dreamt/dreamed', 'dreamt/dreamed'),
        (66, 'drink', 'drank', 'drunk'),
        (13, 'drive', 'drove', 'driven'),
        (93, 'dwell', 'dwelt', 'dwelt/dwelled'),
        (14, 'eat', 'ate', 'eaten'),
        (60, 'fall', 'fell', 'fallen'),
        (94, 'feed', 'fed', 'fed'),
        (15, 'feel', 'felt', 'felt'),
        (95, 'fight', 'fought', 'fought'),
        (16, 'find', 'found', 'found'),
        (96, 'flee', 'fled', 'fled'),
        (97, 'fling', 'flung', 'flung'),
        (67, 'fly', 'flew', 'flown'),
        (98, 'forbid', 'forbade', 'forbidden'),
        (99, 'forecast', 'forecast', 'forecast'),
        (100, 'foresee', 'foresaw', 'foreseen'),
        (58, 'forget', 'forgot', 'forgotten'),
        (101, 'forgive', 'forgave', 'forgiven'),
        (102, 'forsake', 'forsook', 'forsaken'),
        (103, 'freeze', 'froze', 'frozen'),
        (17, 'get', 'got', 'got'), # gotten au pp aussi?
        (18, 'give', 'gave', 'given'),
        (19, 'go', 'went', 'gone'),
        (104, 'grind', 'ground', 'ground'),
        (105, 'grow', 'grew', 'grown'),
        (106, 'hang', 'hung', 'hung'),
        (20, 'have', 'had', 'had'),
        (21, 'hear', 'heard', 'heard'),
        (107, 'hide', 'hid', 'hidden'),
        (108, 'hit', 'hit', 'hit'),
        (22, 'hold', 'held', 'held'),
        (109, 'hurt', 'hurt', 'hurt'),
        (23, 'keep', 'kept', 'kept'),
        (110, 'kneel', 'knelt/knelled', 'knelt/kneeled'),
        (24, 'know', 'knew', 'known'),
        (111, 'lay', 'laid', 'laid'),
        (26, 'lead', 'led', 'led'),
        (112, 'lean', 'leant/leaned', 'leant/leaned'),
        (113, 'leap', 'leapt/leaped', 'leapt/leaped'),
        (114, 'learn', 'learnt/learned', 'learnt/learned'),
        (25, 'leave', 'left', 'left'),
        (115, 'lend', 'lent', 'lent'),
        (27, 'let', 'let', 'let'),
        (28, 'lie', 'lay', 'lain'),
        (116, 'light', 'lit/lighted', 'lit/lighted'),
        (29, 'lose', 'lost', 'lost'),
        (30, 'make', 'made', 'made'),
        (31, 'mean', 'meant', 'meant'),
        (32, 'meet', 'met', 'met'),
        (117, 'mow', 'mowed', 'mowed/mown'),
        (61, 'must', '-', '-'),
        (118, 'offset', 'offset', 'offset'),
        (119, 'overcome', 'overcame', 'overcome'),
        (120, 'partake', 'partook', 'partaken'),
        (33, 'pay', 'paid', 'paid'),
        (121, 'plead', 'pled/pleaded', 'pled/pleaded'),
        (122, 'preset', 'preset', 'preset'),
        (123, 'prove', 'proved', 'proven/proved'),
        (34, 'put', 'put', 'put'),
        (124, 'quit', 'quit', 'quit'),
        (57, 'read', 'read', 'read'),
        (125, 'relay', 'relaid', 'relaid'),
        (126, 'rend', 'rent', 'rent'),
        (127, 'rid', 'rid', 'rid'),
        (128, 'ride', 'rode', 'ridden'),
        (129, 'ring', 'rang', 'rung'),
        (130, 'rise', 'rose', 'risen'),
        (35, 'run', 'ran', 'run'),
        (131, 'saw', 'saw/sawed', 'saw/sawed'),
        (36, 'say', 'said', 'said'),
        (37, 'see', 'saw', 'seen'),
        (132, 'seek', 'sought', 'sought'),
        (38, 'sell', 'sold', 'sold'),
        (39, 'send', 'sent', 'sent'),
        (40, 'set', 'set', 'set'),
        (133, 'shake', 'shook', 'shaken'),
        (134, 'shed', 'shed', 'shed'),
        (135, 'shine', 'shone', 'shone'),
        (136, 'shoe', 'shod', 'shod'),
        (56, 'shoot', 'shot', 'shot'),
        (137, 'show', 'showed', 'shown'),
        (138, 'shut', 'shut', 'shut'),
        (41, 'sing', 'sang', 'sung'),
        (139, 'sink', 'sank/sunk', 'sunk/sunken'),
        (42, 'sit', 'sat', 'sat'),
        (140, 'slay', 'slew', 'slain'),
        (141, 'sleep', 'slept', 'slept'),
        (142, 'slide', 'slid', 'slid'),
        (143, 'slink', 'slunk/slinked', 'slunk/slinked'),
        (144, 'slit', 'slit', 'slit'),
        (145, 'smell', 'smelt/smelled', 'smelt/smelled'),
        (146, 'sow', 'sowed', 'sown/sowed'),
        (43, 'speak', 'spoke', 'spoken'),
        (147, 'speed', 'sped', 'sped'),
        (148, 'spell', 'spelt', 'spelt'),
        (44, 'spend', 'spent', 'spent'),
        (149, 'spill', 'spilt/spilled', 'spilt/spilled'),
        (150, 'spin', 'spun', 'spun'),
        (151, 'spit', 'spat/spit', 'spat/spit'),
        (152, 'split', 'split', 'split'),
        (153, 'spoil', 'spoilt', 'spoilt'),
        (154, 'spread', 'spread', 'spread'),
        (155, 'spring', 'sprang', 'sprung'),
        (45, 'stand', 'stood', 'stood'),
        (62, 'steal', 'stole', 'stolen'),
        (156, 'stick', 'stuck', 'stuck'),
        (157, 'sting', 'stung', 'stung'),
        (158, 'stink', 'stink', 'stink'),
        (159, 'strew', 'strew', 'strew'),
        (160, 'strike', 'struck', 'stricken/struck'),
        (161, 'strive', 'strove', 'striven'),
        (162, 'swear', 'swore', 'sworn'),
        (163, 'sweat', 'sweat/sweated', 'sweat/sweated'),
        (164, 'sweep', 'swept', 'swept'),
        (165, 'swell', 'swelled', 'swollen/swelled'),
        (63, 'swim', 'swam', 'swum'),
        (46, 'take', 'took', 'taken'),
        (47, 'teach', 'taught', 'taught'),
        (166, 'tear', 'tore', 'torn'),
        (48, 'tell', 'told', 'told'),
        (49, 'think', 'thought', 'thought'),
        (167, 'thrive', 'throve/thrived', 'thriven/thrived'),
        (64, 'throw', 'threw', 'thrown'),
        (168, 'thrust', 'thrust', 'thrust'),
        (169, 'tread', 'trod', 'trodden'),
        (170, 'typeset', 'typeset', 'typeset'),
        (171, 'undergo', 'underwent', 'undergone'),
        (50, 'understand', 'understood', 'understood'),
        (65, 'wake', 'woke', 'woken'),
        (51, 'wear', 'wore', 'worn'),
        (172, 'weep', 'wept', 'wept'),
        (173, 'wet', 'wet/wetted', 'wet/wetted'),
        (52, 'win', 'won', 'won'),
        (174, 'wind', 'wound', 'wound'),
        (175, 'withdraw', 'withdrew', 'withdrawn'),
        (176, 'wring', 'wrung', 'wrung'),
        (53, 'write', 'wrote', 'written'),
    ] # last used is 178
    return content


def get_traductions():
    content = [
        #----------------------------------------------------------------------
        # VAGUE 1 TRADUCTIONS FR->EN
        #----------------------------------------------------------------------
        (1, 1, 100001, None, None),
        (2, 1, 200001, None, None),
        (3, 1, 300001, None, None),
        (6, 9, 100009, None, None),
        (7, 9, 200009, None, None),
        (8, 2, 100002, None, None),
        (9, 3, 100003, None, None),
        (10, 5, 100005, 'dans les airs', None),
        (11, 6, 100006, None, None),
        (12, 7, 100007, None, None),
        (13, 8, 100008, None, None),
        (14, 10, 100010, None, None),
        (15, 11, 100011, None, None),
        (16, 12, 100012, None, None),
        (17, 13, 100013, None, None),
        (18, 14, 100014, None, None),
        (19, 15, 100015, None, None),
        (20, 16, 100016, None, None),
        (21, 17, 100017, None, None),
        (22, 26, 100026, None, None),
        (23, 27, 100027, None, None),
        (24, 28, 100028, "observer, surveiller, visionner (un film, une émission)", None),

        (4, 28, 190028, None, None),
        (5,  6, 100028, "visionner (un film, une émission)", None),

        (25, 29, 100029, None, None),
        (26, 30, 100030, None, None),
        (27, 31, 100031, None, None),
        (28, 32, 100032, None, None),
        (29, 33, 100033, None, None),
        (30, 34, 100034, None, None),
        (31, 35, 100035, None, None),
        (32, 36, 100036, None, None),
        (33, 37, 100037, None, None),
        (34, 38, 100038, None, None),
        (35, 39, 100039, None, None),
        (36, 40, 100040, None, None),
        (37, 41, 100041, 'une odeur', None),
        (38, 42, 100042, None, None),
        (39, 43, 100043, None, None),
        (40, 44, 100044, None, None),
        (41, 45, 100045, None, None),
        (42, 46, 100046, 'amener vers soi un objet', None),
        (43, 47, 100047, None, None),
        (44, 48, 100048, None, None),
        (45, 49, 100049, None, None),
        (46, 50, 100050, None, None),
        (47, 51, 100051, None, None),
        (48, 52, 100052, None, None),
        (49, 53, 100053, None, None),
        (50, 54, 100054, 'parler une langue, échanger des paroles', None),
        (621, 54, 190054, 'échanger des paroles', None),
        (51, 55, 100055, None, None),
        (52, 56, 100056, None, None),
        (53, 57, 100057, None, None),
        (54, 58, 100058, None, None),
        (55, 59, 100059, None, None),
        (56, 60, 100060, None, None),
        (57, 61, 100061, None, None),
        (58, 62, 100062, None, None),
        (59, 63, 100063, "porter un objet", None), # porter => carry
        (60, 64, 100064, None, None),
        (61, 65, 100065, None, None),
        (62, 66, 100066, "présenter quelqu'un", "to introduce someone/something to someone : présenter quelqu'un/quelqu'chose à quelqu'un, to introduce yourself : se présenter, to introduce something into something : introduire quelque chose dans quelque chose"),
        (63, 67, 100067, None, None),
        (64, 68, 100068, None, None),
        (65, 69, 100069, None, None),
        (66, 70, 100070, None, None),
        (67, 71, 100071, None, None),
        (68, 72, 100072, None, None),
        (69, 73, 100073, None, None),
        (70, 74, 100074, None, None),
        (71, 75, 100075, None, None),
        (72, 76, 100076, None, None),
        (73, 77, 100077, None, None),
        (74, 78, 100078, None, None),
        (75, 79, 100079, None, None),
        (76, 80, 100080, None, None),
        (77, 81, 100081, None, None),
        (78, 82, 100082, None, None),
        (79, 83, 100083, None, None),
        (80, 84, 100084, None, None),
        (81, 85, 100085, None, None),
        (82, 86, 100086, None, None),
        (83, 87, 100087, None, None),
        (84, 88, 100088, None, None),
        (85, 89, 100089, None, None),
        (86, 90, 100090, None, None),
        (87, 91, 100091, None, None),
        (88, 92, 100092, None, None),
        (89, 93, 100093, None, None),
        (90, 94, 100094, None, None),
        (91, 95, 100095, None, None),
        (92, 96, 100096, None, None),
        (93, 97, 100097, None, None),
        (94, 98, 100098, None, None),
        (95, 99, 100099, None, None),
        (96, 100, 100100, None, None),
        (97, 101, 100101, None, None),
        (98, 102, 100102, None, None),
        (99, 103, 100103, None, None),
        (100, 104, 100104, None, None),
        (101, 105, 100105, None, None),
        (102, 106, 100038, None, None),
        (103, 107, 100107, None, None),
        (104, 108, 100108, None, None),
        (105, 109, 100109, None, None),
        (106, 110, 100110, None, None),
        (107, 111, 100111, None, None),
        (108, 112, 100112, None, None),
        (109, 113, 100113, None, None),
        (110, 114, 100114, None, None),
        (111, 115, 100115, None, None),
        (112, 116, 100116, None, None),
        (113, 117, 100117, None, None),
        (114, 118, 100118, None, None),
        (115, 119, 100119, None, None),
        (116, 120, 100120, None, None),
        (117, 121, 100121, None, None),
        (118, 122, 100122, None, None),
        (119, 123, 100123, None, None),
        (120, 124, 100124, None, None),
        (121, 125, 100125, None, None),
        (122, 126, 100126, 'quelque part', None),
        (123, 127, 100127, None, None),
        (124, 128, 100128, None, None),
        (125, 129, 100129, None, None),
        (126, 130, 100130, None, None),
        (127, 132, 100132, None, None),
        (128, 133, 100133, None, None),
        (129, 134, 100134, None, None),
        (130, 135, 100135, None, None),
        (131, 136, 100136, None, None),
        (132, 41, 190041, 'un sentiment', None),
        (133, 5, 190005, 'atteinte à la propriété d\'autrui', None),
        (134, 137, 100055, None, None), # CORRECTED
        (135, 46, 190046, 'lancer un projectile', None),

        #----------------------------------------------------------------------
        # VAGUE 1 TRADUCTIONS FR->EO
        #----------------------------------------------------------------------
        (136, 1, 400001, None, None),
        (137, 9, 400009, None, None),
        (139, 2, 400002, None, None),
        (140, 3, 400003, None, None),
        (141, 5, 400005, 'dans les airs', None),
        (142, 6, 400006, None, None),
        (143, 7, 400007, None, None),
        (144, 8, 400008, None, None),
        (145, 10, 400010, None, None),
        (146, 11, 400011, None, None),
        (147, 12, 400012, None, None),
        (148, 13, 400013, None, None),
        (149, 14, 400014, None, None),
        (150, 15, 400015, None, None),
        (151, 16, 400016, None, None),
        (152, 17, 400017, None, None),
        (153, 26, 400026, None, None),
        (154, 27, 400027, None, None),
        (155, 28, 400028, None, None),
        (156, 29, 400029, None, None),
        (157, 30, 400030, None, None),
        (158, 31, 400031, None, None),
        (159, 32, 400032, None, None),
        (160, 33, 400033, None, None),
        (161, 34, 400034, None, None),
        (162, 35, 400035, None, None),
        (163, 36, 400036, None, None),
        (164, 37, 400037, None, None),
        (165, 38, 400038, None, None),
        (166, 39, 400039, None, None),
        (167, 40, 400040, None, None),
        (168, 41, 400041, 'une odeur', None),
        (169, 42, 400042, None, None),
        (170, 43, 400043, None, None),
        (171, 44, 400044, None, None),
        (172, 45, 400045, None, None),
        (173, 46, 400046, 'amener vers soi un objet', None),
        (174, 47, 400047, None, None),
        (175, 48, 400048, None, None),
        (176, 49, 400049, None, None),
        (177, 50, 400050, None, None),
        (178, 51, 400051, None, None),
        (179, 52, 400052, None, None),
        (180, 53, 400053, None, None),
        (181, 54, 400054, None, None),
        (182, 55, 400055, None, None),
        (183, 56, 400056, None, None),
        (184, 57, 400057, None, None),
        (185, 58, 400058, None, None),
        (186, 59, 400059, None, None),
        (187, 60, 400060, None, None),
        (188, 61, 400061, None, None),
        (189, 62, 400062, None, None),
        (190, 63, 400063, None, None),
        (191, 64, 400064, None, None),
        (192, 65, 400065, None, None),
        (193, 66, 400066, None, None),
        (194, 67, 400067, None, None),
        (195, 68, 400068, None, None),
        (196, 69, 400069, None, None),
        (197, 70, 400070, None, None),
        (198, 71, 400071, None, None),
        (199, 72, 400072, None, None),
        (200, 73, 400073, None, None),
        (201, 74, 400074, None, None),
        (202, 75, 400075, None, None),
        (203, 76, 400076, None, None),
        (204, 77, 400077, None, None),
        (205, 78, 400078, None, None),
        (206, 79, 400079, None, None),
        (207, 80, 400080, None, None),
        (208, 81, 400081, None, None),
        (209, 82, 400082, None, None),
        (210, 83, 400083, None, None),
        (211, 84, 400084, None, None),
        (212, 85, 400085, None, None),
        (213, 86, 400086, None, None),
        (214, 87, 400087, None, None),
        (215, 88, 400088, None, None),
        (216, 89, 400089, None, None),
        (217, 90, 400090, None, None),
        (218, 91, 400091, None, None),
        (219, 92, 400092, None, None),
        (220, 93, 400093, None, None),
        (221, 94, 400094, None, None),
        (222, 95, 400095, None, None),
        (223, 96, 400096, None, None),
        (224, 97, 400097, None, None),
        (225, 98, 400098, None, None),
        (226, 99, 400099, None, None),
        (227, 100, 400100, None, None),
        (228, 101, 400101, None, None),
        (229, 102, 400102, None, None),
        (230, 103, 400103, None, None),
        (231, 104, 400104, None, None),
        (232, 105, 400105, None, None),
        (233, 106, 400038, None, None),
        (234, 107, 400107, None, None),
        (235, 108, 400108, None, None),
        (236, 109, 400109, None, None),
        (237, 110, 400110, None, None),
        (238, 111, 400111, None, None),
        (239, 112, 400112, None, None),
        (240, 113, 400113, None, None),
        (241, 114, 400114, None, None),
        (242, 115, 400115, None, None),
        (243, 116, 400116, None, None),
        (244, 117, 400117, None, None),
        (245, 118, 400118, None, None),
        (246, 119, 400119, None, None),
        (247, 120, 400120, None, None),
        (248, 121, 400121, None, None),
        (249, 122, 400122, None, None),
        (250, 123, 400123, None, None),
        (251, 124, 400124, None, None),
        (252, 125, 400125, None, None),
        (253, 126, 400126, 'quelque part', None),
        (254, 127, 400127, None, None),
        (255, 128, 400128, None, None),
        (256, 129, 400129, None, None),
        (257, 130, 400130, None, None),
        (258, 132, 400132, None, None),
        (259, 133, 400133, None, None),
        (260, 134, 400134, None, None),
        (261, 135, 400135, None, None),
        (262, 136, 400136, None, None),
        (265, 137, 400137, None, None),
        (267, 46, 490046, 'lancer un projectile', None),
        (268, 5, 490005, 'atteinte à la propriété d\'autrui', None),
        (269, 41, 490041, 'un sentiment', None),

        #----------------------------------------------------------------------
        # VAGUE 1 TRADUCTIONS FR->IT
        #----------------------------------------------------------------------
        (270, 134, 200134, None, None),
        (271, 124, 200124, None, None),
        (272, 86, 200086, None, None),
        (273, 55, 200055, None, None),
        (274, 66, 200066, None, None),
        (275, 2, 200002, None, None),
        (276, 3, 200003, None, None),
        (277, 5, 200005, 'dans les airs', None),
        (278, 5, 290005, 'dérober', None),
        (279, 6, 200006, None, None),
        (280, 7, 200007, None, None),
        (281, 8, 200008, None, None),
        (282, 10, 200010, None, None),
        (283, 11, 200011, None, None),
        (284, 12, 200012, None, None),
        (285, 13, 200013, None, None),
        (286, 14, 200014, 'd\'une langue à une autre', None),
        (287, 15, 200015, None, None),
        (288, 16, 200016, 'physiquement et émotionnellement', None),
        (289, 17, 200017, None, None),
        (290, 26, 200026, None, None),
        (291, 27, 200027, None, None),
        (292, 28, 200028, None, None),
        (293, 29, 200029, None, None),
        (294, 30, 200030, None, None),
        (295, 31, 200031, None, None),
        (296, 32, 200032, None, None),
        (297, 33, 200033, None, None),
        (298, 34, 200034, None, None),
        (299, 35, 200035, None, None),
        (300, 36, 200036, None, None),
        (301, 37, 200037, None, None),
        (302, 38, 200038, None, None),
        (303, 39, 200039, None, None),
        (304, 40, 200040, None, None),
        (305, 41, 200041, 'une odeur ou un sentiment', None),
        (306, 42, 200042, None, None),
        (307, 43, 200043, None, None),
        (308, 44, 200044, None, None),
        (309, 45, 200045, None, None),
        (310, 46, 200046, None, None),
        (311, 47, 200047, None, None),
        (312, 48, 200048, None, None),
        (313, 49, 200049, None, None),
        (314, 50, 200050, None, None),
        (315, 51, 200051, None, None),
        (316, 52, 200052, None, None),
        (317, 53, 200053, None, None),
        (318, 54, 200054, None, None),
        (319, 56, 200056, None, None),
        (320, 57, 200057, None, None),
        (321, 58, 200058, None, None),
        (322, 59, 200059, None, None),
        (323, 60, 200060, None, None),
        (324, 61, 200061, None, None),
        (325, 62, 200062, None, None),
        (326, 63, 200063, None, None),
        (327, 64, 200064, None, None),
        (328, 65, 200065, None, None),
        # BUG DOUBLE to present fr/it ! (329, 66, 20066, None, None), (274, 66, 20066, None, None),
        (330, 67, 200067, None, None),
        (331, 68, 200068, None, None),
        (332, 69, 200069, None, None),
        (333, 70, 200070, None, None),
        (334, 71, 200071, None, None),
        (335, 72, 200072, None, None),
        (336, 73, 200073, None, None),
        (337, 74, 200074, None, None),
        (338, 75, 200075, 'à un jeu, un sport', None),
        (339, 75, 290075, 'une pièce au théâtre', None),
        (340, 75, 280075, 'd\'un instrument', None),
        (341, 76, 200076, None, None),
        (342, 77, 200077, None, None),
        (343, 78, 200078, None, None),
        (344, 79, 200079, None, None),
        (345, 80, 200080, None, None),
        (346, 81, 200081, None, None),
        (347, 82, 200082, None, None),
        (348, 83, 200083, None, None),
        (349, 84, 200084, None, None),
        (350, 85, 200085, None, None),
        (351, 87, 200087, None, None),
        (352, 88, 200088, None, None),
        (353, 89, 200089, None, None),
        (354, 90, 200041, None, None),
        (355, 91, 200091, None, None),
        (356, 92, 200092, None, None),
        (357, 93, 200093, None, None),
        (358, 94, 200094, None, None),
        (359, 95, 200095, None, None),
        (360, 96, 200096, None, None),
        (361, 97, 200097, None, None),
        (362, 98, 200098, None, None),
        (363, 99, 200099, None, None),
        (364, 100, 200100, None, None),
        (365, 101, 200101, None, None),
        (366, 102, 200102, None, None),
        (367, 103, 200103, None, None),
        (368, 104, 200104, None, None),
        (369, 105, 200105, None, None),
        (370, 106, 200106, None, None),
        (371, 107, 200107, None, None),
        (372, 108, 200108, None, None),
        (373, 109, 200109, None, None),
        (374, 110, 200110, None, None),
        (375, 111, 200111, None, None),
        (376, 112, 200112, None, None),
        (377, 113, 200113, None, None),
        (378, 114, 200114, None, None),
        (379, 115, 200115, None, None),
        (380, 116, 200116, None, None),
        (381, 117, 200117, None, None),
        (382, 118, 200118, None, None),
        (383, 119, 200119, None, None),
        (384, 120, 200120, None, None),
        (385, 121, 200121, None, None),
        (386, 122, 200122, None, None),
        (387, 123, 200123, None, None),
        (388, 125, 200125, None, None),
        (389, 126, 200126, 'quelque part', None),
        (390, 127, 200127, None, None),
        (391, 128, 200128, None, None),
        (392, 129, 200129, None, None),
        (393, 130, 200130, None, None),
        (394, 132, 200132, None, None),
        (395, 133, 200133, None, None),
        (396, 135, 200135, None, None),
        (397, 136, 200136, None, None),
        (398, 137, 200137, None, None),
        
        #----------------------------------------------------------------------
        # VAGUE 1.5 TRADUCTIONS MIXTES FR->EO, EN, IT
        #----------------------------------------------------------------------
        (399, 138, 400138, None, None),
        (400, 139, 400139, None, None),
        (401, 138, 100138, 'vu de l\'intérieur du lieu que l\'on quitte', None),
        (402, 138, 190138, 'vu de l\'extérieur du lieu que l\'on quitte', None),
        (403, 138, 180138, 'sortir quelque chose', None),
        (404, 139, 100139, 'vu de l\'extérieur du lieu où l\'on entre', None),
        (405, 139, 190139, 'vu de l\'intérieur du lieu où l\'on entre', None),
        (406, 139, 180139, 'de façon générale', None),
        (407, 138, 200138, None, None),
        (408, 139, 200139, None, None),
        (409, 86, 290086, 'l\'autre', None),
        (410, 140, 100140, None, None),
        (411, 141, 100141, None, None),
        (412, 140, 200140, None, None),
        (413, 141, 200141, None, None),
        (414, 140, 400140, None, None),
        (415, 141, 400141, None, None),
        (416, 142, 100142, None, None),
        (417, 142, 400142, None, None),
        (418, 142, 200142, None, None),
        (422, 143, 100143, None, None),
        (423, 143, 200143, None, None),
        (424, 143, 400143, None, None),
        (425, 144, 100047, None, None), # CORRECTED
        (426, 144, 200144, None, None),
        (427, 144, 400047, None, None), # CORRECTED
        (428, 145, 100145, None, None),
        (429, 145, 200145, None, None),
        (430, 145, 400145, None, None),
        (431, 146, 100146, None, None),
        (432, 146, 200146, None, None),
        (433, 146, 400146, None, None),
        (434, 147, 100147, 'vu du lieu plus bas', None),
        (435, 147, 190147, 'vu du lieu plus haut', None),
        (436, 147, 400147, None, None),
        (437, 147, 200147, None, None),
        (438, 148, 100148, 'vu du lieu plus haut', None),
        (439, 148, 190148, 'vu du lieu plus bas', None),
        (440, 148, 200148, None, None),
        (441, 148, 400148, None, None),
        (445, 150, 100150, None, None),
        (446, 150, 200150, None, None),
        (447, 150, 400150, None, None),
        (448, 151, 100151, None, None),
        (449, 151, 200151, None, None),
        (450, 151, 400151, None, None),
        #----------------------------------------------------------------------
        # VAGUE 2 TRADUCTIONS FR->EN
        #----------------------------------------------------------------------
        (451, 126, 190126, "une occurrence", None),
        (452, 152, 100152, None, None),
        (453, 153, 100153, None, None),
        (454, 154, 100154, None, None),
        (455, 155, 100155, None, None),
        (456, 156, 100156, "attraper du gibier", None),
        (457, 156, 190156, "expulser", None),
        (458, 158, 100105, None, None),
        (459, 159, 100159, None, None),
        (460, 160, 100003, "vouloir", None),
        (461, 160, 100043, "souhaiter", None),
        (462, 160, 100160, "convoiter (y compris sexuellement)", None),
        (463, 161, 100161, None, None),
        (464, 162, 100162, None, None),
        (465, 163, 100163, None, None),
        (466, 73, 190073, "(se dit également du soleil)", None),
        (467, 84, 190084, "fabriquer", None),
        (468, 164, 100164, None, None),
        (469, 165, 100165, None, None),
        (470, 166, 100166, None, None),
        (471, 167, 100167, None, None),
        (472, 168, 100168, "déraper", None),
        (473, 168, 190168, "se mouvoir de façon fluide", None),
        (474, 169, 100169, None, None),
        (475, 169, 190169, "concerner", None),
        (476,  28, 190169, "concerner", None),
        (477, 170, 100170, "lever", None),
        (478, 170, 190170, "soulever", None),
        (479, 171, 100171, None, None),
        (480, 171, 190171, None, None),
        (481, 171, 180171, None, None),
        (482, 172, 100172, None, None),
        (483, 173, 100173, None, None),
        (484, 174, 100174, None, None),
        (485, 175, 100175, None, None),
        (486, 176, 100176, "immerger (dans l'eau), descendre (dans l'air)", None),
        (487, 177, 100177, None, None),
        (488, 178, 100178, None, None),
        (489, 179, 100179, None, None),
        (490, 180, 100058, None, None),
        (491, 181, 100045, None, None),
        (492, 182, 100182, None, None),
        (493, 183, 100183, None, None),
        (494, 184, 100184, None, None),
        (495, 185, 100185, None, None),
        (496, 186, 100076, None, None),
        (597, 187, 100187, None, None),
        #(666, 187, 99999, None) # ERREUR VOLONTAIRE "VERS" DE TEST
        #(666, 19999, 187, None) # ERREUR VOLONTAIRE "DE" DE TEST    
        #----------------------------------------------------------------------
        # VAGUE 3 TRADUCTIONS FR->EN
        #----------------------------------------------------------------------
        (598, 188, 100188, None, None),
        (599, 189, 100189, None, None),
        (600, 190, 100190, None, None),
        (601, 191, 100191, None, None),
        (602, 192, 100192, None, None),
        (603, 193, 100193, None, None),
        (604, 194, 100194, None, None),
        (605, 195, 100195, None, None),
        (606, 63, 190063, "porter un vêtement", None),
        (607, 196, 100196, None, None), # être debout => stand
        (609, 197, 100197, None, None), # être assis => sit
        (610, 150, 100197, None, None), # s'assoir => sit
        #----------------------------------------------------------------------
        # VAGUE 4 TRADUCTIONS FR->EN
        #----------------------------------------------------------------------
        (618, 201, 100201, None, None), # tuer => kill
        (619, 202, 100202, None, None), # blesser => hurt
        (620, 203, 100203, None, None), # combattre => fight
        
        #----------------------------------------------------------------------
        # VAGUES 1 & 2 TRADUCTIONS EN->FR
        #----------------------------------------------------------------------
		(10000, 100001, 1, None, "ouvrir quelque chose : to open something"), # open => ouvrir
		(60000, 100009, 9, None, "venir de quelque part : to come from somewhere, venir ici : to come here, venir jusqu'ici : to come this far"), # come => venir
		(80000, 100002, 2, None, "voyager : to travel"), # travel => voyager
		(90000, 100003, 3, None, "vouloir quelque chose : want something, vouloir faire quelque chose : want to do something"), # want => vouloir
		(100000, 100005, 5, "dans les airs", "voler dans les airs : to fly"), # fly => voler
		(110000, 100006, 6, None, 'to see something'), # see => voir
		(120000, 100007, 7, None, None), # live => vivre
		(130000, 100008, 8, None, None), # visit => visiter
		(140000, 100010, 10, None, None), # sell => vendre
		(150000, 100011, 11, None, None), # use => utiliser
		(160000, 100012, 12, None, None), # find => trouver
		(170000, 100013, 13, None, None), # work => travailler
		(180000, 100014, 14, None, None), # translate => traduire
		(190000, 100015, 15, None, None), # turn => tourner
		(200000, 100016, 16, None, None), # touch => toucher
		(210000, 100017, 17, None, None), # fall => tomber
		(220000, 100026, 26, None, None), # tell => raconter
		(230000, 100027, 27, None, None), # receive => recevoir
		(240000, 100028, 28, "observer, surveiller, visionner (un film, une émission)", None), # watch => regarder
		(40000, 190028, 28, None, None), # look at => regarder
		(50000, 100028, 6, "visionner (un film, une émission)", None), # watch => voir
		(250000, 100029, 29, None, None), # thank => remercier
		(260000, 100030, 30, None, None), # meet => rencontrer
		(270000, 100031, 31, None, None), # answer => répondre
		(280000, 100032, 32, None, None), # stay => rester
		(290000, 100033, 33, None, None), # success => réussir
		(300000, 100034, 34, None, None), # wake up => réveiller (se)
		(310000, 100035, 35, None, None), # laugh => rire
		(320000, 100036, 36, None, None), # take care => occuper (s')
		(330000, 100037, 37, None, None), # jump => sauter
		(340000, 100038, 38, None, None), # know => savoir
		(350000, 100039, 39, None, None), # rest => reposer (se)
		(360000, 100040, 40, None, None), # remember => souvenir (se)
		(370000, 100041, 41, "une odeur", None), # smell => sentir
		(380000, 100042, 42, None, None), # suffer => souffrir
		(390000, 100043, 43, None, "souhaiter que quelqu'un fasse quelque chose : to wish someone to do something, souhaiter faire quelque chose : to wish to do something, souhaiter quelque chose : to wish for something, souhaiter quelque chose à quelqu'un : to wish someone something, souhaiter quelque chose : to wish (that) proposition"), # wish => souhaiter
		(400000, 100044, 44, None, None), # follow => suivre
		(410000, 100045, 45, None, None), # hold => tenir
		(420000, 100046, 46, "amener vers soi un objet", None), # pull => tirer
		(430000, 100047, 47, None, None), # put => mettre
		(440000, 100048, 48, None, None), # show => montrer
		(450000, 100049, 49, None, None), # die => mourir
		(460000, 100050, 50, None, None), # swim => nager
		(470000, 100051, 51, None, None), # be born => naître
		(480000, 100052, 52, None, None), # forget => oublier
		(490000, 100053, 53, None, None), # forgive => pardonner
		(500000, 100054, 54, 'parler une langue, échanger des paroles', None), # speak => parler
       (6210000, 190054, 54, 'échanger des paroles', None), # talk => parler
		(510000, 100055, 55, None, None), # go => partir
		(520000, 100056, 56, None, None), # pass => passer
		(530000, 100057, 57, None, None), # pay => payer
		(540000, 100058, 58, None, None), # think => penser
		(550000, 100059, 59, None, None), # lose => perdre
		(560000, 100060, 60, None, None), # allow => permettre
		(570000, 100061, 61, None, None), # please => plaire
		(580000, 100062, 62, None, None), # cry => pleurer
		(590000, 100063, 63, "porter un objet", None), # carry => porter
		(600000, 100064, 64, None, None), # can => pouvoir
		(610000, 100065, 65, None, None), # take => prendre
		(620000, 100066, 66, "présenter quelqu'un", "présenter quelqu'un/quelqu'chose à quelqu'un : to introduce someone/something to someone, se présenter : to introduce yourself, introduire quelque chose dans quelque chose : to introduce something into something"), # introduce yourself => présenter (se)
		(630000, 100067, 67, None, None), # pledge => promettre
		(640000, 100068, 68, None, None), # leave => quitter
		(650000, 100069, 69, None, None), # walk => marcher
		(660000, 100070, 70, None, None), # miss => manquer
		(670000, 100071, 71, None, None), # eat => manger
		(680000, 100072, 72, None, None), # read => lire
		(690000, 100073, 73, None, None), # stand up => lever (se)
		(700000, 100074, 74, None, None), # wash => laver
		(710000, 100075, 75, None, None), # play => jouer
		(720000, 100076, 76, None, None), # throw => jeter
		(730000, 100077, 77, None, None), # invite => inviter
		(740000, 100078, 78, None, None), # live in => habiter
		(750000, 100079, 79, None, None), # dress => habiller (s')
		(760000, 100080, 80, None, None), # taste => goûter
		(770000, 100081, 81, None, None), # win => gagner
		(780000, 100082, 82, None, None), # finish => finir
		(790000, 100083, 83, None, None), # close => fermer
		(800000, 100084, 84, None, None), # do => faire
		(810000, 100085, 85, None, None), # study => étudier
		(820000, 100086, 86, None, None), # be => être
		(830000, 100087, 87, None, None), # try => essayer
		(840000, 100088, 88, None, None), # hope => espérer
		(850000, 100089, 89, None, None), # send => envoyer
		(860000, 100090, 90, None, None), # hear => entendre
		(870000, 100091, 91, None, None), # teach => enseigner
		(880000, 100092, 92, None, None), # write => écrire
		(890000, 100093, 93, None, None), # listen => écouter
		(900000, 100094, 94, None, None), # sleep => dormir
		(910000, 100095, 95, None, None), # say => dire
		(920000, 100096, 96, None, None), # must => devoir
		(930000, 100097, 97, None, None), # ask => demander
		(940000, 100098, 98, None, None), # dance => danser
		(950000, 100099, 99, None, None), # cook => cuire
		(960000, 100100, 100, None, None), # believe => croire
		(970000, 100101, 101, None, None), # shout => crier
		(980000, 100102, 102, None, None), # create => créer
		(990000, 100103, 103, None, None), # cost => coûter
		(1000000, 100104, 104, None, None), # run => courir 
		(1010000, 100105, 105, None, None), # build => construire
		(1020000, 100038, 106, None, None), # know => connaître
		(1030000, 100107, 107, None, None), # drive => conduire
		(1040000, 100108, 108, None, None), # count => compter
		(1050000, 100109, 109, None, None), # understand => comprendre
		(1060000, 100110, 110, None, None), # begin => commencer
		(1070000, 100111, 111, None, None), # choose => choisir
		(1080000, 100112, 112, None, None), # look for => chercher
		(1090000, 100113, 113, None, None), # sing => chanter
		(1100000, 100114, 114, None, None), # change => changer
		(1110000, 100115, 115, None, None), # break => casser
		(1120000, 100116, 116, None, None), # hide => cacher
		(1130000, 100117, 117, None, None), # burn => brûler
		(1140000, 100118, 118, None, None), # move => bouger
		(1150000, 100119, 119, None, None), # drink => boire
		(1160000, 100120, 120, None, None), # chat => bavarder
		(1170000, 100121, 121, None, None), # be afraid => avoir peur
		(1180000, 100122, 122, None, None), # trust => avoir confiance
		(1190000, 100123, 123, None, None), # need => avoir besoin
		(1200000, 100124, 124, None, None), # have => avoir
		(1210000, 100125, 125, None, None), # wait => attendre
		(1220000, 100126, 126, "quelque part", None), # arrive => arriver
		(1230000, 100127, 127, None, None), # stop => arrêter
		(1240000, 100128, 128, None, None), # learn => apprendre
		(1250000, 100129, 129, None, None), # like => apprécier
		(1260000, 100130, 130, None, None), # call => appeler
		(1270000, 100132, 132, None, None), # love => aimer
		(1280000, 100133, 133, None, None), # buy => acheter
		(1290000, 100134, 134, None, None), # help => aider
		(1300000, 100135, 135, None, None), # give => donner
		(1310000, 100136, 136, None, None), # come back => revenir
		(1320000, 190041, 41, "un sentiment", None), # feel => sentir
		(1330000, 190005, 5, "atteinte à la propriété d'autrui", None), # steal => voler
		(1340000, 100055, 137, None, None), # go => aller
		(1350000, 190046, 46, "lancer un projectile", None), # shoot => tirer
		(4010000, 100138, 138, "vu de l'intérieur du lieu que l'on quitte", None), # go out => sortir
		(4020000, 190138, 138, "vu de l'extérieur du lieu que l'on quitte", None), # come out => sortir
		(4030000, 180138, 138, "sortir quelque chose", None), # take out => sortir
		(4040000, 100139, 139, "vu de l'extérieur du lieu où l'on entre", None), # go in => entrer
		(4050000, 190139, 139, "vu de l'intérieur du lieu où l'on entre", None), # come in => entrer
		(4060000, 180139, 139, "de façon générale", None), # enter => entrer
		(4100000, 100140, 140, None, None), # turn on => allumer
		(4110000, 100141, 141, None, None), # turn off => éteindre
        (4160000, 100142, 142, None, None), # suggest => proposer
		(4220000, 100143, 143, None, None), # decide => décider
		(4250000, 100047, 144, None, None), # put => poser
		(4280000, 100145, 145, None, None), # reduce => réduire
        (4310000, 100146, 146, None, None), # fill => remplir
		(4340000, 100147, 147, "vu du lieu plus bas", None), # go up => monter
		(4350000, 190147, 147, "vu du lieu plus haut", None), # come up => monter
		(4380000, 100148, 148, "vu du lieu plus haut", None), # go down => descendre
		(4390000, 190148, 148, "vu du lieu plus bas", None), # come down => descendre
        (4450000, 100150, 150, None, None), # sit down => asseoir (s')
        (4480000, 100151, 151, None, None), # remove => enlever
        (4510000, 190126, 126, "une occurrence", None), # happen => arriver VAGUE 2
		(4520000, 100152, 152, None, "ajouter quelque chose à quelque chose : to add something to something"), # add => ajouter VAGUE 2
		(4530000, 100153, 153, None, None), # catch => attraper VAGUE 2
		(4540000, 100154, 154, None, None), # increase => augmenter VAGUE 2
		(4550000, 100155, 155, None, None), # shine => briller VAGUE 2
		(4560000, 100156, 156, "attraper du gibier", None), # hunt => chasser VAGUE 2
		(4570000, 190156, 156, "expulser", None), # drive out => chasser VAGUE 2
		(4580000, 100105, 158, None, None), # build => bâtir
		(4590000, 100159, 159, None, None), # discover => découvrir  VAGUE 2
		(4600000, 100003, 160, "vouloir", None), # want => désirer
		(4610000, 100043, 160, "dans le sens de souhaiter", None), # wish => désirer
		(4620000, 100160, 160, "convoiter (y compris sexuellement)", None), # desire => désirer VAGUE 2
		(4630000, 100161, 161, None, None), # guess => deviner VAGUE 2
		(4640000, 100162, 162, None, None), # decrease => diminuer VAGUE 2
		(4650000, 100163, 163, None, None), # discuss => discuter VAGUE 2
		(4660000, 190073, 73, "(se dit également du soleil)", None), # rise => lever (se)
		(4670000, 190084, 84, "fabriquer", None), # make => faire
		(4680000, 100164, 164, None, None), # disappear => disparaître VAGUE 2
		(4690000, 100165, 165, None, None), # last => durer VAGUE 2
		(4700000, 100166, 166, None, None), # agree => être d'accord VAGUE 2
		(4710000, 100167, 167, None, None), # moan => gémir VAGUE 2
		(4720000, 100168, 168, "déraper", None), # slip => glisser VAGUE 2
		(4730000, 190168, 168, "se mouvoir de façon fluide", None), # glide => glisser VAGUE 2
		(4740000, 100169, 169, None, None), # interest => intéresser VAGUE 2
		(4750000, 190169, 169, "concerner", None), # concern => intéresser VAGUE 2
		(4760000, 190169, 28, "concerner", None), # concern => regarder VAGUE 2
		(4770000, 100170, 170, "lever", None), # raise => lever VAGUE 2
		(4780000, 190170, 170, "soulever", None), # lift => lever VAGUE 2
		(4790000, 100171, 171, None, None), # rent => louer VAGUE 2
		(4800000, 190171, 171, None, None), # hire => louer VAGUE 2
		(4810000, 180171, 171, None, None), # lease => louer VAGUE 2
		(4820000, 100172, 172, None, None), # feed => nourrir VAGUE 2
		(4830000, 100173, 173, None, None), # share => partager VAGUE 2
		(4840000, 100174, 174, None, None), # hang => pendre VAGUE 2
		(4850000, 100175, 175, None, None), # fold => plier VAGUE 2
		(4860000, 100176, 176, "immerger (dans l'eau), descendre (dans l'air)", None), # dive => plonger VAGUE 2
		(4870000, 100177, 177, None, None), # push => pousser VAGUE 2
		(4880000, 100178, 178, None, None), # lend => prêter VAGUE 2
		(4890000, 100179, 179, None, None), # produce => produire VAGUE 2
		(4900000, 100058, 180, None, None), # think => réfléchir
		(4910000, 100045, 181, None, None), # hold => retenir
		(4920000, 100182, 182, None, None), # dream => rêver VAGUE 2
		(4930000, 100183, 183, None, None), # be worth => valoir VAGUE 2
		(4940000, 100184, 184, None, None), # empty => vider VAGUE 2
		(4950000, 100185, 185, None, None), # become => devenir VAGUE 2
		(4960000, 100076, 186, None, None), # throw => lancer VAGUE 2
		(5970000, 100187, 187, None, None), # bring => apporter VAGUE 2
		(5980000, 100188, 188, None, None), # cut => couper VAGUE 3
		(5990000, 100189, 189, None, None), # draw => dessiner VAGUE 3
		(6000000, 100190, 190, None, None), # keep => garder VAGUE 3
		(6010000, 100191, 191, None, None), # lead => mener VAGUE 3
		(6020000, 100192, 192, None, None), # let => laisser VAGUE 3
		(6030000, 100193, 193, None, None), # lie => mentir VAGUE 3
		(6040000, 100194, 194, None, None), # mean => signifier VAGUE 3
		(6050000, 100195, 195, None, None), # spend => dépenser VAGUE 3
		(6060000, 190063, 63, "porter un vêtement", None), # wear => porter VAGUE 3
		(6070000, 100196, 196, None, None), # stand => être debout VAGUE 3
		(6090000, 100197, 197, None, None), # sit => être assis VAGUE 3
		(6100000, 100197, 150, None, None), # sit => asseoir (s') VAGUE 3
        #----------------------------------------------------------------------
        # VAGUE 3 TRADUCTIONS EN->FR (La vague 3 est uniquement dans le sens EN->FR)
        #----------------------------------------------------------------------
        (6080000, 100196, 86, None, None), # stand => être VAGUE 3
        (6110000, 100197, 86, None, None), # sit => être VAGUE 3
        (6120000, 100199, 124, None, None), # get => avoir VAGUE 3
        (6130000, 100199, 27, None, None), # get => recevoir VAGUE 3
        (6140000, 100199, 109, None, None), # get => comprendre VAGUE 3
        (6150000, 100200, 102, None, None), # set => créer VAGUE 3
        (6160000, 100200, 47, None, None), # set => mettre VAGUE 3
        (6170000, 100200, 144, None, None), # set => poser VAGUE 3
        #----------------------------------------------------------------------
        # VAGUE 4 TRADUCTIONS EN->FR
        #----------------------------------------------------------------------
        (6180000, 100201, 201, None, None), # kill => tuer
        (6190000, 100202, 202, None, None), # hurt => blesser
        (6200000, 100203, 203, None, None), # fight => combattre
        #----------------------------------------------------------------------
        # VAGUE 5 TRADUCTIONS EN->FR
        #----------------------------------------------------------------------
        
        (620001, 100214, 214, None, None), # blow => souffler
        (620002, 100211, 211, None, None), # bind => attacher
        (620003, 100211, 90211, None, None), # bind => lier
        (620004, 100227, 227, None, None), # check => vérifier
        (620005, 100207, 207, None, None), # beat => battre
        (620006, 100212, 212, None, None), # bite => mordre
        (620007, 100213, 213, None, None), # bleed => saigner
        (620008, 100225, 225, None, None), # cancel => annuler
        (620009, 190225, 225, None, None), # call off => annuler
        
        #----------------------------------------------------------------------
        # VAGUE 1 TRADUCTIONS EN->EO
        #----------------------------------------------------------------------
		(1360000, 400001, 1, None, None), # ouvrir
		(1370000, 400009, 9, None, None), # venir
		(1390000, 400002, 2, None, None),
		(1400000, 400003, 3, None, None),
		(1410000, 400005, 5, "dans les airs", None),
		(1420000, 400006, 6, None, None),
		(1430000, 400007, 7, None, None),
		(1440000, 400008, 8, None, None),
		(1450000, 400010, 10, None, None),
		(1460000, 400011, 11, None, None),
		(1470000, 400012, 12, None, None),
		(1480000, 400013, 13, None, None),
		(1490000, 400014, 14, None, None),
		(1500000, 400015, 15, None, None),
		(1510000, 400016, 16, None, None),
		(1520000, 400017, 17, None, None),
		(1530000, 400026, 26, None, None),
		(1540000, 400027, 27, None, None),
		(1550000, 400028, 28, None, None),
		(1560000, 400029, 29, None, None),
		(1570000, 400030, 30, None, None),
		(1580000, 400031, 31, None, None),
		(1590000, 400032, 32, None, None),
		(1600000, 400033, 33, None, None),
		(1610000, 400034, 34, None, None),
		(1620000, 400035, 35, None, None),
		(1630000, 400036, 36, None, None),
		(1640000, 400037, 37, None, None),
		(1650000, 400038, 38, None, None),
		(1660000, 400039, 39, None, None),
		(1670000, 400040, 40, None, None),
		(1680000, 400041, 41, "une odeur", None),
		(1690000, 400042, 42, None, None),
		(1700000, 400043, 43, None, None),
		(1710000, 400044, 44, None, None),
		(1720000, 400045, 45, None, None),
		(1730000, 400046, 46, "amener vers soi un objet", None),
		(1740000, 400047, 47, None, None),
		(1750000, 400048, 48, None, None),
		(1760000, 400049, 49, None, None),
		(1770000, 400050, 50, None, None),
		(1780000, 400051, 51, None, None),
		(1790000, 400052, 52, None, None),
		(1800000, 400053, 53, None, None),
		(1810000, 400054, 54, None, None),
		(1820000, 400055, 55, None, None),
		(1830000, 400056, 56, None, None),
		(1840000, 400057, 57, None, None),
		(1850000, 400058, 58, None, None),
		(1860000, 400059, 59, None, None),
		(1870000, 400060, 60, None, None),
		(1880000, 400061, 61, None, None),
		(1890000, 400062, 62, None, None),
		(1900000, 400063, 63, None, None),
		(1910000, 400064, 64, None, None),
		(1920000, 400065, 65, None, None),
		(1930000, 400066, 66, None, None),
		(1940000, 400067, 67, None, None),
		(1950000, 400068, 68, None, None),
		(1960000, 400069, 69, None, None),
		(1970000, 400070, 70, None, None),
		(1980000, 400071, 71, None, None),
		(1990000, 400072, 72, None, None),
		(2000000, 400073, 73, None, None),
		(2010000, 400074, 74, None, None),
		(2020000, 400075, 75, None, None),
		(2030000, 400076, 76, None, None),
		(2040000, 400077, 77, None, None),
		(2050000, 400078, 78, None, None),
		(2060000, 400079, 79, None, None),
		(2070000, 400080, 80, None, None),
		(2080000, 400081, 81, None, None),
		(2090000, 400082, 82, None, None),
		(2100000, 400083, 83, None, None),
		(2110000, 400084, 84, None, None),
		(2120000, 400085, 85, None, None),
		(2130000, 400086, 86, None, None),
		(2140000, 400087, 87, None, None),
		(2150000, 400088, 88, None, None),
		(2160000, 400089, 89, None, None),
		(2170000, 400090, 90, None, None),
		(2180000, 400091, 91, None, None),
		(2190000, 400092, 92, None, None),
		(2200000, 400093, 93, None, None),
		(2210000, 400094, 94, None, None),
		(2220000, 400095, 95, None, None),
		(2230000, 400096, 96, None, None),
		(2240000, 400097, 97, None, None),
		(2250000, 400098, 98, None, None),
		(2260000, 400099, 99, None, None),
		(2270000, 400100, 100, None, None),
		(2280000, 400101, 101, None, None),
		(2290000, 400102, 102, None, None),
		(2300000, 400103, 103, None, None),
		(2310000, 400104, 104, None, None),
		(2320000, 400105, 105, None, None),
		(2330000, 400038, 106, None, None),
		(2340000, 400107, 107, None, None),
		(2350000, 400108, 108, None, None),
		(2360000, 400109, 109, None, None),
		(2370000, 400110, 110, None, None),
		(2380000, 400111, 111, None, None),
		(2390000, 400112, 112, None, None),
		(2400000, 400113, 113, None, None),
		(2410000, 400114, 114, None, None),
		(2420000, 400115, 115, None, None),
		(2430000, 400116, 116, None, None),
		(2440000, 400117, 117, None, None),
		(2450000, 400118, 118, None, None),
		(2460000, 400119, 119, None, None),
		(2470000, 400120, 120, None, None),
		(2480000, 400121, 121, None, None),
		(2490000, 400122, 122, None, None),
		(2500000, 400123, 123, None, None),
		(2510000, 400124, 124, None, None),
		(2520000, 400125, 125, None, None),
		(2530000, 400126, 126, "quelque part", None),
		(2540000, 400127, 127, None, None),
		(2550000, 400128, 128, None, None),
		(2560000, 400129, 129, None, None),
		(2570000, 400130, 130, None, None),
		(2580000, 400132, 132, None, None),
		(2590000, 400133, 133, None, None),
		(2600000, 400134, 134, None, None),
		(2610000, 400135, 135, None, None),
		(2620000, 400136, 136, None, None),
		(2650000, 400137, 137, None, None),
		(2670000, 490046, 46, "lancer un projectile", None),
		(2680000, 490005, 5, "atteinte à la propriété d'autrui", None),
		(2690000, 490041, 41, "un sentiment", None),
        (3990000, 400138, 138, None, None),
		(4000000, 400139, 139, None, None),
        (4140000, 400140, 140, None, None),
		(4150000, 400141, 141, None, None),
        (4170000, 400142, 142, None, None),
		(4240000, 400143, 143, None, None),
		(4270000, 400047, 144, None, None),
		(4300000, 400145, 145, None, None),
		(4330000, 400146, 146, None, None),
		(4360000, 400147, 147, None, None),
		(4410000, 400148, 148, None, None),
		(4470000, 400150, 150, None, None),
		(4500000, 400151, 151, None, None),
        
        # TRADUCTIONS IT->FR
		(2700000, 200134, 134, None, None),
		(2710000, 200124, 124, None, None),
		(2720000, 200086, 86, None, None),
		(2730000, 200055, 55, None, None),
		(2740000, 200066, 66, None, None),
		(2750000, 200002, 2, None, None),
		(2760000, 200003, 3, None, None),
		(2770000, 200005, 5, "dans les airs", None),
		(2780000, 290005, 5, "dérober", None),
		(2790000, 200006, 6, None, None),
		(2800000, 200007, 7, None, None),
		(2810000, 200008, 8, None, None),
		(2820000, 200010, 10, None, None),
		(2830000, 200011, 11, None, None),
		(2840000, 200012, 12, None, None),
		(2850000, 200013, 13, None, None),
		(2860000, 200014, 14, "dune langue à une autre", None),
		(2870000, 200015, 15, None, None),
		(2880000, 200016, 16, "physiquement et émotionnellement", None),
		(2890000, 200017, 17, None, None),
		(2900000, 200026, 26, None, None),
		(2910000, 200027, 27, None, None),
		(2920000, 200028, 28, None, None),
		(2930000, 200029, 29, None, None),
		(2940000, 200030, 30, None, None),
		(2950000, 200031, 31, None, None),
		(2960000, 200032, 32, None, None),
		(2970000, 200033, 33, None, None),
		(2980000, 200034, 34, None, None),
		(2990000, 200035, 35, None, None),
		(3000000, 200036, 36, None, None),
		(3010000, 200037, 37, None, None),
		(3020000, 200038, 38, None, None),
		(3030000, 200039, 39, None, None),
		(3040000, 200040, 40, None, None),
		(3050000, 200041, 41, "une odeur ou un sentiment", None),
		(3060000, 200042, 42, None, None),
		(3070000, 200043, 43, None, None),
		(3080000, 200044, 44, None, None),
		(3090000, 200045, 45, None, None),
		(3100000, 200046, 46, None, None),
		(3110000, 200047, 47, None, None),
		(3120000, 200048, 48, None, None),
		(3130000, 200049, 49, None, None),
		(3140000, 200050, 50, None, None),
		(3150000, 200051, 51, None, None),
		(3160000, 200052, 52, None, None),
		(3170000, 200053, 53, None, None),
		(3180000, 200054, 54, None, None),
		(3190000, 200056, 56, None, None),
		(3200000, 200057, 57, None, None),
		(3210000, 200058, 58, None, None),
		(3220000, 200059, 59, None, None),
		(3230000, 200060, 60, None, None),
		(3240000, 200061, 61, None, None),
		(3250000, 200062, 62, None, None),
		(3260000, 200063, 63, None, None),
		(3270000, 200064, 64, None, None),
		(3280000, 200065, 65, None, None),
		(3300000, 200067, 67, None, None),
		(3310000, 200068, 68, None, None),
		(3320000, 200069, 69, None, None),
		(3330000, 200070, 70, None, None),
		(3340000, 200071, 71, None, None),
		(3350000, 200072, 72, None, None),
		(3360000, 200073, 73, None, None),
		(3370000, 200074, 74, None, None),
		(3380000, 200075, 75, "à un jeu, un sport", None),
		(3390000, 290075, 75, "une pièce au théâtre", None),
		(3400000, 280075, 75, "d'un instrument", None),
		(3410000, 200076, 76, None, None),
		(3420000, 200077, 77, None, None),
		(3430000, 200078, 78, None, None),
		(3440000, 200079, 79, None, None),
		(3450000, 200080, 80, None, None),
		(3460000, 200081, 81, None, None),
		(3470000, 200082, 82, None, None),
		(3480000, 200083, 83, None, None),
		(3490000, 200084, 84, None, None),
		(3500000, 200085, 85, None, None),
		(3510000, 200087, 87, None, None),
		(3520000, 200088, 88, None, None),
		(3530000, 200089, 89, None, None),
		(3540000, 200041, 90, None, None),
		(3550000, 200091, 91, None, None),
		(3560000, 200092, 92, None, None),
		(3570000, 200093, 93, None, None),
		(3580000, 200094, 94, None, None),
		(3590000, 200095, 95, None, None),
		(3600000, 200096, 96, None, None),
		(3610000, 200097, 97, None, None),
		(3620000, 200098, 98, None, None),
		(3630000, 200099, 99, None, None),
		(3640000, 200100, 100, None, None),
		(3650000, 200101, 101, None, None),
		(3660000, 200102, 102, None, None),
		(3670000, 200103, 103, None, None),
		(3680000, 200104, 104, None, None),
		(3690000, 200105, 105, None, None),
		(3700000, 200106, 106, None, None),
		(3710000, 200107, 107, None, None),
		(3720000, 200108, 108, None, None),
		(3730000, 200109, 109, None, None),
		(3740000, 200110, 110, None, None),
		(3750000, 200111, 111, None, None),
		(3760000, 200112, 112, None, None),
		(3770000, 200113, 113, None, None),
		(3780000, 200114, 114, None, None),
		(3790000, 200115, 115, None, None),
		(3800000, 200116, 116, None, None),
		(3810000, 200117, 117, None, None),
		(3820000, 200118, 118, None, None),
		(3830000, 200119, 119, None, None),
		(3840000, 200120, 120, None, None),
		(3850000, 200121, 121, None, None),
		(3860000, 200122, 122, None, None),
		(3870000, 200123, 123, None, None),
		(3880000, 200125, 125, None, None),
		(3890000, 200126, 126, "quelque part", None),
		(3900000, 200127, 127, None, None),
		(3910000, 200128, 128, None, None),
		(3920000, 200129, 129, None, None),
		(3930000, 200130, 130, None, None),
		(3940000, 200132, 132, None, None),
		(3950000, 200133, 133, None, None),
		(3960000, 200135, 135, None, None),
		(3970000, 200136, 136, None, None),
		(3980000, 200137, 137, None, None),
        (4070000, 200138, 138, None, None),
        (4080000, 200139, 139, None, None),
		(4090000, 290086, 86, "l'autre", None),
        (4120000, 200140, 140, None, None),
		(4130000, 200141, 141, None, None),
        (4180000, 200142, 142, None, None),
		(4230000, 200143, 143, None, None),
        (4260000, 200144, 144, None, None),
		(4290000, 200145, 145, None, None),
		(4320000, 200146, 146, None, None),
		(4370000, 200147, 147, None, None),
		(4400000, 200148, 148, None, None),
		(4460000, 200150, 150, None, None),
		(4490000, 200151, 151, None, None),
		(20000, 200001, 1, None, None), # ouvrir
		(70000, 200009, 9, None, None), # venir
        
        # TRADUCTION DE->FR
        (30000, 300001, 1, None, None), # ouvrir
        ]
    return content

def make_reverse_traductions():
    pass
    
    # Adding reverse translation only for en -> fr
    #f = open('zorba.txt', 'w', encoding='utf-8')
    #id = 700
    #added = []
    #for cc in content:
    #    #id += 1
    #    de = cc[1]
    #    vers = cc[2]
    #    comment = cc[3]
    #    if vers >= 100000: # only vers des verbes anglais
    #        added.append((cc[0]*1000+1, cc[2], cc[1], cc[3])) #id
    #        if cc[3] is not None:
    #            f.write('\t\t(' + str(cc[0]*10000) + ', ' + str(cc[2]) + ', ' + str(cc[1]) + ', "' + str(cc[3]) + '"),\n')
    #        else:
    #            f.write('\t\t(' + str(cc[0]*10000) + ', ' + str(cc[2]) + ', ' + str(cc[1]) + ', ' + str(cc[3]) + '),\n')
    #f.close()
    #for aa in added:
    #    content.append(aa)
    