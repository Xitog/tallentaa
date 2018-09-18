//-----------------------------------------------------------------------------
// LOOKING DWARF STRATEGIE PROJECTS                                           -
// CONTROLEUR D'UNITEES AFFICHAGE GRAPHIQUE ET CALCUL MATRICIELLE             -
// Daté de 2001                                                               -
// Retrouvé et présenté en 2018.                                              -
// Il s'agit d'une version initiale peu complète.                             -
//-----------------------------------------------------------------------------

PROGRAM STRATEGIE_TEMPS_REEL;

// Lance les strucutures décisives

GLOBAL

    idpro   =   0;      // identifie le processus en collision avec la souris
    idselect=   0;      // identifie le processu selectionne (qui va obéir au ordre donnee par la souris)

    typecase;           // type de terrain à afficher
    Xdepart = 0;        // point de vue X de la caméra (srcolling)
    Ydepart = 0;        // point de vue Y de la caméra (scrolling)
    font1;              // la police
    file1;              // les graphismes
    file2;              // graphismes unitées

    struct Xmap[31];    // la carte
           Ymap[31];
    end;
    struct Xbrou[31];   // pour le brouillard de guerre (à la command and conquer)
           Ybrou[31];
    end;

    /*
    struct ennemi[5];
           xa1;
           ya1;
           xa2;
           ya2;
           pos;
           typeunit;
    end
    */

LOCAL

    x2;
    y2;
    graphunit;

BEGIN

    /*
    ennemi[1].xa1 = 32*5;
    ennemi[1].ya1 = 32*5;
    ennemi[1].xa2 = 32*5;
    ennemi[1].ya2 = 32*5;
    ennemi[1].pos = 0;
    ennemi[1].typeunit = 20;
    */

    text_z = -950;
    dump_type = complete_dump;

    set_fps(24, 1);
    set_mode(m640x400);                      // tester en 800 * 600 : c'est trop beau
    file1 = load_fpg("GAMES\LDS\SW\MAINGRAPH.FPG");
    file2 = load_fpg("GAMES\LDS\SW\UNITEES.FPG");
    font1 = load_fnt("GAMES\LDS\SW\CONFIG\SWJ.FNT");

    charge();
    barre();
    randomize();
    unit(4, 4, 3, 6, 3);
    unit(3, 3, 11, 3, 3);
    unit(2, 2, 7, 3, 3);
    map();
    souris();

    RETURN;
END

//-----------------------------------------------------------------------------
// Affiche une case puis disparait
//-----------------------------------------------------------------------------

PROCESS terrain(xcase, ycase, typecase);

BEGIN

    file = file1;
    priority = 0;
    x = xcase*32;
    y = ycase*32;
    graph = typecase;
    put(file1, typecase, x, y);
    RETURN;

END

//-----------------------------------------------------------------------------
// Gère la souris et le scrolling
//-----------------------------------------------------------------------------

PROCESS souris()

PRIVATE
    touche;                             //test la sensibilité clavier. 0 = très sensible 6 = peu sensible
    ids;
    c;

BEGIN

    file = file1;
    priority = 3;
    graph=7; x=0; y=0;
    mouse.z = -1000;
    LOOP

        graph = 7;

        //FROM c = 0 TO 1;
        //ids = get_id(TYPE unit);
        //signal(ids,s_sleep);
        //END

        map();

        //FROM c = 0 TO 1;
        //ids = get_id(TYPE unit);
        //signal(ids,s_wakeup);
        //END

        x=((mouse.x)/32)*32;
        y=((mouse.y)/32)*32;

        IF (y > (32*11)) y = 32*11; END

        idpro = collision(TYPE unit);     //cherche si il y a collision : si oui idpro = id processus, si non idpro = 0

        touche = touche - 1 ;

        IF (touche =< 0) IF (key(_down))  IF (Ydepart < 20) Ydepart = Ydepart + 1; touche = 2; END; END; END
        IF (touche =< 0) IF (key(_up))    IF (Ydepart > 0)  Ydepart = Ydepart - 1; touche = 2; END; END; END
        IF (touche =< 0) IF (key(_left))  IF (Xdepart > 0)  Xdepart = Xdepart - 1; touche = 2; END; END; END
        IF (touche =< 0) IF (key(_right)) IF (Xdepart < 11) Xdepart = Xdepart + 1; touche = 2; END; END; END

        IF (key(_esc)) exit("Fin",0); END

        // Si clique gauche et pas d'unité rien ne se passe
        IF (mouse.left)  IF (idpro ==  0) idselect = 0; END; END
        // Si clique gauche et unité selectionne l'unité
        IF (mouse.left)  IF (idpro <>  0) IF (idpro <> idselect) idselect = idpro; unitselect(idselect.x,idselect.y,idselect,idselect.graphunit); END; END; END
        // Donne un ordre a l'unité selectionne
        IF (mouse.right) IF (idselect<>0) idselect.x2 = (x / 32) + Xdepart; idselect.y2 = (y / 32) + Ydepart; graph = 6; END; END

        FRAME;
    END

END

//--------------------------------------------------------------------------------------------------------
// Lit 20 sur 12 case de la matrice "carte" qui seront afficher à l'écran
//--------------------------------------------------------------------------------------------------------

PROCESS map();

PRIVATE

    xcons = 0;
    ycons = 0;

BEGIN

    file = file1;
    priority = 2;
    clear_screen();

    LOOP
        LOOP
            typecase =0;
            typecase = Xmap[xcons + Xdepart].Ymap[ycons + Ydepart];
            IF (Xbrou[xcons + Xdepart].Ybrou[ycons + Ydepart] == 1) terrain(xcons, ycons, typecase); END
            xcons = xcons + 1;
            IF (xcons == 20) BREAK; END;
        END
        ycons = ycons + 1;
        xcons = 0;
        IF (ycons == 12) BREAK; END;
    END
    
    RETURN;

END

//-----------------------------------------------------------------------------
// Remplit la matrice "brouillard" de zéro (pas de vue sur la case)
//-----------------------------------------------------------------------------

PROCESS randomize();

PRIVATE

    A=0;
    B;

BEGIN

    LOOP
        B=0;
        LOOP
            Xbrou[A].Ybrou[B]= 0;
            B = B + 1;
            IF (B == 32) BREAK; END;
        END
     A = A + 1;
     IF (A == 32) BREAK; END;
     END
     RETURN;

END

//-----------------------------------------------------------------------------
// Une unité
//-----------------------------------------------------------------------------

PROCESS unit(casex, casey, graphunit, rapunit, vision)

PRIVATE

    casex;          //coordonnée matricielle X;
    casey;          //coordonnée matricielle Y;

    rap;            //temps de base que met l'unité à accomplir une action
    rapunit;        //rapidité de l'unité

    action;         //si il a fait une action pendant ce tour
    last_action;    //quelle est sa dernière action

    vision;         //largeur du champ de vision de l'unité
    A;              //X du champ de vision de l'unité
    B;              //Y du champ de vision de l'unité

BEGIN

    file = file2;
    priority = 2;
    z = 1000;       //profondeur du graphisme (ainsi la souris sera dessus le graphisme)
    graph = graphunit;
    last_action = 0;
    rap = rapunit;
    x2 = casex;
    y2 = casey;

    LOOP

        /*
        x = ennemi[1].xa1;
        y = ennemi[1].ya1;
        graph = (ennemi[1].typeunit + ennemi[1].pos);
        */

        //test de rapidité

        IF (rap =< rapunit) action = 0; rap = 10; END;
        rap = rap - 1;

        //I.A.

        IF (x2 > casex) IF (action == 0) casex = casex + 1; graph = graph - last_action; graph = graph - 1; last_action = -1; action = 1; END; END
        IF (x2 < casex) IF (action == 0) casex = casex - 1; graph = graph - last_action; graph = graph + 1; last_action = +1; action = 1; END; END
        IF (y2 > casey) IF (action == 0) casey = casey + 1; graph = graph - last_action; graph = graph + 0; last_action = +0; action = 1; END; END
        IF (y2 < casey) IF (action == 0) casey = casey - 1; graph = graph - last_action; graph = graph - 2; last_action = -2; action = 1; END; END

        //champ de vision

        A = casex - vision;
        LOOP
            B = casey - vision;
            LOOP
                IF (A > -1) IF (B > -1) IF (A < 32) IF (B < 32) Xbrou[A].Ybrou[B] = 1; END; END; END; END
                B = B + 1;
                IF (B  == (casey + vision + 1)) BREAK; END
            END
        A = A + 1;
        IF (A == (casex + vision + 1)) BREAK; END
        END

        //Affichage graphique

        x = ((casex - Xdepart) * 32);
        y = ((casey - Ydepart) * 32);

        FRAME;

    END

    RETURN;

END

//-----------------------------------------------------------------------------
// Entoure l'unité selectionné d'un carré vert qui la suit
//-----------------------------------------------------------------------------

PROCESS unitselect(x, y, idselected, typeunit)

PRIVATE
    idt;

BEGIN

    graph = 9;
    IF (typeunit == 3) idt = write(font1,0,384,0,"Homme des sables"); END
    IF (typeunit == 7) idt = write(font1,0,384,0,"Officier Impérial"); END
    IF (typeunit == 11) idt = write(font1,0,384,0,"Stormtroopers"); END
    LOOP
        x = idselect.x;
        y = idselect.y;
        FRAME;
        IF (idselect <> idselected) BREAK; END
    END
    delete_text(idt);
    RETURN;

END

//-----------------------------------------------------------------------------
// Charge la carte
//-----------------------------------------------------------------------------

PROCESS charge();

BEGIN

    load("mymap.dat", offset Xmap.Ymap);

END

//-----------------------------------------------------------------------------
// Xdepart et Ydepart que pour les calculs matricielles et ne sont
// pas traduit à l'écran (si l'objet en question est à la base matriciel).
//-----------------------------------------------------------------------------

PROCESS Barre()

BEGIN

    file = file1;
    graph = 49;
    x = 0;
    y = 32*12;
    z = -900;

    LOOP
        FRAME;
    END

END

//-----------------------------------------------------------------------------
