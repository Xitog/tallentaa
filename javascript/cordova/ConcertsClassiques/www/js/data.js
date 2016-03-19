//-----------------------------------------------------------------------------
// Data needed by the application covering :
// ONCT 2015-2016 season
//-----------------------------------------------------------------------------
        
var works = { 
    'Gustav Holst' : {
        '32' : 'The Planets op.32',
    },
    'Maurice Ravel' : {
        'M.61' : 'Valses nobles et sentimentales',
        'MereOye' : 'Ma Mère l’Oye, Suite pour orchestre',
        'ConcertoPianoSolMajeur' : 'Concerto pour piano et orchestre en sol majeur',
        'La Valse' : 'La Valse',
        'DaphnisChloéSuite2' : 'Daphnis et Chloé, Suite d’orchestre n°2',
        'Boléro' : 'Boléro pour orchestre',
    },
    'John Adams' : {
        'ConViolon1993' : 'Concerto pour violon et orchestre',
    },
    'Ludwig van Beethoven' : {
        '37' : 'Concerto pour piano et orchestre n°3 en ut mineur, op. 37',
        '55' : 'Symphonie n°3 « Héroïque » en mi bémol majeur op. 55',
        '58' : 'Concerto pour piano et orchestre n° 4 en sol majeur, op. 58',
        '61' : 'Concerto pour violon et orchestre en ré majeur op. 61',
        '68' : 'Symphonie n°6 « Pastorale » en fa majeur, op. 68',   
        '72B': 'Léonore III, Ouverture en do majeur, op. 72 B',
        'Egmont Ouverture' : 'Egmont Ouverture',
    },
    'Bohuslav Martinů' : {
        'MemorialLidice' : 'Mémorial pour Lidice',
    },
    'Karl Amadeus Hartmann' : {
        'ConcertoFunebre' : 'Concerto funèbre pour violon et orchestre à cordes',
    },
    'Richard Strauss' : {
        '64' : 'Symphonie Alpestre op. 64',
    },
    'Max Bruch' : {
        '84' : 'Konzertstück pour violon solo et orchestre en fa dièse mineur op. 84',
    },
    'Gustav Mahler' : {
        'S5' : 'Symphonie n° 5 en do dièse mineur',
        'Symph6' : 'Symphonie n°6 « Tragique »',
    },
    'Benjamin Attahir' : {
        'NBruch' : 'Nach(t)spiel, pour violon et orchestre - final additionnel au Konzertstück, op. 84 de Max Bruch', // Création mondiale
    },
    'Béla Bartók' : {
        'op. 13, Sz. 60' : 'Le Prince de bois, poème chorégraphique op. 13',
        'cordes_percu_celesta' : 'Musique pour cordes, percussions et célesta',
    },
    'David Azagra' : {
        'Prelude' : 'Prélude, création mondiale',
    },
    'Piotr Ilitch Tchaïkovski' : {
        'romeojuliette' : 'Roméo et Juliette, ouverture fantaisie',
        '17' : 'Symphonie n°2 « Petite Russie », en ut mineur, opus 17',
        '33' : 'Variations sur un thème rococo pour violoncelle et orchestre op. 33',
        '55' : 'Suite n°3 en sol majeur, opus 55',
        '74' : 'Symphonie n°6 « Pathétique », en si mineur, opus 74',
        'extraitsBelle04022016' : 'La Belle au bois dormant : Acte 2, scène 1 n°18 : Entr\'acte',
        'extraitsLac04022016' : 'Le Lac des Cygnes : Acte 1 n°5: Pas de deux "le cygne noir" et Acte 3: Danse Russe',
        'BABD:Valse6' : 'La Belle au Bois Dormant : Valse n°6',
        'SW:Spe1' : 'Le Lac des Cygnes : Danse Espagnole, Danse Hongroise Czardas',
        'CN:Spe1' : 'Casse-Noisette : Danse des Mirlitons, Valse des Fleurs et Pas de deux',
    },
    'Sergei Vasilievich Rachmaninoff' : {
        '45' : 'Danses symphoniques op. 45',
    },
    'Damien Lehman' : {
        'alibaba' : 'Ali Baba et les Quarante Voleurs',
    },
    'Marc-André Dalbavie' : {
        'color' : 'Color',
    },
    'Fazil Say' : {
        'water' : 'Water pour piano et orchestre',
    },
    'Dmitri Dmitrievitch Chostakovitch' : {
        '10' : 'Symphonie n°1 en fa mineur op. 10',
        'Jazz2' : 'Suite de Jazz n°2 : Valse II (Sérénade / Valse) et Little polka n°4',
        'TahitiTrot' : 'Tahiti-Trot',
        '93' : 'Symphonie n°10 en mi mineur, op. 93',
    },
    'Leonard Bernstein' : {
        'candide' : 'Candide, Ouverture',
        'wss_danses' : 'Danses symphoniques de West Side Story',
    },
    'George Gershwin' : {
        'americain_a_paris' : 'Un Américain à Paris, pour orchestre',
        '3songs' : 'Three songs (Arr. D. Powers)',
    },
    'Hector Berlioz' : {
        '17' : 'Roméo et Juliette, symphonie dramatique op. 17',
        'symph_fantastique' : 'Symphonie "Fantastique"',
    },
    'Olivier Messiaen' : {
        'offrandes' : 'Les Offrandes oubliées, méditation symphonique',
    },
    'Henri Dutilleux' : {
        'toutunmondelointain' : 'Tout un Monde lointain, Concerto pour violoncelle et orchestre',
    },
    'Claude Debussy' : {
        'lamer' : 'La Mer, trois esquisses symphoniques',
        'Rhapsodie n°1 pour clarinette' : 'Rhapsodie n°1 pour clarinette',
    },
    'Igor Fyodorovich Stravinsky' : {
        'oiseausuite2' : 'L’Oiseau de feu, Suite pour orchestre n° 2',
        'oiseausuiteX' : 'Suite pour orchestre de l\'Oiseau de feu', // Ils ne précisent pas sur quelle suite Béjart a fait son ballet
        'OF:Spe1' : 'L\'Oiseau de feu, Suite pour Orchestre (version 1919) : Danse infernale du Roi Kastcheï, Berceuse et Final ',   
    },
    'Arnold Schoenberg' : {
        '16' : 'Cinq pièces pour orchestre, op. 16',
    },
    'Bruno Mantovani' : {
        'jeuxdeau' : 'Jeux d’eau pour violon et orchestre',
    },
    'Luciano Berio' : {
        'chemin4' : 'Chemin IV pour hautbois et cordes',
    },
    'Franz Schubert' : {
        '485' : 'Symphonie n°5 en si bémol majeur, D. 485',
        '644': 'Ouverture de Rosamunde D. 644',
        '935' : 'Impromptus n°3 et 4 D. 935'
    },
    'Johannes Brahms' : {
        '68' : 'Symphonie n° 1 en ut mineur, op. 68',
        '83' : 'Concerto pour piano et orchestre n° 2 en si bémol majeur, op. 83',
    },
    'André Campra' : {
        'Les Fêtes Vénitiennes' : 'Les Fêtes Vénitiennes', // 2h40 baroque français
        'years' : '1660-1744',
    },
    'Léo Delibes' : {
        'Coppélia' : 'Coppélia', // 1h50
    },
    'Sergueï Prokofiev' : {
        'Pièces pour piano pour Salle des pas perdus' : 'Pièces pour piano pour Salle des pas perdus',
        'Alexandre Nevski' : 'Alexandre Nevski',
        '91' : 'Ouverture de Guerre et Paix, op. 91',
        '100' : 'Symphonie n°5 en si bémol majeur, op. 100',
    },
    'Gavin Bryars' : {
        'Les Fiançailles' : 'Les Fiançailles',
    },
    'Luigi Dallapiccola' : {
        'Canti di Prigionia' : 'Canti di Prigionia',
    },
    'Wolfgang Amadeus Mozart' : {
        'Les Noces de Figaro' : 'Les Noces de Figaro', // 1789 3h20
        'years' : '1756-1791',
        'K297' : 'Symphonie n°31 en ré majeur « Paris », K. 297',
        'KV297b' : 'Symphonie concertante pour vents, en mi bémol majeur, KV. 297b',
        'K315' : 'Andante pour flûte et orchestre en ut majeur, K. 315',
        'K488' : 'Concerto pour piano n°23 K.488 en La Majeur',
        '551' : 'Symphonie n°41 en ut majeur, « Jupiter », KV. 551',
        'Nozze di Figaro, Ouverture et La deuxième comtesse « Dove sono »' : 'Nozze di Figaro, Ouverture et La deuxième comtesse « Dove sono »',
        'Don Giovanni, Ouverture et Air de Zerlina - Vedrai carino' : 'Don Giovanni, Ouverture et Air de Zerlina - Vedrai carino',
        'Così fan tutte, Ouverture et Air de Despina - Una donna a quindici anni »' : 'Così fan tutte, Ouverture et Air de Despina - Una donna a quindici anni »',
    },
    'Gioacchino Rossini' : {
        'L\'Italienne à Alger' : 'L\'Italienne à Alger', // 1813 2h45
        'years' : '1792-1868',
    },
    'Ludwig Minkus' : {
        'Paquita Grand Pas' : 'Paquita Grand Pas', // Création de la version d’Oleg Vinogradov par le Ballet du Kirov le 29 juin 1978 au Théâtre Kirov de Léningrad 
    },
    'Eric Tanguy' : {
        'Intrada' : 'Intrada',
    },
    'Camille Saint-Saëns' : {
        'Symph3' : 'Symphonie n°3 « avec orgue »',
        '33' : 'Concerto pour violoncelle et orchestre n°1 en la mineur, op. 33',
    },
    'William Walton' : {
        'Henry V' : 'Henry V',
    },
    'Felix Mendelssohn' : {
        'songe' : 'Le Songe d\'une nuit d\'été',
        '64' : 'Concerto pour violon et orchestre en mi mineur, op. 64',
    },
    'Bernd Alois Zimmermann' : {
        'nobody' : '« Nobody Knows the Trouble I See », pour trompette et orchestre',
    },
    'Jean-Louis Agobet' : {
        'Génération, pour 3 clarinettes' : 'Génération, pour 3 clarinettes',
    },
    'Toru Takemitsu' : {
        'Quotation of a dream' : 'Quotation of a dream',
    },
    'Anatoli Konstantinovitch Liadov' : {
        '62' : 'Le Lac enchanté op. 62',
    },
    'Alexandre Konstantinovitch Glazounov' : {
        'extraitsRaymonda04022016' : 'Raymonda: Acte 1 scène 2 : Grand Adagio et Acte 1 scène 2: Variation 3',
    },
    'Richard Wagner' : {
        'Tristan und Isolde, Prélude et « Liebestod »' : 'Tristan und Isolde, Prélude et « Liebestod »',
        'Parsifal, Ouverture et « Enchantement du Vendredi Saint »' : 'Parsifal, Ouverture et « Enchantement du Vendredi Saint »',
        'Götterdämmerung, Extraits' : 'Götterdämmerung, Extraits',
    },
    'François Devienne' : {
        'cfo7' : 'Concerto pour flûte et orchestre n°7 en mi mineur',
    },
    'Antonín Dvořák' : {
        '88' : 'Symphonie n°8 en sol majeur, op. 88',
    },
    'Edvard Grieg' : {
        '16' : 'Concerto pour piano en la mineur, op. 16',
    },
    'Thierry Escaich' : {
        'ClaudeSuite' : 'Suite symphonique extraite de l’Opéra "Claude"',
    },
    'Samuel Barber' : {
        '36' : 'Toccata festiva, op. 36',
    },
    'Anton Bruckner' : {
        '109' : 'Symphonie n°7 en mi majeur, A. 109',
    },
    'Robert Schumann' : {
        '54' : 'Concerto pour piano et orchestre en la mineur, op. 54',
    },
    'Vincenzo Bellini' : {
        'ConcertoHauboisMiBémolMajeur' : 'Concerto pour Hautbois et orchestre en mi bémol Majeur',
    },
    'Aram Khatchaturian' : {
        'DanseSabre' : 'La Danse du Sabre',
    },
    'Hervé Suhubiette' : {
        'Gâteaux et chapeaux' : 'Gâteaux et chapeaux',
    },
    'Johann II Strauss' : {
        'Bat' : 'La Chauve-Souris, ouverture',
    },
    'Jacques Offenbach' : {
        'CdH:Barcarolle' : 'Les Contes d\'Hoffmann, Barcarolle',
    },
    'Giuseppe Verdi' : {
        'Force du Destin : Ouverture' : 'Force du Destin : Ouverture',
        'Don Carlo : Acte II, Choeur et aria (Il Frate) « Carlo, il sommo Imperatore… »' : 'Don Carlo : Acte II, Choeur et aria (Il Frate) « Carlo, il sommo Imperatore… »',
        'Simon Boccanegra : Acte III, Prologue, récitatif avec choeur « A te l’estremo addio… »' : 'Simon Boccanegra : Acte III, Prologue, récitatif avec choeur « A te l’estremo addio… »',
        'Nabucco : Gli arredi festivi (Choeur d’introduction du 1er acte)' : 'Nabucco : Gli arredi festivi (Choeur d’introduction du 1er acte)',
        'Traviata : Prélude' : 'Traviata : Prélude',
        'Nabucco : Acte II, Air de Zaccaria. Preghiera « Vieni, o Levita ! », « Tu sul labro… »' : 'Nabucco : Acte II, Air de Zaccaria. Preghiera « Vieni, o Levita ! », « Tu sul labro… »',
        'Nabucco : Va’ pensiero' : 'Nabucco : Va’ pensiero',
        'Macbeth (version Paris 1865) : Acte II, n°10, recitatif “Studia il passo” + Air de Banco “Come dal ciel precipita”' : 'Macbeth (version Paris 1865) : Acte II, n°10, recitatif “Studia il passo” + Air de Banco “Come dal ciel precipita”',
        'Les Vêpres siciliennes : Ouverture' : 'Les Vêpres siciliennes : Ouverture',
        'Les Vêpres siciliennes : Acte II, scène 1 (n°7) : Air de Giovanni da Procida « O patria o cara », « O tu Palermo ».' : 'Les Vêpres siciliennes : Acte II, scène 1 (n°7) : Air de Giovanni da Procida « O patria o cara », « O tu Palermo ».',
        'Otello : Fuoco di gioia (1er acte)' : 'Otello : Fuoco di gioia (1er acte)',
        'Ernani : Acte I, scène 9 (final), récitatif : « Che mai veggio » + air de Silva « Infelice !... e tuo credevi »' : 'Ernani : Acte I, scène 9 (final), récitatif : « Che mai veggio » + air de Silva « Infelice !... e tuo credevi »',
        'Nabucco : Ouverture' : 'Nabucco : Ouverture',
        'Don Carlo : Acte IV, Air de Filippo « Ella Giammai m’ amo »' : 'Don Carlo : Acte IV, Air de Filippo « Ella Giammai m’ amo »',
    },
    'Spécial' : {
        'Programme spécial' : 'Programme spécial',
        'Clarinettes250216' : 'Ensemble de Clarinettes (pièce de 4 minutes, jouée par 150 élèves clarinettistes de Gironde)',
        'tourdumonde' : 'Petits et grands : Le tour du monde en 45\', Musiques de Tchaikovski, Bartok, De Falla, Copland...',
        //'nouvel_an_tlse_2016' : 'Concerts du nouvel an, Un nouvel an russe en compagnie de Tugan Sokhiev',
        'BabaYaga' : 'Baba Yaga, avec la musique de M. Moussorgski et I. Stravinski',
    },
};

var dates = [
    //
    // Concerts ONCT et Opéra TC par dates
    //
    [
        '02/07/2016', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Nelson Freire (piano)', '', [
            ['Johannes Brahms', '83'],
            ['Johannes Brahms', '68']
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '25/06/2016', '20:00', 'ONCT', 'Thomas Sondergard (dir.)', 'Inon Barnatan (piano)', '', [
            ['Ludwig van Beethoven', '72B'],
            ['Ludwig van Beethoven', '58'],
            ['Piotr Ilitch Tchaïkovski', '17'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '17/06/2016', '20:00', 'ONCT', 'Bruno Mantovani (dir.)', 'Renaud Capuçon (violon), Olivier Stankiewicz (hautbois)', '', [
            ['Arnold Schoenberg', '16'],
            ['Bruno Mantovani', 'jeuxdeau'],
            ['Luciano Berio', 'chemin4'],
            ['Franz Schubert', '485'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '12/06/2016', '15:00', 'BC', 'Oleg Vinogradov d\'après Marius Petipa, Maurice Béjard (chorégraphies)', 'Joop Stokvis décors et costumes, Oleg Vinogradov lumières, réalisées par Patrick Méeüs', 'Joëlle Roustan et Roger Bernard décors et costumes, Roger Bernard lumières', [ // 1h15
            ['Ludwig Minkus', 'Paquita Grand Pas', 'Paquita Grand Pas'],
            ['Igor Fyodorovich Stravinsky', 'oiseausuiteX', 'L\'Oiseau de feu'],
        ],
        'Toulouse', 'Halle aux Grains', 'Ballet',
    ],
    [
        '11/06/2016', '20:00', 'BC', 'Oleg Vinogradov d\'après Marius Petipa, Maurice Béjard (chorégraphies)', 'Joop Stokvis décors et costumes, Oleg Vinogradov lumières, réalisées par Patrick Méeüs', 'Joëlle Roustan et Roger Bernard décors et costumes, Roger Bernard lumières', [ // 1h15
            ['Ludwig Minkus', 'Paquita Grand Pas', 'Paquita Grand Pas'],
            ['Igor Fyodorovich Stravinsky', 'oiseausuiteX', 'L\'Oiseau de feu'],
        ],
        'Toulouse', 'Halle aux Grains', 'Ballet',
    ],
    [
        '10/06/2016', '20:00', 'BC', 'Oleg Vinogradov d\'après Marius Petipa, Maurice Béjard (chorégraphies)', 'Joop Stokvis décors et costumes, Oleg Vinogradov lumières, réalisées par Patrick Méeüs', 'Joëlle Roustan et Roger Bernard décors et costumes, Roger Bernard lumières', [ // 1h15
            ['Ludwig Minkus', 'Paquita Grand Pas', 'Paquita Grand Pas'],
            ['Igor Fyodorovich Stravinsky', 'oiseausuiteX', 'L\'Oiseau de feu'],
        ],
        'Toulouse', 'Halle aux Grains', 'Ballet',
    ],
    [
        '09/06/2016', '20:00', 'ONBA', 'Alain Lombard (dir.)', '', '', [
            ['Béla Bartók', 'cordes_percu_celesta'],
            ['Hector Berlioz', 'symph_fantastique'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [
        '09/06/2016', '20:00', 'BC', 'Oleg Vinogradov d\'après Marius Petipa, Maurice Béjard (chorégraphies)', 'Joop Stokvis décors et costumes, Oleg Vinogradov lumières, réalisées par Patrick Méeüs', 'Joëlle Roustan et Roger Bernard décors et costumes, Roger Bernard lumières', [ // 1h15
            ['Ludwig Minkus', 'Paquita Grand Pas', 'Paquita Grand Pas'],
            ['Igor Fyodorovich Stravinsky', 'oiseausuiteX', 'L\'Oiseau de feu'],
        ],
        'Toulouse', 'Halle aux Grains', 'Ballet',
    ],
    [
        '08/06/2016', '20:00', 'BC', 'Oleg Vinogradov d\'après Marius Petipa, Maurice Béjard (chorégraphies)', 'Joop Stokvis décors et costumes, Oleg Vinogradov lumières, réalisées par Patrick Méeüs', 'Joëlle Roustan et Roger Bernard décors et costumes, Roger Bernard lumières', [ // 1h15
            ['Ludwig Minkus', 'Paquita Grand Pas', 'Paquita Grand Pas'],
            ['Igor Fyodorovich Stravinsky', 'oiseausuiteX', 'L\'Oiseau de feu'],
        ],
        'Toulouse', 'Halle aux Grains', 'Ballet',
    ],
    [
        '29/05/2016', '15:00', 'TC', '', '', '', [ // 2h45
            ['Gioacchino Rossini', 'L\'Italienne à Alger']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '27/05/2016', '20:00', 'TC', '', '', '', [ // 2h45
            ['Gioacchino Rossini', 'L\'Italienne à Alger']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '24/05/2016', '20:00', 'TC', '', '', '', [ // 2h45
            ['Gioacchino Rossini', 'L\'Italienne à Alger']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '22/05/2016', '15:00', 'TC', '', '', '', [ // 2h45
            ['Gioacchino Rossini', 'L\'Italienne à Alger']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '20/05/2016', '20:00', 'ONBA', 'Geoffrey Styles (dir.)', '', '', [
            ['Spécial', 'Programme spécial']
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [
        '20/05/2016', '20:00', 'TC', '', '', '', [ // 2h45
            ['Gioacchino Rossini', 'L\'Italienne à Alger']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '19/05/2016', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Gautier Capuçon (violoncelle)', '', [
            ['Olivier Messiaen', 'offrandes'],
            ['Henri Dutilleux', 'toutunmondelointain'],
            ['Claude Debussy', 'lamer'],
            ['Igor Fyodorovich Stravinsky', 'oiseausuite2'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '17/05/2016', '20:00', 'TC', '', '', '', [ // 2h45
            ['Gioacchino Rossini', 'L\'Italienne à Alger']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '13/05/2016', '19:00', 'ONBA', 'Michel Plasson (dir.)', 'Sarah Kim (orgue)', '', [
            ['Eric Tanguy', 'Intrada'],
            ['Maurice Ravel', 'M.61'],
            ['Maurice Ravel', 'La Valse'],
            ['Camille Saint-Saëns', 'Symph3'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [
        '12/05/2016', '20:00', 'ONBA', 'Michel Plasson (dir.)', 'Sarah Kim (orgue)', '', [
            ['Eric Tanguy', 'Intrada'],
            ['Maurice Ravel', 'M.61'],
            ['Maurice Ravel', 'La Valse'],
            ['Camille Saint-Saëns', 'Symph3'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [
        '29/04/2016', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Julie Boulianne (mezzo-soprano), Loïc Félix (ténor), Orfeón Donostiarra (chœur), José Antonio Sainz Alfaro (chef de chœur)', '', [
            ['Hector Berlioz', '17'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '28/04/2016', '20:00', 'ONBA', 'Paul Daniel (dir.)', 'Aude Extrémo (contre-alto)', 'Chœur de l’Opéra National de Bordeaux, Salvatore Caputo, chef de chœur, Chœur de l\'Armée Française, sous la direction d\'Aurore Tillac', [
            ['Sergueï Prokofiev', 'Alexandre Nevski'],
            ['William Walton', 'Henry V'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [
        '26/04/2016', '20:00', 'TC', '', '', '', [ // 3h20
            ['Wolfgang Amadeus Mozart', 'Les Noces de Figaro'],
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '24/04/2016', '15:00', 'TC', '', '', '', [ // 3h20 audiodescription
            ['Wolfgang Amadeus Mozart', 'Les Noces de Figaro'],
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '23/04/2016', '18:00', 'ONCT', 'Pierre Bleuse (dir.)', '', '', [
            ['Leonard Bernstein', 'candide'],
            ['George Gershwin', 'americain_a_paris'],
            ['Leonard Bernstein', 'wss_danses'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '22/04/2016', '20:00', 'TC', '', '', '', [ // 3h20 audiodescription
            ['Wolfgang Amadeus Mozart', 'Les Noces de Figaro'],
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '19/04/2016', '20:00', 'TC', '', '', '', [ // 3h20
            ['Wolfgang Amadeus Mozart', 'Les Noces de Figaro'],
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '17/04/2016', '15:00', 'TC', '', '', '', [ // 3h20
            ['Wolfgang Amadeus Mozart', 'Les Noces de Figaro'],
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '17/04/2016', '15:00', 'BC', 'Kader Belarbi, Angel Rodriguez, Kader Belarbi (chorégraphies)', 'Michaela Buerger (costumes), Patrick Méeüs (lumières)', 'Paradis Perdus / Nos mémoires enfouies', [ // (1h45)
            ['Sergueï Prokofiev', 'Pièces pour piano pour Salle des pas perdus', 'Salle des pas perdus'],
            ['Gavin Bryars', 'Les Fiançailles', 'Thousand of Thoughts'],
            ['Luigi Dallapiccola', 'Canti di Prigionia', 'Mur-Mur'],
        ],
        'Toulouse', 'Saint-Pierre-des-Cuisine', 'Ballet', // Auditorium 
    ],
    [
        '16/04/2016', '20:00', 'BC', 'Kader Belarbi, Angel Rodriguez, Kader Belarbi (chorégraphies)', 'Michaela Buerger (costumes), Patrick Méeüs (lumières)', '', [
            ['Sergueï Prokofiev', 'Pièces pour piano pour Salle des pas perdus', 'Salle des pas perdus'],
            ['Gavin Bryars', 'Les Fiançailles', 'Thousand of Thoughts'],
            ['Luigi Dallapiccola', 'Canti di Prigionia', 'Mur-Mur'],
        ],
        'Toulouse', 'Saint-Pierre-des-Cuisine', 'Ballet', // Auditorium 
    ],
    [
        '15/04/2016', '20:00', 'TC', '', '', '', [ // 3h20
            ['Wolfgang Amadeus Mozart', 'Les Noces de Figaro'],
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '15/04/2016', '20:00', 'BC', 'Kader Belarbi, Angel Rodriguez, Kader Belarbi (chorégraphies)', 'Michaela Buerger (costumes), Patrick Méeüs (lumières)', '', [
            ['Sergueï Prokofiev', 'Pièces pour piano pour Salle des pas perdus', 'Salle des pas perdus'],
            ['Gavin Bryars', 'Les Fiançailles', 'Thousand of Thoughts'],
            ['Luigi Dallapiccola', 'Canti di Prigionia', 'Mur-Mur'],
        ],
        'Toulouse', 'Saint-Pierre-des-Cuisine', 'Ballet', // Auditorium 
    ],
    [
        '14/04/2016', '20:00', 'BC', 'Kader Belarbi, Angel Rodriguez, Kader Belarbi (chorégraphies)', 'Michaela Buerger (costumes), Patrick Méeüs (lumières)', '', [
            ['Sergueï Prokofiev', 'Pièces pour piano pour Salle des pas perdus', 'Salle des pas perdus'],
            ['Gavin Bryars', 'Les Fiançailles', 'Thousand of Thoughts'],
            ['Luigi Dallapiccola', 'Canti di Prigionia', 'Mur-Mur'],
        ],
        'Toulouse', 'Saint-Pierre-des-Cuisine', 'Ballet', // Auditorium 
    ],
    [
        '13/04/2016', '20:00', 'BC', 'Kader Belarbi, Angel Rodriguez, Kader Belarbi (chorégraphies)', 'Michaela Buerger (costumes), Patrick Méeüs (lumières)', '', [
            ['Sergueï Prokofiev', 'Pièces pour piano pour Salle des pas perdus', 'Salle des pas perdus'],
            ['Gavin Bryars', 'Les Fiançailles', 'Thousand of Thoughts'],
            ['Luigi Dallapiccola', 'Canti di Prigionia', 'Mur-Mur'],
        ],
        'Toulouse', 'Saint-Pierre-des-Cuisine', 'Ballet', // Auditorium 
    ],
    [
        '07/04/2016', '20:00', 'ONBA', 'Paul Daniel (dir.)', 'Chœur de femmes de l\'Opéra National de Bordeaux, Chef de chœur, Salvatore Caputo', 'Chloé Briot, Alice Ferrière (sopranos), Juliette Deschamps, réalisation vidéo et adaptation du texte', [
            ['Felix Mendelssohn', 'songe'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [
        '26/03/2016', '20:00', 'ONCT', 'Andris Poga (dir.)', 'Fazil Say (piano)', '', [
            ['Marc-André Dalbavie', 'color'],
            ['Fazil Say', 'water'],
            ['Dmitri Dmitrievitch Chostakovitch', '10'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '24/03/2016', '20:00', 'ONBA', 'Paul Daniel (dir.)', 'Laurent Dupéré (trompette)', '', [
            ['Bernd Alois Zimmermann', 'nobody'],
            ['Gustav Mahler', 'Symph6'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [ 
        '22/03/2016', '20:00', 'BC', 'Charles Jude', '', '', [
            ['Léo Delibes', 'Coppélia']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Ballet',
    ],
    [ 
        '20/03/2016', '15:00', 'BC', 'Charles Jude', '', '', [
            ['Léo Delibes', 'Coppélia']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Ballet',
    ],
    [
        '20/03/2016', '10:45', 'ONCT', 'Christophe Mangou (dir. & présentation)', 'Hervé Salliot (récitant)', '', [
            ['Damien Lehman', 'alibaba'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [ 
        '19/03/2016', '20:00', 'BC', 'Charles Jude', '', '', [
            ['Léo Delibes', 'Coppélia']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Ballet',
    ],
    [ 
        '19/03/2016', '15:00', 'BC', 'Charles Jude', '', '', [
            ['Léo Delibes', 'Coppélia']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Ballet',
    ],
    [ 
        '18/03/2016', '20:00', 'BC', 'Charles Jude', '', '', [
            ['Léo Delibes', 'Coppélia']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Ballet',
    ],
    [ 
        '17/03/2016', '20:00', 'BC', 'Charles Jude', '', '', [
            ['Léo Delibes', 'Coppélia']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Ballet',
    ],
    [
        '11/03/2016', '20:00', 'ONCT', 'Vladimir Spivakov (dir.)', 'Anastasia Kobekina (violoncelle)', '', [
            ['Piotr Ilitch Tchaïkovski', 'romeojuliette'],
            ['Piotr Ilitch Tchaïkovski', '33'],
            ['Sergei Vasilievich Rachmaninoff', '45'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '04/03/2016', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Vadim Gluzman (violon)', '', [
            ['David Azagra', 'Prelude'],
            ['Ludwig van Beethoven', '61'],
            ['Béla Bartók', 'op. 13, Sz. 60']
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '28/02/2016', '15:00', 'TC', 'William Christie et Robert Carsen', '', '', [
            ['André Campra', 'Les Fêtes Vénitiennes']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '27/02/2016', '20:00', 'ONCT', 'Thomas Søndergård (dir.)', 'Geneviève Laurenceau (violon)', '', [
            ['Max Bruch', '84'],
            ['Benjamin Attahir', 'NBruch'],
            ['Gustav Mahler', 'S5'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '26/02/2016', '20:00', 'TC', 'William Christie et Robert Carsen', '', '', [
            ['André Campra', 'Les Fêtes Vénitiennes']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '25/02/2016', '20:00', 'ONBA', 'Yasuaki Itakura (dir.)', 'Sébastien Batut, Sandrine Vasseur, Stéphane Kwiatek, Richard Rimbert (clarinettes)', 'Jean-Philippe Guillo, Thomas Besnard (pianos)', [
            ['Claude Debussy', 'Rhapsodie n°1 pour clarinette'],
            ['Jean-Louis Agobet', 'Génération, pour 3 clarinettes'],
            ['Spécial', 'Clarinettes250216'], // Ensemble de Clarinettes (pièce de 4 minutes, jouée par 150 élèves clarinettistes de Gironde) 
            ['Toru Takemitsu', 'Quotation of a dream'],
            ['Claude Debussy', 'lamer'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [
        '25/02/2016', '20:00', 'TC', 'William Christie et Robert Carsen', '', '', [
            ['André Campra', 'Les Fêtes Vénitiennes']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '23/02/2016', '20:00', 'TC', 'William Christie et Robert Carsen', '', '', [
            ['André Campra', 'Les Fêtes Vénitiennes']
        ],
        'Toulouse', 'Théâtre du Capitole', 'Opéra',
    ],
    [
        '19/02/2016', '20:00', 'ONCT', 'Hartmut Haenchen (dir.)', 'Isabelle van Keulen (violon)', '', [
            ['Bohuslav Martinů', 'MemorialLidice'],
            ['Karl Amadeus Hartmann', 'ConcertoFunebre'],
            ['Richard Strauss', '64'],   
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '14/02/2016', '10:45', 'ONCT', 'Nicholas Collon (dir.)', '', '', [
            ['Gustav Holst', '32'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '12/02/2016', '20:00', 'ONCT', 'Nicholas Collon (dir.)', 'Chad Hoopes (violon)', '', [
            ['Maurice Ravel', 'M.61'], 
            ['John Adams', 'ConViolon1993'], 
            ['Gustav Holst', '32']
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '6/02/2016', '18:00', 'ONCT', 'Gustavo Gimeno (dir.)', '', '', [
            ['Ludwig van Beethoven', '55'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '05/02/2016', '19:00', 'ONBA', 'Paul Daniel (dir.)', 'Matthieu Arama (violon)', '', [
            ['Anatoli Konstantinovitch Liadov', '62'],
            ['Alexandre Konstantinovitch Glazounov', 'extraitsRaymonda04022016'],
            ['Piotr Ilitch Tchaïkovski', 'extraitsBelle04022016'],
            ['Piotr Ilitch Tchaïkovski', 'extraitsLac04022016'],
            ['Piotr Ilitch Tchaïkovski', '74'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    [
        '05/02/2016', '20:00', 'ONCT', 'Gustavo Gimeno (dir.)', 'Nicholas Angelich (piano)', '', [
            ['Maurice Ravel', 'MereOye'],
            ['Maurice Ravel', 'ConcertoPianoSolMajeur'],
            ['Ludwig van Beethoven', '55'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '04/02/2016', '20:00', 'ONBA', 'Paul Daniel (dir.)', 'Matthieu Arama (violon)', '', [
            ['Anatoli Konstantinovitch Liadov', '62'],
            ['Alexandre Konstantinovitch Glazounov', 'extraitsRaymonda04022016'],
            ['Piotr Ilitch Tchaïkovski', 'extraitsBelle04022016'],
            ['Piotr Ilitch Tchaïkovski', 'extraitsLac04022016'],
            ['Piotr Ilitch Tchaïkovski', '74'],
        ],
        'Bordeaux', 'Auditorium (Dutilleux)', 'Concert',
    ],
    
    //-------------------------------------------------------------------------
    // Janvier
    //-------------------------------------------------------------------------
    
    [
        '31/01/2016', '10:45', 'ONCT', 'Christophe Mangou (dir. et présentation)', '', '', [
            ['Spécial', 'tourdumonde'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ], 
    [
        '22/01/2016', '20:00', 'ONCT', 'Josep Pons (dir.)', 'François-Frédéric Guy (piano)', '', [
            ['Richard Wagner', 'Tristan und Isolde, Prélude et « Liebestod »'],
            ['Ludwig van Beethoven', '37'],
            ['Richard Wagner', 'Parsifal, Ouverture et « Enchantement du Vendredi Saint »'],
            ['Richard Wagner', 'Götterdämmerung, Extraits'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '16/01/2016', '18:00', 'ONCT', 'Giovanni Antonini (dir.)', '', '', [
            ['Wolfgang Amadeus Mozart', 'K297'],
            ['Ludwig van Beethoven', '68'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '15/01/2016', '20:00', 'ONCT', 'Giovanni Antonini (dir.)', 'Emmanuel Pahud (flûte)', '', [
            ['Wolfgang Amadeus Mozart', 'K297'],
            ['Wolfgang Amadeus Mozart', 'K315'],
            ['François Devienne', 'cfo7'],
            ['Ludwig van Beethoven', '68'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '01/01/2016', '18:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Alexeï Ogrintchouk (hautbois)', '', [
            // CONCERTS DU NOUVEL AN : UN NOUVEL AN RUSSE EN COMPAGNIE DE TUGAN SOKHIEV
            ['Piotr Ilitch Tchaïkovski', 'BABD:Valse6'],
            ['Piotr Ilitch Tchaïkovski', 'SW:Spe1'],
            ['Piotr Ilitch Tchaïkovski', 'CN:Spe1'],
            ['Vincenzo Bellini', 'ConcertoHauboisMiBémolMajeur'],
            ['Dmitri Dmitrievitch Chostakovitch', 'Jazz2'],
            ['Aram Khatchaturian', 'DanseSabre'],
            ['Dmitri Dmitrievitch Chostakovitch', 'TahitiTrot'],
            ['Igor Fyodorovich Stravinsky', 'OF:Spe1'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    
    //-------------------------------------------------------------------------
    // Décembre
    //-------------------------------------------------------------------------
 
    [
        '31/12/2015', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Alexeï Ogrintchouk (hautbois)', '', [
            // CONCERTS DU NOUVEL AN : UN NOUVEL AN RUSSE EN COMPAGNIE DE TUGAN SOKHIEV
            ['Piotr Ilitch Tchaïkovski', 'BABD:Valse6'],
            ['Piotr Ilitch Tchaïkovski', 'SW:Spe1'],
            ['Piotr Ilitch Tchaïkovski', 'CN:Spe1'],
            ['Vincenzo Bellini', 'ConcertoHauboisMiBémolMajeur'],
            ['Dmitri Dmitrievitch Chostakovitch', 'Jazz2'],
            ['Aram Khatchaturian', 'DanseSabre'],
            ['Dmitri Dmitrievitch Chostakovitch', 'TahitiTrot'],
            ['Igor Fyodorovich Stravinsky', 'OF:Spe1'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '18/12/2015', '20:00', 'ONCT', 'Georges Prêtre (dir.)', 'Adam Laloum (piano pour moz et schu)', 'Eric Crambes (dir. violon solo pour moz)', [
            ['Ludwig van Beethoven', 'Egmont Ouverture'],
            ['Wolfgang Amadeus Mozart', 'K488'],
            ['Johann II Strauss', 'Bat'],
            ['Franz Schubert', '935'],
            ['Jacques Offenbach', 'CdH:Barcarolle'],
            ['Maurice Ravel', 'Boléro'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '13/12/2015', '10:45', 'ONCT', 'François Terrieux (dir. et chef de choeur)', 'Hervé Suhubiette (récitant et chant)', 'Eloïse Chadourne (chant), Les éclats (choeur d\'enfants), Fabrice Guérin (mise en scène)', [
            ['Hervé Suhubiette', 'Gâteaux et chapeaux'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '09/12/2015', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'David Minetti (clarinette)', 'Olivier Stankiewicz (hautbois), Jacques Deleplancque (cor), Estelle Richard (basson)', [
            ['Wolfgang Amadeus Mozart', 'KV297b'],
            ['Dmitri Dmitrievitch Chostakovitch', '93'],            
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '04/12/2015', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Ferruccio Furlanetto (basse)', 'Choeur du Capitole (choeur), Alfonso Caiani (chef de coeur)', [
            // Verdi : Airs d’opéras Don Carlo, Nabucco, Ernani, Simon Boccanegra, Vespri Siciliani, Macbeth
            ['Giuseppe Verdi', 'Force du Destin : Ouverture'],
            ['Giuseppe Verdi', 'Don Carlo : Acte II, Choeur et aria (Il Frate) « Carlo, il sommo Imperatore… »'],
            ['Giuseppe Verdi', 'Simon Boccanegra : Acte III, Prologue, récitatif avec choeur « A te l’estremo addio… »'],
            ['Giuseppe Verdi', 'Nabucco : Gli arredi festivi (Choeur d’introduction du 1er acte)'],
            ['Giuseppe Verdi', 'Traviata : Prélude'],
            ['Giuseppe Verdi', 'Nabucco : Acte II, Air de Zaccaria. Preghiera « Vieni, o Levita ! », « Tu sul labro… »'],
            ['Giuseppe Verdi', 'Nabucco : Va’ pensiero'],
            ['Giuseppe Verdi', 'Macbeth (version Paris 1865) : Acte II, n°10, recitatif “Studia il passo” + Air de Banco “Come dal ciel precipita”'],
            ['Giuseppe Verdi', 'Les Vêpres siciliennes : Ouverture'],
            ['Giuseppe Verdi', 'Les Vêpres siciliennes : Acte II, scène 1 (n°7) : Air de Giovanni da Procida « O patria o cara », « O tu Palermo ».'],
            ['Giuseppe Verdi', 'Otello : Fuoco di gioia (1er acte) '],
            ['Giuseppe Verdi', 'Ernani : Acte I, scène 9 (final), récitatif : « Che mai veggio » + air de Silva « Infelice !... e tuo credevi »'],
            ['Giuseppe Verdi', 'Nabucco : Ouverture'],
            ['Giuseppe Verdi', 'Don Carlo : Acte IV, Air de Filippo « Ella Giammai m’ amo »'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    
    //-------------------------------------------------------------------------
    // Novembre
    //-------------------------------------------------------------------------
    
    [
        '15/11/2015', '10:45', 'ONCT', 'Christophe Mangou (dir. et présentation)', 'Maëlle Mietton (récitante)', '', [
            ['Spécial', 'BabaYaga'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '06/11/2015', '20:00', 'ONCT', 'Kazuki Yamada (dir.)', 'Edgar Moreau (violoncelle)', '', [
            ['Thierry Escaich', 'ClaudeSuite'],
            ['Camille Saint-Saëns', '33'],
            ['Maurice Ravel', 'DaphnisChloéSuite2'],
            ['Maurice Ravel', 'Boléro'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    
    //-------------------------------------------------------------------------
    // Octobre
    //-------------------------------------------------------------------------
    
    [
        '30/10/2015', '20:00', 'ONCT', 'Lahav Shani (dir.)', 'Philippe Bianconi (piano)', '', [
            ['Sergueï Prokofiev', '91'],
            ['Robert Schumann', '54'],
            ['Sergueï Prokofiev', '100'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '23/10/2015', '20:00', 'ONCT', 'Joseph Swensen (dir.)', 'Itamar Zorman (violon)', '', [
            ['Felix Mendelssohn', '64'],
            ['Anton Bruckner', '109'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '17/10/2015', '20:00', 'ONCT', 'Rinaldo Alessandrini (dir.)', 'Anaïs Constans (soprano)', '', [
            ['Wolfgang Amadeus Mozart', 'Nozze di Figaro, Ouverture et La deuxième comtesse « Dove sono »'],
            ['Wolfgang Amadeus Mozart', 'Don Giovanni, Ouverture et Air de Zerlina - Vedrai carino'],
            ['Wolfgang Amadeus Mozart', 'Così fan tutte, Ouverture et Air de Despina - Una donna a quindici anni »'],
            ['Wolfgang Amadeus Mozart', '551'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    [
        '14/10/2015', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Cameron Carpenter (orgue)', '', [
            ['George Gershwin', '3songs'],
            ['Samuel Barber', '36'],
            ['Piotr Ilitch Tchaïkovski', '55'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
    
    //-------------------------------------------------------------------------
    // Septembre
    //-------------------------------------------------------------------------
    
    [
        '18/09/2015', '20:00', 'ONCT', 'Tugan Sokhiev (dir.)', 'Elisabeth Leonskaja (piano)', '', [
            ['Franz Schubert', '644'],
            ['Edvard Grieg', '16'],
            ['Antonín Dvořák', '88'],
        ],
        'Toulouse', 'Halle aux grains', 'Concert',
    ],
];

// FIN DATE

var authors_short = {
    'John Adams' : 'Adams (J.)',
    'Jean-Louis Agobet' : 'Agobet',
    'Benjamin Attahir' : 'Attahir',
    'David Azagra' : 'Azagra',
    'Samuel Barber' : 'Barber',
    'Béla Bartók' : 'Bartók',
    'Ludwig van Beethoven' : 'Beethoven',
    'Vincenzo Bellini' : 'Bellini',
    'Luciano Berio' : 'Berio',
    'Hector Berlioz' : 'Berlioz',
    'Leonard Bernstein' : 'Bernstein',
    'Johannes Brahms' : 'Brahms',
    'Max Bruch' : 'Bruch',
    'Anton Bruckner' : 'Bruckner',
    'Gavin Bryars' : 'Bryars',
    'André Campra' : 'Campra',
    'Dmitri Dmitrievitch Chostakovitch' : 'Chostakovitch',
    'Marc-André Dalbavie' : 'Dalbavie',
    'Luigi Dallapiccola' : 'Dallapiccola',
    'Claude Debussy' : 'Debussy',
    'Léo Delibes' : 'Delibes',
    'François Devienne' : 'Devienne',
    'Henri Dutilleux' : 'Dutilleux',
    'Antonín Dvořák' : 'Dvořák',
    'Thierry Escaich' : 'Escaich',
    'George Gershwin' : 'Gershwin',
    'Alexandre Konstantinovitch Glazounov' : 'Glazounov',
    'Edvard Grieg' : 'Grieg',
    'Karl Amadeus Hartmann' : 'Hartmann (K.A.)',
    'Gustav Holst' : 'Holst',
    'Aram Khatchaturian' : 'Khatchaturian',
    'Anatoli Konstantinovitch Liadov' : 'Liadov',
    'Damien Lehman' : 'Lehman',
    'Gustav Mahler' : 'Mahler',
    'Bruno Mantovani' : 'Mantovani',
    'Bohuslav Martinů' : 'Martinů',
    'Felix Mendelssohn' : 'Mendelssohn',
    'Olivier Messiaen' : 'Messiaen',
    'Ludwig Minkus' : 'Minkus',
    'Wolfgang Amadeus Mozart' : 'Mozart',
    'Jacques Offenbach' : 'Offenbach',
    'Sergueï Prokofiev' : 'Prokofiev',
    'Sergei Vasilievich Rachmaninoff' : 'Rachmaninoff',
    'Maurice Ravel' : 'Ravel',
    'Gioacchino Rossini' : 'Rossini',
    'Camille Saint-Saëns' : 'Saint-Saëns',
    'Fazil Say' : 'Say',
    'Arnold Schoenberg' : 'Schoenberg',
    'Franz Schubert' : 'Schubert',
    'Robert Schumann' : 'Schumann',
    'Johann II Strauss' : 'Strauss (J. II)',
    'Richard Strauss' : 'Strauss (R.)',
    'Igor Fyodorovich Stravinsky' : 'Stravinsky',
    'Hervé Suhubiette' : 'Suhubiette',
    'Toru Takemitsu' : 'Takemitsu',
    'Eric Tanguy' : 'Tanguy',
    'Piotr Ilitch Tchaïkovski' : 'Tchaïkovski',
    'Giuseppe Verdi' : 'Verdi',
    'Richard Wagner' : 'Wagner',
    'William Walton' : 'Walton',
    'Bernd Alois Zimmermann' : 'Zimmermann',
    'Spécial' : 'Spécial',
};

var authors_abc = [
    'John Adams',
    'Jean-Louis Agobet',
    'Benjamin Attahir',
    'David Azagra',
    'Samuel Barber',
    'Béla Bartók',
    'Ludwig van Beethoven',
    'Vincenzo Bellini',
    'Luciano Berio',
    'Hector Berlioz',
    'Leonard Bernstein',
    'Johannes Brahms',
    'Max Bruch',
    'Anton Bruckner',
    'Gavin Bryars',
    'André Campra',
    'Dmitri Dmitrievitch Chostakovitch',
    'Marc-André Dalbavie',
    'Luigi Dallapiccola',
    'Claude Debussy',
    'Léo Delibes',
    'François Devienne',
    'Henri Dutilleux',
    'Antonín Dvořák',
    'Thierry Escaich',
    'George Gershwin',
    'Alexandre Konstantinovitch Glazounov',
    'Edvard Grieg',
    'Karl Amadeus Hartmann',
    'Gustav Holst',
    'Aram Khatchaturian',
    'Anatoli Konstantinovitch Liadov',
    'Damien Lehman',
    'Gustav Mahler',
    'Bruno Mantovani',
    'Bohuslav Martinů',
    'Felix Mendelssohn',
    'Olivier Messiaen',
    'Ludwig Minkus',
    'Wolfgang Amadeus Mozart',
    'Jacques Offenbach',
    'Sergueï Prokofiev',
    'Sergei Vasilievich Rachmaninoff',
    'Maurice Ravel',
    'Gioacchino Rossini',
    'Camille Saint-Saëns',
    'Fazil Say',
    'Arnold Schoenberg',
    'Franz Schubert',
    'Robert Schumann',
    'Johann II Strauss',
    'Richard Strauss',
    'Igor Fyodorovich Stravinsky',
    'Hervé Suhubiette',
    'Toru Takemitsu',
    'Eric Tanguy',
    'Piotr Ilitch Tchaïkovski',
    'Giuseppe Verdi',
    'Richard Wagner',
    'William Walton',
    'Bernd Alois Zimmermann',
];

var months = {
    '01' : 'jan.',
    '02' : 'fév.',
    '03' : 'mars',
    '04' : 'avril',
    '05' : 'mai',
    '06' : 'juin',
    '07' : 'juil.',
    '08' : 'août',
    '09' : 'sept.',
    '10' : 'oct.',
    '11' : 'nov.',
    '12' : 'déc.',
};

var org_disp = {
    'BC' : 'Ballet du Capitole',
    'TC' : 'Théâtre du Capitole',
    'ONCT' : 'Orch. Nat. du Capitole',
    'ONBA' : 'Orch. Nat. Bordeaux Aquitaine',
};
