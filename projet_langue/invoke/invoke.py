# ------------------------------------------------------------------------------
# Local version of Invoke
# Recreate the database of words
# ------------------------------------------------------------------------------

import os
import sys
import sqlite3
import unicodedata

# print("Current working dir : " + os.getcwd())
# os.chdir("C:\\Users\\damie_000\\Documents\GitHub\\tallentaa\\projet_langue\\invoke")
# print("Current working dir : " + os.getcwd())


def check_content_verbs(content):
    # Test de l'unicité des ids et des bases
    verbes_id = []
    verbes_base_lang = {}
    error = False
    for cc in content:
        id = cc[0]
        if id in verbes_id:
            print("ERROR : id 2x : " + str(id))
            error = True
        else:
            verbes_id.append(id)
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
    c.execute("CREATE TABLE IF NOT EXISTS voc_translate ( id int(11) NOT NULL, de int(11) NOT NULL, vers int(11) NOT NULL, sens varchar(100) DEFAULT NULL, PRIMARY KEY (`id`) ) ")

    c.execute("CREATE TABLE IF NOT EXISTS voc_verbs_en ( id int(11) NOT NULL, base varchar(50) NOT NULL, pret varchar(50) NOT NULL, part varchar(50) NOT NULL )")
    
    # Tables filling

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
        (36, 'fr', 'occuper (s'')', 'verb', 1),
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
        (79, 'fr', 'habiller (s'')', 'verb', 1),
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
        (150, 'fr', 'asseoir (s'')', 'verb', 1),
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
        (166, 'fr', 'être d''accord', 'verb', 2),
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
        (100066, 'en', 'introduce yourself', 'verb', 1),
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

        # VAGUE 2
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
        
        # VAGUE 3
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
        (21000, 'fr', 'livre', 'noun', 1),   (11000, 'en', 'book', 'noun', 1),
        (21001, 'fr', 'lit', 'noun', 1),     (11001, 'en', 'bed', 'noun', 1),
        (21002, 'fr', 'père', 'noun', 1),    (11002, 'en', 'father', 'noun', 1),
        (21003, 'fr', 'mère', 'noun', 1),    (11003, 'en', 'mother', 'noun', 1),
        (21004, 'fr', 'frère', 'noun', 1),   (11004, 'en', 'brother', 'noun', 1),
        (21005, 'fr', 'sœur', 'noun', 1),    (11005, 'en', 'sister', 'noun', 1),
        (21006, 'fr', 'fils', 'noun', 1),    (11006, 'en', 'son', 'noun', 1),
        (21007, 'fr', 'fille', 'noun', 1),   (11007, 'en', 'daughter', 'noun', 1),
                                            (18007, 'en', 'girl', 'noun', 1),
        (21008, 'fr', 'garçon', 'noun', 1),  (11008, 'en', 'boy', 'noun', 1),

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

    verbes_id = check_content_verbs(content)

    c.executemany('INSERT INTO voc_verbs VALUES (?,?,?,?,?)', content)
    #c.execute("INSERT INTO verbs VALUES ('ŝteli')")

    #----------------------------------------------------------------
    # VERBES ANGLAIS IRRÉGULIERS
    #----------------------------------------------------------------
    
    content_verbs_en = [
        (1, 'be', 'were', 'been'),
        (54, 'become', 'became', 'become'),
        (2, 'begin', 'began', 'begun'),
        (3, 'break', 'broke', 'broken'),
        (4, 'bring', 'brought', 'brought'),
        (55, 'burn', 'burned/burnt', 'burned/burnt'),
        (5, 'buy', 'bought', 'bought'),
        (6, 'build', 'built', 'built'),
        (59, 'can', 'could', 'could'),
        (7, 'choose', 'chose', 'chosen'),
        (8, 'come', 'came', 'come'),
        (9, 'cost', 'cost', 'cost'),
        (10, 'cut', 'cut', 'cut'),
        (11, 'do', 'did', 'done'),
        (12, 'draw', 'drew', 'drawn'),
        (66, 'drink', 'drank', 'drunk'),
        (13, 'drive', 'drove', 'driven'),
        (14, 'eat', 'ate', 'eaten'),
        (60, 'fall', 'fell', 'fallen'),
        (15, 'feel', 'felt', 'felt'),
        (16, 'find', 'found', 'found'),
        (58, 'forget', 'forgot', 'forgotten'),
        (17, 'get', 'got', 'got'),
        (18, 'give', 'gave', 'given'),
        (19, 'go', 'went', 'gone'),
        (20, 'have', 'had', 'had'),
        (21, 'hear', 'heard', 'heard'),
        (22, 'hold', 'held', 'held'),
        (23, 'keep', 'kept', 'kept'),
        (24, 'know', 'knew', 'known'),
        (25, 'leave', 'left', 'left'),
        (26, 'lead', 'led', 'led'),
        (27, 'let', 'let', 'let'),
        (28, 'lie', 'lay', 'lain'),
        (29, 'lose', 'lost', 'lost'),
        (30, 'make', 'made', 'made'),
        (31, 'mean', 'meant', 'meant'),
        (32, 'meet', 'met', 'met'),
        (61, 'must', '-', '-'),
        (33, 'pay', 'paid', 'paid'),
        (34, 'put', 'put', 'put'),
        (57, 'read', 'read', 'read'),
        (35, 'run', 'ran', 'run'),
        (36, 'say', 'said', 'said'),
        (37, 'see', 'saw', 'seen'),
        (38, 'sell', 'sold', 'sold'),
        (39, 'send', 'sent', 'sent'),
        (40, 'set', 'set', 'set'),
        (56, 'shoot', 'shot', 'shot'),
        (41, 'sing', 'sang', 'sung'),
        (42, 'sit', 'sat', 'sat'),
        (43, 'speak', 'spoke', 'spoken'),
        (44, 'spend', 'spent', 'spent'),
        (45, 'stand', 'stood', 'stood'),
        (62, 'steal', 'stole', 'stolen'),
        (63, 'swim', 'swam', 'swum'),
        (46, 'take', 'took', 'taken'),
        (47, 'teach', 'taught', 'taught'),
        (48, 'tell', 'told', 'told'),
        (49, 'think', 'thought', 'thought'),
        (64, 'throw', 'threw', 'thrown'),
        (50, 'understand', 'understood', 'understood'),
        (65, 'wake', 'woke', 'woken'),
        (51, 'wear', 'wore', 'worn'),
        (52, 'win', 'won', 'won'),
        (53, 'write', 'wrote', 'written'),
    ] # last is 65
    
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
    
    #----------------------------------------------------------------
    # TRADUCTIONS
    #----------------------------------------------------------------
    
    content = [
        (1, 1, 100001, None),
        (2, 1, 200001, None),
        (3, 1, 300001, None),
        (6, 9, 100009, None),
        (7, 9, 200009, None),
        (8, 2, 100002, None),
        (9, 3, 100003, None),
        (10, 5, 100005, 'dans les airs'),
        (11, 6, 100006, None),
        (12, 7, 100007, None),
        (13, 8, 100008, None),
        (14, 10, 100010, None),
        (15, 11, 100011, None),
        (16, 12, 100012, None),
        (17, 13, 100013, None),
        (18, 14, 100014, None),
        (19, 15, 100015, None),
        (20, 16, 100016, None),
        (21, 17, 100017, None),
        (22, 26, 100026, None),
        (23, 27, 100027, None),
        (24, 28, 100028, "observer, surveiller, visionner (un film, une émission)"),

        (4, 28, 190028, None),
        (5,  6, 100028, "visionner (un film, une émission)"),

        (25, 29, 100029, None),
        (26, 30, 100030, None),
        (27, 31, 100031, None),
        (28, 32, 100032, None),
        (29, 33, 100033, None),
        (30, 34, 100034, None),
        (31, 35, 100035, None),
        (32, 36, 100036, None),
        (33, 37, 100037, None),
        (34, 38, 100038, None),
        (35, 39, 100039, None),
        (36, 40, 100040, None),
        (37, 41, 100041, 'une odeur'),
        (38, 42, 100042, None),
        (39, 43, 100043, None),
        (40, 44, 100044, None),
        (41, 45, 100045, None),
        (42, 46, 100046, 'amener vers soi un objet'),
        (43, 47, 100047, None),
        (44, 48, 100048, None),
        (45, 49, 100049, None),
        (46, 50, 100050, None),
        (47, 51, 100051, None),
        (48, 52, 100052, None),
        (49, 53, 100053, None),
        (50, 54, 100054, None),
        (51, 55, 100055, None),
        (52, 56, 100056, None),
        (53, 57, 100057, None),
        (54, 58, 100058, None),
        (55, 59, 100059, None),
        (56, 60, 100060, None),
        (57, 61, 100061, None),
        (58, 62, 100062, None),
        (59, 63, 100063, "porter un objet"), # porter => carry
        (60, 64, 100064, None),
        (61, 65, 100065, None),
        (62, 66, 100066, None),
        (63, 67, 100067, None),
        (64, 68, 100068, None),
        (65, 69, 100069, None),
        (66, 70, 100070, None),
        (67, 71, 100071, None),
        (68, 72, 100072, None),
        (69, 73, 100073, None),
        (70, 74, 100074, None),
        (71, 75, 100075, None),
        (72, 76, 100076, None),
        (73, 77, 100077, None),
        (74, 78, 100078, None),
        (75, 79, 100079, None),
        (76, 80, 100080, None),
        (77, 81, 100081, None),
        (78, 82, 100082, None),
        (79, 83, 100083, None),
        (80, 84, 100084, None),
        (81, 85, 100085, None),
        (82, 86, 100086, None),
        (83, 87, 100087, None),
        (84, 88, 100088, None),
        (85, 89, 100089, None),
        (86, 90, 100090, None),
        (87, 91, 100091, None),
        (88, 92, 100092, None),
        (89, 93, 100093, None),
        (90, 94, 100094, None),
        (91, 95, 100095, None),
        (92, 96, 100096, None),
        (93, 97, 100097, None),
        (94, 98, 100098, None),
        (95, 99, 100099, None),
        (96, 100, 100100, None),
        (97, 101, 100101, None),
        (98, 102, 100102, None),
        (99, 103, 100103, None),
        (100, 104, 100104, None),
        (101, 105, 100105, None),
        (102, 106, 100038, None),
        (103, 107, 100107, None),
        (104, 108, 100108, None),
        (105, 109, 100109, None),
        (106, 110, 100110, None),
        (107, 111, 100111, None),
        (108, 112, 100112, None),
        (109, 113, 100113, None),
        (110, 114, 100114, None),
        (111, 115, 100115, None),
        (112, 116, 100116, None),
        (113, 117, 100117, None),
        (114, 118, 100118, None),
        (115, 119, 100119, None),
        (116, 120, 100120, None),
        (117, 121, 100121, None),
        (118, 122, 100122, None),
        (119, 123, 100123, None),
        (120, 124, 100124, None),
        (121, 125, 100125, None),
        (122, 126, 100126, 'quelque part'),
        (123, 127, 100127, None),
        (124, 128, 100128, None),
        (125, 129, 100129, None),
        (126, 130, 100130, None),
        (127, 132, 100132, None),
        (128, 133, 100133, None),
        (129, 134, 100134, None),
        (130, 135, 100135, None),
        (131, 136, 100136, None),
        (132, 41, 190041, 'un sentiment'),
        (133, 5, 190005, 'atteinte à la propriété d''autrui'),
        (134, 137, 100055, None), # CORRECTED
        (135, 46, 190046, 'lancer un projectile'),

        (136, 1, 400001, None),
        (137, 9, 400009, None),
        (139, 2, 400002, None),
        (140, 3, 400003, None),
        (141, 5, 400005, 'dans les airs'),
        (142, 6, 400006, None),
        (143, 7, 400007, None),
        (144, 8, 400008, None),
        (145, 10, 400010, None),
        (146, 11, 400011, None),
        (147, 12, 400012, None),
        (148, 13, 400013, None),
        (149, 14, 400014, None),
        (150, 15, 400015, None),
        (151, 16, 400016, None),
        (152, 17, 400017, None),
        (153, 26, 400026, None),
        (154, 27, 400027, None),
        (155, 28, 400028, None),
        (156, 29, 400029, None),
        (157, 30, 400030, None),
        (158, 31, 400031, None),
        (159, 32, 400032, None),
        (160, 33, 400033, None),
        (161, 34, 400034, None),
        (162, 35, 400035, None),
        (163, 36, 400036, None),
        (164, 37, 400037, None),
        (165, 38, 400038, None),
        (166, 39, 400039, None),
        (167, 40, 400040, None),
        (168, 41, 400041, 'une odeur'),
        (169, 42, 400042, None),
        (170, 43, 400043, None),
        (171, 44, 400044, None),
        (172, 45, 400045, None),
        (173, 46, 400046, 'amener vers soi un objet'),
        (174, 47, 400047, None),
        (175, 48, 400048, None),
        (176, 49, 400049, None),
        (177, 50, 400050, None),
        (178, 51, 400051, None),
        (179, 52, 400052, None),
        (180, 53, 400053, None),
        (181, 54, 400054, None),
        (182, 55, 400055, None),
        (183, 56, 400056, None),
        (184, 57, 400057, None),
        (185, 58, 400058, None),
        (186, 59, 400059, None),
        (187, 60, 400060, None),
        (188, 61, 400061, None),
        (189, 62, 400062, None),
        (190, 63, 400063, None),
        (191, 64, 400064, None),
        (192, 65, 400065, None),
        (193, 66, 400066, None),
        (194, 67, 400067, None),
        (195, 68, 400068, None),
        (196, 69, 400069, None),
        (197, 70, 400070, None),
        (198, 71, 400071, None),
        (199, 72, 400072, None),
        (200, 73, 400073, None),
        (201, 74, 400074, None),
        (202, 75, 400075, None),
        (203, 76, 400076, None),
        (204, 77, 400077, None),
        (205, 78, 400078, None),
        (206, 79, 400079, None),
        (207, 80, 400080, None),
        (208, 81, 400081, None),
        (209, 82, 400082, None),
        (210, 83, 400083, None),
        (211, 84, 400084, None),
        (212, 85, 400085, None),
        (213, 86, 400086, None),
        (214, 87, 400087, None),
        (215, 88, 400088, None),
        (216, 89, 400089, None),
        (217, 90, 400090, None),
        (218, 91, 400091, None),
        (219, 92, 400092, None),
        (220, 93, 400093, None),
        (221, 94, 400094, None),
        (222, 95, 400095, None),
        (223, 96, 400096, None),
        (224, 97, 400097, None),
        (225, 98, 400098, None),
        (226, 99, 400099, None),
        (227, 100, 400100, None),
        (228, 101, 400101, None),
        (229, 102, 400102, None),
        (230, 103, 400103, None),
        (231, 104, 400104, None),
        (232, 105, 400105, None),
        (233, 106, 400038, None),
        (234, 107, 400107, None),
        (235, 108, 400108, None),
        (236, 109, 400109, None),
        (237, 110, 400110, None),
        (238, 111, 400111, None),
        (239, 112, 400112, None),
        (240, 113, 400113, None),
        (241, 114, 400114, None),
        (242, 115, 400115, None),
        (243, 116, 400116, None),
        (244, 117, 400117, None),
        (245, 118, 400118, None),
        (246, 119, 400119, None),
        (247, 120, 400120, None),
        (248, 121, 400121, None),
        (249, 122, 400122, None),
        (250, 123, 400123, None),
        (251, 124, 400124, None),
        (252, 125, 400125, None),
        (253, 126, 400126, 'quelque part'),
        (254, 127, 400127, None),
        (255, 128, 400128, None),
        (256, 129, 400129, None),
        (257, 130, 400130, None),
        (258, 132, 400132, None),
        (259, 133, 400133, None),
        (260, 134, 400134, None),
        (261, 135, 400135, None),
        (262, 136, 400136, None),
        (265, 137, 400137, None),
        (267, 46, 490046, 'lancer un projectile'),
        (268, 5, 490005, 'atteinte à la propriété d''autrui'),
        (269, 41, 490041, 'un sentiment'),

        (270, 134, 200134, None),
        (271, 124, 200124, None),
        (272, 86, 200086, None),
        (273, 55, 200055, None),
        (274, 66, 200066, None),
        (275, 2, 200002, None),
        (276, 3, 200003, None),
        (277, 5, 200005, 'dans les airs'),
        (278, 5, 290005, 'dérober'),
        (279, 6, 200006, None),
        (280, 7, 200007, None),
        (281, 8, 200008, None),
        (282, 10, 200010, None),
        (283, 11, 200011, None),
        (284, 12, 200012, None),
        (285, 13, 200013, None),
        (286, 14, 200014, 'd''une langue à une autre'),
        (287, 15, 200015, None),
        (288, 16, 200016, 'physiquement et émotionnellement'),
        (289, 17, 200017, None),
        (290, 26, 200026, None),
        (291, 27, 200027, None),
        (292, 28, 200028, None),
        (293, 29, 200029, None),
        (294, 30, 200030, None),
        (295, 31, 200031, None),
        (296, 32, 200032, None),
        (297, 33, 200033, None),
        (298, 34, 200034, None),
        (299, 35, 200035, None),
        (300, 36, 200036, None),
        (301, 37, 200037, None),
        (302, 38, 200038, None),
        (303, 39, 200039, None),
        (304, 40, 200040, None),
        (305, 41, 200041, 'une odeur ou un sentiment'),
        (306, 42, 200042, None),
        (307, 43, 200043, None),
        (308, 44, 200044, None),
        (309, 45, 200045, None),
        (310, 46, 200046, None),
        (311, 47, 200047, None),
        (312, 48, 200048, None),
        (313, 49, 200049, None),
        (314, 50, 200050, None),
        (315, 51, 200051, None),
        (316, 52, 200052, None),
        (317, 53, 200053, None),
        (318, 54, 200054, None),
        (319, 56, 200056, None),
        (320, 57, 200057, None),
        (321, 58, 200058, None),
        (322, 59, 200059, None),
        (323, 60, 200060, None),
        (324, 61, 200061, None),
        (325, 62, 200062, None),
        (326, 63, 200063, None),
        (327, 64, 200064, None),
        (328, 65, 200065, None),
        # BUG DOUBLE to present fr/it ! (329, 66, 20066, None), (274, 66, 20066, None),
        (330, 67, 200067, None),
        (331, 68, 200068, None),
        (332, 69, 200069, None),
        (333, 70, 200070, None),
        (334, 71, 200071, None),
        (335, 72, 200072, None),
        (336, 73, 200073, None),
        (337, 74, 200074, None),
        (338, 75, 200075, 'à un jeu, un sport'),
        (339, 75, 290075, 'une pièce au théâtre'),
        (340, 75, 280075, 'd''un instrument'),
        (341, 76, 200076, None),
        (342, 77, 200077, None),
        (343, 78, 200078, None),
        (344, 79, 200079, None),
        (345, 80, 200080, None),
        (346, 81, 200081, None),
        (347, 82, 200082, None),
        (348, 83, 200083, None),
        (349, 84, 200084, None),
        (350, 85, 200085, None),
        (351, 87, 200087, None),
        (352, 88, 200088, None),
        (353, 89, 200089, None),
        (354, 90, 200041, None),
        (355, 91, 200091, None),
        (356, 92, 200092, None),
        (357, 93, 200093, None),
        (358, 94, 200094, None),
        (359, 95, 200095, None),
        (360, 96, 200096, None),
        (361, 97, 200097, None),
        (362, 98, 200098, None),
        (363, 99, 200099, None),
        (364, 100, 200100, None),
        (365, 101, 200101, None),
        (366, 102, 200102, None),
        (367, 103, 200103, None),
        (368, 104, 200104, None),
        (369, 105, 200105, None),
        (370, 106, 200106, None),
        (371, 107, 200107, None),
        (372, 108, 200108, None),
        (373, 109, 200109, None),
        (374, 110, 200110, None),
        (375, 111, 200111, None),
        (376, 112, 200112, None),
        (377, 113, 200113, None),
        (378, 114, 200114, None),
        (379, 115, 200115, None),
        (380, 116, 200116, None),
        (381, 117, 200117, None),
        (382, 118, 200118, None),
        (383, 119, 200119, None),
        (384, 120, 200120, None),
        (385, 121, 200121, None),
        (386, 122, 200122, None),
        (387, 123, 200123, None),
        (388, 125, 200125, None),
        (389, 126, 200126, 'quelque part'),
        (390, 127, 200127, None),
        (391, 128, 200128, None),
        (392, 129, 200129, None),
        (393, 130, 200130, None),
        (394, 132, 200132, None),
        (395, 133, 200133, None),
        (396, 135, 200135, None),
        (397, 136, 200136, None),
        (398, 137, 200137, None),

        (399, 138, 400138, None),
        (400, 139, 400139, None),
        (401, 138, 100138, 'vu de l''intérieur du lieu que l''on quitte'),
        (402, 138, 190138, 'vu de l''extérieur du lieu que l''on quitte'),
        (403, 138, 180138, 'sortir quelque chose'),
        (404, 139, 100139, 'vu de l''extérieur du lieu où l''on entre'),
        (405, 139, 190139, 'vu de l''intérieur du lieu où l''on entre'),
        (406, 139, 180139, 'de façon générale'),
        (407, 138, 200138, None),
        (408, 139, 200139, None),
        (409, 86, 290086, 'l''autre'),
        (410, 140, 100140, None),
        (411, 141, 100141, None),
        (412, 140, 200140, None),
        (413, 141, 200141, None),
        (414, 140, 400140, None),
        (415, 141, 400141, None),
        (416, 142, 100142, None),
        (417, 142, 400142, None),
        (418, 142, 200142, None),
        (422, 143, 100143, None),
        (423, 143, 200143, None),
        (424, 143, 400143, None),
        (425, 144, 100047, None), # CORRECTED
        (426, 144, 200144, None),
        (427, 144, 400047, None), # CORRECTED
        (428, 145, 100145, None),
        (429, 145, 200145, None),
        (430, 145, 400145, None),
        (431, 146, 100146, None),
        (432, 146, 200146, None),
        (433, 146, 400146, None),
        (434, 147, 100147, 'vu du lieu plus bas'),
        (435, 147, 190147, 'vu du lieu plus haut'),
        (436, 147, 400147, None),
        (437, 147, 200147, None),
        (438, 148, 100148, 'vu du lieu plus haut'),
        (439, 148, 190148, 'vu du lieu plus bas'),
        (440, 148, 200148, None),
        (441, 148, 400148, None),
        (445, 150, 100150, None),
        (446, 150, 200150, None),
        (447, 150, 400150, None),
        (448, 151, 100151, None),
        (449, 151, 200151, None),
        (450, 151, 400151, None),

        # VAGUE 2
        (451, 126, 190126, "une occurrence"),
        (452, 152, 100152, None),
        (453, 153, 100153, None),
        (454, 154, 100154, None),
        (455, 155, 100155, None),
        (456, 156, 100156, "attraper du gibier"),
        (457, 156, 190156, "expulser"),
        (458, 158, 100105, None),
        (459, 159, 100159, None),
        (460, 160, 100003, "vouloir"),
        (461, 160, 100043, "souhaiter"),
        (462, 160, 100160, "convoiter (y compris sexuellement)"),
        (463, 161, 100161, None),
        (464, 162, 100162, None),
        (465, 163, 100163, None),
        (466, 73, 190073, "(se dit également du soleil)"),
        (467, 84, 190084, "fabriquer"),
        (468, 164, 100164, None),
        (469, 165, 100165, None),
        (470, 166, 100166, None),
        (471, 167, 100167, None),
        (472, 168, 100168, "déraper"),
        (473, 168, 190168, "se mouvoir de façon fluide"),
        (474, 169, 100169, None),
        (475, 169, 190169, "concerner"),
        (476,  28, 190169, "concerner"),
        (477, 170, 100170, "lever"),
        (478, 170, 190170, "soulever"),
        (479, 171, 100171, None),
        (480, 171, 190171, None),
        (481, 171, 180171, None),
        (482, 172, 100172, None),
        (483, 173, 100173, None),
        (484, 174, 100174, None),
        (485, 175, 100175, None),
        (486, 176, 100176, "immerger (dans l'eau), descendre (dans l'air)"),
        (487, 177, 100177, None),
        (488, 178, 100178, None),
        (489, 179, 100179, None),
        (490, 180, 100058, None),
        (491, 181, 100045, None),
        (492, 182, 100182, None),
        (493, 183, 100183, None),
        (494, 184, 100184, None),
        (495, 185, 100185, None),
        (496, 186, 100076, None),
        (597, 187, 100187, None),
        #(666, 187, 99999, None) # ERREUR VOLONTAIRE "VERS" DE TEST
        #(666, 19999, 187, None) # ERREUR VOLONTAIRE "DE" DE TEST
    
        # VAGUE 3
        (598, 188, 100188, None),
        (599, 189, 100189, None),
        (600, 190, 100190, None),
        (601, 191, 100191, None),
        (602, 192, 100192, None),
        (603, 193, 100193, None),
        (604, 194, 100194, None),
        (605, 195, 100195, None),
        (606, 63, 190063, "porter un vêtement"),
        (607, 196, 100196, None), # être debout => stand
        (608, 100196, 86, None), # stand => être, on ne le met que dans ce sens
        (609, 197, 100197, None), # être assis => sit
        (610, 150, 100197, None), # s'assoir => sit
        (611, 100197, 86, None), # sit => être
        (612, 100199, 124, None), # get => avoir
        (613, 100199, 27, None), # get => recevoir
        (614, 100199, 109, None), # get => comprendre
        (615, 100200, 102, None), # set => créer
        (616, 100200, 47, None), # set => mettre
        (617, 100200, 144, None), # set => poser
        ]
        
    check_content_trans(content, verbes_id)
    
    # Adding reverse translation only for en -> fr
    id = 700
    added = []
    for cc in content:
        id += 1
        de = cc[1]
        vers = cc[2]
        comment = cc[3]
        if vers >= 100000:
            added.append((id, cc[2], cc[1], cc[3]))
    for aa in added:
        content.append(aa)
    
    c.executemany('INSERT INTO voc_translate VALUES (?,?,?,?)', content)

    conn.commit()

    conn.close()

    # ---

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    #c.execute("SELECT * FROM voc_verbs")
    #r = c.fetchone()
    f = open('results.txt', 'w', encoding='utf-8')

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


def get_all_verbs_full(): # all verbs, with translations and irregular forms
    p_conn = sqlite3.connect('example.db')
    p_cursor = p_conn.cursor()
    p_lang = 'en'
    p_to = 'fr'
    p_order = p_lang + '.base'
    nb = 0
    p_string = ("SELECT " + p_lang + ".id, " + p_lang + ".base, " + p_lang + ".surtype, " + p_lang + ".lvl, " + p_to + ".base, " + p_to + ".id, t.sens, t.id " +
                "FROM voc_verbs as " +
                p_lang + ", voc_verbs as " + p_to + ", voc_translate as t WHERE " + p_lang + ".id = t.de AND " +
                p_to + ".id = t.vers AND " + p_lang + ".lang = '" + p_lang + "' AND " + p_to + ".lang = '" + p_to + "' AND " + p_lang + ".surtype = 'verb'" +
                " ORDER BY " + p_order)
    verbs = []
    actual = None
    irregulars = get_all_verbs_en()
    #print(p_string)
    for p_row in p_cursor.execute(p_string):
        if actual is None or actual['id'] != p_row[0]:
            if actual is None:
                #print('debut')
                actual = {}
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
                        if actual['root_base'][-2] in ['a', 'u']:
                            if actual['root_base'][-3] in ['a', 'e', 'o', 'u']:     # base (cook => cooked)
                                actual['part'] = actual['root_base'] + 'ed'
                            else:                                                   # chat => chatted
                                actual['part'] = actual['root_base'] + actual['root_base'][-1] + 'ed'
                        else:
                            actual['part'] = actual['root_base'] + 'ed'             # base
                    else:
                        actual['part'] = actual['root_base'] + 'ed'                 # base
                    
                    actual['pret'] = actual['part']
                verbs.append(actual)
                actual = {}
            #print('verbe : ' + p_row[1])
            actual['id'] = p_row[0]
            actual['base'] = p_row[1]
            actual['surtype'] = p_row[2]
            actual['lvl'] = p_row[3]
            actual['trans'] = {}
            actual['trans'][p_row[4]] = p_row[6]
            #print('\ttranslated to : ' + p_row[4])
        elif actual is not None:
            actual['trans'][p_row[4]] = p_row[6]
            #print('\ttranslated to : ' + p_row[4])
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

def rappel_en():
    f = open('output.html', 'w')
    f.write("""
<html>
    <head>
        <style type="text/css">
            body : {
                font-family: Verdana;
            }
            h1 {
                color: #cc1479; /*#CC6714;*/
            }
            h2 {
                color: #14cc67;
                font-family: "Palatino Linotype";
                font-size: 22px;
                border-bottom: 1px solid #14cc67;
            }
            h3 {
                color: #6714cc;
                font-family: "Palatino Linotype";
                font-size: 18px;
            }
            
            tr:nth-child(odd) {
                background: #DDDDDD;
            }
            
            th {
                background: #FFFFFF;
                border-bottom: 1px black solid;
            }
            

            b {
                font-family: verdana;
            }
            
            b.present {
                color: white;
                background: #4198e1;
            }
            
            b.past {
                color: white;
                background: #e4575d;
            }
            
            b.future {
                color: white;
                background: #419f3c;
            }
            
            b.ing {
                color: white;
                background: #f4a014;
            }
            
            b.s {
                color: red;
                background: #4198e1;
            }
            b.pp {
                color: white;
                background : #9a3c9f;
            }
            
            div.simple {
                border-left: 2px solid lightgrey;
                padding-left: 5px;
            }
            
            div.pp {
                border-left: 2px solid #9a3c9f;
                padding-left: 5px;
            }
            
            div.ing {
                border-left: 2px solid #f4a014;
                padding-left: 5px;
            }
            
            div.title_page {
                width: 100%;
                text-align:center;
                border: 1px solid #cc1479;
                padding: 10px;
            }
            
        </style>
    </head>
    <body>
        <!-- Title Page -->
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <div class="title_page">
            <h1>200 verbes anglais fondamentaux</h1>
            <h3>Damien Gouteux</h3>
        </div>
        <mbp:pagebreak />
        
        <!-- Copyright Page -->
        <p>© Damien Gouteux 2015</p>
        <p>Tous droits de traduction, de reproduction et d'adaptation, totales ou partielles, réservés pour tous pays.</p>
        <mbp:pagebreak />

        <!-- Dedication -->
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <p>Aux anglais et à leur langue.</p>
        <mbp:pagebreak />
        
        <!-- Preface -->
        <!-- Prologue -->
        
        <h1>Sommaire</h1>
        <h2>Considérations sur les verbes anglais</h2>
            <h3>1. De la modeste portée de cet ouvrage</h3>
            <h3>2. Légende : choix1/choix2 (négatif) pers. sing.</h3>
            <h3>3. Les formes contractées de la négation</h3>
            <h3>4. Les valeurs des modes et des temps</h3>
            <h3>5. Règles systématiques de production des temps</h3>
        <h2>Liste des 200 verbes</h2>
    """)
    #    <table><thead><tr><th>N°</th><th>Verbe</th><th>Page</th></thead><tbody>
    #""")
    verbs = get_all_verbs_full()
    nb = 0
    for v in verbs:
        nb += 1
        pages = 100 + nb
        #f.write('\t<tr><td>' + str(nb) + '</td><td>' + v['base'] + '</td><td>' + str(pages) + '</td></tr>')
        f.write('<h3>' + str(pages) + '. ' + v['root_base'] + v['particle'] + ' &nbsp;(' + v['pret'] + v['particle'] + ', ' + v['part'] + v['particle'] + ')')
        if v['irregular']:
            f.write(' *')
        f.write('</h3>')
    f.write('\n\n')
    f.write('<p>Les verbes avec une * sont irréguliers.</p>')
    f.write('<mbp:pagebreak />')
    
    f.write("""
        <h2>1. De la modeste portée de cet ouvrage</h2>
        <p>Cette ouvrage entend proposer 200 verbes fondamentaux à la pratique de la langue anglaise. On y retrouvera pour chacun ses différentes traductions et formes dans un format concis et clair.</p>
        
        <p>La langue anglaise est <i>de facto</i> la langue auxiliaire internationale actuelle. Dans les aéroports et de nombreux endroits, elle fait office de langue secondaire pour comprendre l'essentiel. De part la puissance des économies anglophones, elle est aussi en usage dans de nombreux secteurs clés comme celui de la recherche scientifique. Pour toutes ces raisons, comprendre et savoir utiliser un minimum cette langue nous semble un élément essentiel du citoyen d'aujourd'hui. Cela ne doit pas se faire au détriment de sa (ses) langue(s) maternelle(s), mais en complément, comme le mot <i>auxiliaire</i> le laisse entendre. Néanmoins nous tenons à attirer l'attention de nos lecteurs sur des tentatives effectuées par de nombreux individus de doter l'Humanité, ou une grande partie de celle-ci, d'une langue auxiliaire <i>construite</i> ou <i>artificielle</i> comme l'<i>Esperanto</i>, l'<i>Ido</i> ou l'<i>Interlingua</i>, et toutes les autres. Ces langues poursuivent le but d'être <i>simple</i>, mais elles se heurtent à de nombreux obstacles : la définition même de cette <i>simplicité</i> rêvée - ce qui est simple pour un Chinois ne l'étant pas forcément pour un Français, le désintérêt du plus grande nombre pour la question, les obstacles posés par certains pays, institutions et personnes - dont la France et Staline, et la satisfaction générale pour la situation actuelle, ou du moins son acceptation fataliste. L'auteur ne peut que faire remarquer qu'avec un vocabulaire issu très fortement du français, peut-être moins dans le cas des verbes les plus utilisés, dont les origines sont plutôt germaniques, un Français peut fort aisément tirer partie de la domination de la langue anglaise, pour peu qu'il arrive à se faire à sa prononciation, tout en finesse.</p>
        
        <p>Comme il s'agit de la première édition, malgré nos soins aimants portés à ce livre, il est fort probable qu'il ne soit pas dénué de quelques erreurs fâcheuses. Nous demandons à nos aimables lecteurs de nous pardonner nos offenses à la langue et espérons qu'il y en aura le moins possible. Nous souhaitons avant tout que ce livre vous soit <i>utile</i>, que cela soit pour réviser ou apprendre ces fameux verbes. Bon apprentissage !</p>
        
        <h2>2. Légende : choix1/choix2 (négatif) pers. sing.</h2>
        <h2>3. Les formes contractées de la négation</h2>
        <h2>4. Les valeurs des modes et des temps</h2>
        <h2>5. Règles systématiques de production des temps</h2>
        <p>Modestie la portée de cet ouvrage</p>
        <p>Légende : choix1/choix2 (négatif) pers. sing. </p>
        <p>Les formes contractées de la négation</p>
            <table>
            <thead>
                <tr><th>Forme simple</th><th>Forme contractée</th></tr>
            </thead>
            <tbody>
                <tr><td>do not</td><td>don't</td></tr>
                <tr><td>does not</td><td>doesn't</td></tr>
            </tbody>
            </table>
        <p>Les valeurs des modes et des temps
            <ul>
                <li><i>(L'iréel, la généralité)</i></li>
                <li><i>(Le réel sous conditions)</i></li>
                <li><i>(L\'irréel)</i></li>
                <li><i>(L\'ordre)</i></li>
            </ul>
        </p>
    """)
    f.close()


def conjugate_en(verb, onfile=False, html=False, info=None, nb=None):
    if not onfile or not html or nb is None or info is None:
        print("i This function works only with onfile and html set at true")
        return

    f = open('output.html', 'a')
    pronoms = ['I', 'you', 'she, he, it', 'we', 'you', 'they']
    root = info['root_base']
    particle = info['particle']
    pret = info['pret']
    part = info['part']
    
    # Present 3e
    if root[-1] == 'y' and root[-2] in ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']:
        pres3 = root[0:-1] + "ies"
    elif root[-1] in ['s', 'x', 'z', 'o'] or root[-2:] in ['ch', 'sh']:
        pres3 = root + '<b class="s">es</b>'
    else:
        pres3 = root + '<b class="s">s</b>'

    # ing
    if root[-1] == 'e':
        ing = root[0:-1] + 'ing'
    elif root[-1] in ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z'] and root[-2] in ['a','e','i','o','u']:
        if root[-2] == 'a' and root[-3] == 'e':
            ing = root + 'ing'
        elif root[-2] == 'o' and root[-3] == 'o':
            ing = root + 'ing'
        else:
            ing = root + root[-1] + 'ing'
    else:
        ing = root + 'ing'
    
    f.write('<h2>' + str(nb) + '. ' + root + particle + ' &nbsp;&nbsp;(' + pret + particle + ', ' + part + particle + ')</h2>\n')
    f.write('<p><b>Sens et traduction</b> : <ul>\n')
    for t in info['trans']:
        if info['trans'][t] is not None:
            f.write('\t<li>' + t + ' : ' + info['trans'][t] + '</li>\n')
        else:
            f.write('\t<li>' + t + '</li>\n')
    f.write('</ul></p>\n')
    
    #f.write('<p><b>Base verbale</b> : ' + root + '</p>\n')
    f.write('<p><b>Infinitif</b> : <b>to ' + root + '</b></p>\n')
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
    f.write('<p><b>Futur simple</b> : <b class="future">will</b> (not) <b class="future">' + root + particle + '</b></p>\n')
    f.write('</div>\n')
    
    f.write('<div class="pp">\n')
    f.write('<p><b>Présent parfait</b> : <b class="present">have</b> (not) <b class="pp">' + part + particle + '</b> (3e pers. sing. : <b class="present">' + 'ha</b><b class="s">s</b> (not) <b class="pp">' + part + particle + '</b>)</p>\n')
    f.write('<p><b>Passé parfait</b> : <b class="past">had</b> (not) <b class="pp">' + part + particle + '</b></p>\n')
    f.write('<p><b>Futur parfait</b> : <b class="future">will</b> (not) <b class="future">have</b> <b class="pp">' + part + particle + '</b></p>\n')
    f.write('</div>\n')
    
    f.write('<div class="ing">\n')
    f.write('<p><b>Présent continu</b> : <b class="present">are</b> (not) <b class="ing">' + ing + particle +  '</b> (1ère et 3e pers. sing. : <b class="present">is</b> (not) <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('<p><b>Passé continu</b> : <b class="past">were</b> (not) <b class="ing">' + ing + particle +  '</b> (1ère et 3e pers. sing. : <b class="past">was</b> (not) <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('<p><b>Futur continu</b> : <b class="future">will be</b> (not) <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('</div>\n')
    
    f.write('<div class="pp">\n')
    f.write('<div class="ing">\n')
    f.write('<p><b>Présent parfait continu</b> : <b class="present">have</b> (not) <b class="pp">been</b> <b class="ing">' + ing + particle + '</b> (3e pers. sing. : <b class="present">' + 'ha</b><b class="s">s</b> (not) <b class="pp">been</b> <b class="ing">' + ing + particle + '</b>)</p>\n')
    f.write('<p><b>Passé parfait continu</b> : <b class="past">had</b> (not) <b class="pp">been</b> <b class="ing">' + ing + particle + '</b></p>\n')
    f.write('<p><b>Futur parfait continu</b> : <b class="future">will</b> (not) <b class="future">have</b> <b class="pp">been</b> <b class="ing">' + part + particle + '</b></p>\n')
    f.write('</div>\n')
    f.write('</div>\n')
    
    f.write('<h3>Conditionnel</h3>\n')
    f.write('<p><b>Présent</b> : should/would (not) ' + root + particle + '</p>\n')
    f.write('<p><b>Passé</b> : should/would (not) have ' + part + particle + '</p>\n')
    
    f.write('<h3>Subjonctif</h3>\n')
    f.write('<p>Expression d\'une <b>potentialité</b> : may/might (not) ' + root + particle + '</p>\n')
    f.write('<p>Expression d\'un <b>doute</b>, d\'une <b>supposition</b> ou <b>atténuation polie</b> : should (not) ' + root + particle + '</p>\n')
    
    f.write('<h3>Impératif</h3>\n')
    f.write('<p><b>2e pers.</b> : (do not) ' + root + particle + '!</p>\n')
    f.write('<p><b>Autres pers.</b> :<ul>\n')
    f.write('\t<li><b>forme affirmative</b> : let me/her/him/it/us/them ' + root + particle + '!</li>\n')
    f.write('\t<li><b>formes négatives</b> :<ul>\n')
    f.write('\t\t<li>do not/don\'t let me/her/him/it/us/them ' + root + particle + '!</li>\n')
    f.write('\t\t<li>let me/her/him/it/us/them not ' + root + particle + '!</li>\n')
    f.write('</ul></li></ul></p>\n')
    f.write('<mbp:pagebreak />')
    
    f.close()
    
def conjugate_en2(verb, onfile=False, html=False):
    if not onfile or not html:
        print("i This function works only with onfile and html set at true")
        return
    
    f = open('output.html', 'a')
    
    pronoms = ['I', 'you', 'she, he, it', 'we', 'you', 'they']
    root = verb
    
    f.write('<h3>Sens</h3>\n\n')
    
    f.write('<h3>Infinitif</h3>\n\n')
    
    f.write('<table>\n')
    f.write('\t<thead>\n\t\t<tr><th>Infinitive</th></tr>\n\t</thead>\n\t<tbody>\n')
    f.write('\t\t<tr><td>to ' + root + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n')
    
    f.write('<h3>Formes simples de l\'indicatif</h3>\n\n<table>\n')
    
    # present
    suffix = ['', '', 's', '', '', '']
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Present</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, term in enumerate(suffix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + root + term + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # preterit
    suffix = ['ed', 'ed', 'ed', 'ed', 'ed', 'ed']
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Past</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, term in enumerate(suffix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + root + term + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # futur
    prefix = ['will', 'will', 'will', 'will', 'will', 'will']
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Future</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # present perfect
    prefix = ['have', 'have', 'has', 'have', 'have', 'have']
    suffix = 'ed'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Present perfect</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # Past perfect
    prefix = ['had', 'had', 'had', 'had', 'had', 'had']
    suffix = 'ed'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Past perfect</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # Future perfect
    prefix = ['will have', 'will have', 'will have', 'will have', 'will have', 'will have']
    suffix = 'ed'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Future perfect</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n')
    
    f.write('<h3>Aspect progressif de l\'indicatif</h3>\n\n<table>\n')
    
    # present +ing
    prefix = ['am', 'are', 'is', 'are', 'are', 'are']
    suffix = 'ing'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Present</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # preterit +ing
    prefix = ['was', 'were', 'was', 'were', 'were', 'were']
    suffix = 'ing'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Past</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # futur +ing
    prefix = ['will be', 'will be', 'will be', 'will be', 'will be', 'will be']
    suffix = 'ing'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Future</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # present perfect +ing
    prefix = ['have been', 'have been', 'has been', 'have been', 'have been', 'have been']
    suffix = 'ing'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Present perfect</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # Past perfect +ing
    prefix = ['had been', 'had been', 'had been', 'had been', 'had been', 'had been']
    suffix = 'ing'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Past perfect</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n<table>\n')
    # Future perfect +ing
    prefix = ['will have been', 'will have been', 'will have been', 'will have been', 'will have been', 'will have been']
    suffix = 'ing'
    f.write('\t<thead>\n\t\t<tr><th colspan="2">Future perfect</th></tr>\n\t</thead>\n\t<tbody>\n')
    for i, pre in enumerate(prefix):
        f.write('\t\t<tr><td>' + pronoms[i] + '</td><td>' + pre + ' ' + root + suffix + '</td></tr>\n')
    f.write('\t</tbody>\n</table>\n\n')
    
    f.write('<h3>Conditionnel</h3>\n\n')
    
    f.write('<h3>Impératif</h3>\n\n')
    
    f.write('<h3>Subjonctif</h3>\n\n')
    
    f.close()
    
def conjugate_fr(verb, onfile=False, html=False):
    if onfile:
        f = open('output.html', 'a')
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
    
# Mainloop

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
            print("  Parameter settings:")
            print("    order ... - set the order of the returned results")
            print("    lang ... - set the lang of the returned results (for select and trans)")
            print("    lang - get the current lang of the returned results and translation")
            print("    to ... - set the translation of the returned results (for trans)")
            print("    auto - switch to wait for a key or not before executing the command")
            print("    file - switch to conjugate a verb in a file instead of displaying it")
            print("    html - switch to output in html in the file instead of plain text")
            print("    reset - reset the file where the conjugated verbs are stored")
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
            rappel_en()
            print('i file output.html reset')
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

Console(['create', 'reset', 'html', 'lang en', 'con all', 'exit']) #'con talk', 'con accept', 'exit'])
