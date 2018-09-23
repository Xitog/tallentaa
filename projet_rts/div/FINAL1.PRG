//-----------------------------------------------------------------------------
// LOOKING DWARF STRATEGIE PROJECTS                                           -
// CONTROLEUR D'UNITEES AFFICHAGE GRAPHIQUE ET CALCUL MATRICIELLE             -
// Version du 18 août 2002                                                    -
// Je pense qu'il s'agit de la dernière version avec DIV                      -
// Il y aura des tentatives à l'IUT en Java, C...                             -
// Ensuite suivra la prochaine grande version Ruby / Gosu...                  -
//-----------------------------------------------------------------------------

// note de programmation
// sound (nom du son, volume, ??);
// timer sert à comter des secondes (voir aide)

PROGRAM STRATEGIE_TEMPS_REEL;

// Lance les strucutures décisives

GLOBAL

    introfin = 0;       // dit si l'intro est fini
    menu = 0;           // dit si un boutton a été appuyé et lequel

    idpro   =   0;      // identifie le processus en collision avec la souris
    //idselect=   0;    // identifie le processu selectionne (qui va obéir
                        // au ordre donnee par la souris)

    typecase;           // type de terrain à afficher
    Xdepart = 0;        // point de vue X de la caméra (srcolling)
    Ydepart = 0;        // point de vue Y de la caméra (scrolling)
    font1;              // la police
    file1;              // les graphismes
    file2;              // graphismes unités
    file3;              // graphismes des menus
    file3b;
    file4;              // graphismes des bâtiments
    file5;              // textures
    file6;              // button des menus de constructions
    filetir;
    fileobjectif;
    file0;              // le file de l'intro
    fileaut;

    struct Xmap[31];    // la carte
           Ymap[31];
    end;

    struct Xbrou[31];   // pour le brouillard de guerre
           Ybrou[31];   // à la Command and Conquer
    end;

    struct Xmapunit[31]; // "carte" des unités
           Ymapunit[31];
    end;
    struct Xplan2[31];
           Yplan2[31];
    end;

    cons;                // type d'unité à construire
    ccons;               // emplacement dans la liste d'attente
    resgraph=1;          // résolution de l'écran
    Xpfin;               // fin du visionnage de la carte
    Ypfin;               // pareil mais pour les Y
    Xtaillemap = 31;
    Ytaillemap = 31;
    unitallowed[20];     // unités permises

    sound1;
    sound2;              // tir1
    sound2b;             // tir Homme des sables
    sound3;
    sound4;              // SW 3
    sound5;              // SW 2
    sound6;              // SW 1
    sound7;              // triste fin perdu
    music0;
    music1;

    IDSOURIS;            // id du process (souris) principal
    menuclick;           // si la souris click sur un menu
    soundplayed;         // id du son jou‚ en ce moment

    player[2];           // nombre d'unités max par player
    playerbat[2];        //       de bâtiments

    videofin = 0;
    isound1;
    isoundcanal;

    newtext;

    //structure qui save les unités
    struct saveunits[200];
           etat1;
           vie1;
           typeunit1;
           typebat1;
           r_angle1;
           xa;
           ya;
           xb;
           yb;
           id1;
           construit1;
    end

    //variable qui compte o— on en est (sur 200)
    save1;

    camps;               // camps du joueur
    total;               // nombre d'unités sélectionnées par le joueur

    //test
    glob = "total";

    //variable global du joueur
    //modifié par Souris
    recolt;     //minerai recolté par tour
    maxcollect; //maximum qu'il peut garder
    collect;    //minerai collecté;

    //max x et y affichable
    x_max;
    y_max;

LOCAL

    x2;
    y2;
    typeunit;
    typebat;
    actif;
    etat;
    r_angle;
    Construit[4];
    casex;
    casey;
    imustdie; // si l'unité doit mourir
    tuer;     //nombre d'unité tuée par l'unité
    level;    //niveau de l'unité

    selectionne;
    vol;
    Oldcasex;
    Oldcasey;

    force;
    armure;
    vie;
    portee;
    rapmax;
    name;
    mana;

    idcible;
    tir1;

    typetir;    // quel tir possède l'unité
    compteur;   // temps qu'il faut pour construire une unité

    construit2; // bâtiment qui se construit
    sort;

BEGIN

    set_fps(24,1);
    set_mode(m640x400);
    file0 = load_fpg("NEW/INTRO.FPG");

    video();

    WHILE (Videofin == 0)
    FRAME;
    END

    let_me_alone();
    text_z = -950;
    dump_type = complete_dump;

    set_fps(60,1);        //pour l'intro
    set_mode(m640x400);   // tester en 800 * 600
                          // c'est trop beau !


    file1 = load_fpg("NEW\PJ1.FPG");
    file2 = load_fpg("NEW\UEMP.FPG");
    file3 = load_fpg("NEW\MENU.FPG");
    file3b = load_fpg("NEW\MENU2.FPG");
    file4 = load_fpg("NEW\EMPBAT.FPG");
    file5 = load_fpg("NEW\1DESERT.FPG");
    //file6 = load_fpg("SWLOE\BUTTON.FPG");
    filetir = load_fpg("NEW\TIR.FPG");
    fileobjectif = load_fpg("NEW\OBJ.FPG");

    font1 = load_fnt("NEW\SWJ.FNT");

    sound1 = load_pcm("NEW\PORTE1.PCM",0);
    sound2 = load_pcm("NEW\IMPBLST.PCM",0);
    sound2b = load_pcm("NEW\HURT.PCM",0);
    //sound3 = load_pcm("PCM\EMPTHEME.PCM",0);
    //sound4 = load_pcm("PCM\STARWA~1.PCM",0);
    //sound5 = load_pcm("PCM\STARWA~2.PCM",0);
    sound6 = load_pcm("NEW\STARWA~3.PCM",0);
    sound7 = load_pcm("NEW\SWDARK.PCM",0);
    music0 = load_pcm("NEW\EMP02.PCM",0);
    music1 = load_pcm("NEW\DOF1.PCM",0);

    intro();

    LOOP
        IF (introfin == 1) BREAK; END
        FRAME;
    END

    clear_screen();
    While (key(_enter)); FRAME; END

    set_fps(24,1);        //pour le jeu
    mainmenu();

    RETURN;

END

//-----------------------------------------------------------------------------

PROCESS video();

BEGIN
    file = file0;
    graph = 2;
    x = 0;
    y = 180;
    LOOP
        FRAME;
        compteur = compteur + 1;
        IF (compteur == 60) BREAK; END
        IF (key(_enter) or key(_esc)) finintro(); END
    END
    clear_screen();
    graph = 3;
    compteur = 0;
    LOOP
        IF (key(_enter) or key(_esc)) finintro(); END
        FRAME;
        compteur = compteur + 1;
        IF (compteur == 60) BREAK; END
    END
    clear_screen();
    intro1();
    intro2();
END

//-----------------------------------------------------------------------------

PROCESS intro1();

BEGIN
    file = file0;
    isound1 = load_pcm("NEW\SWMARCH.PCM",0);
    isoundcanal = sound(isound1, 400, 256);
    x = 320;
    y = 200;
    size = 100;
    graph = 8;
    set_fps(10,0);
    LOOP
        IF (key(_enter) or key(_esc)) finintro(); END
        FRAME;
        size = size - 1;
        IF (size == 0) BREAK; END
        IF (size == 60) intro3(); END
    END
END

//-----------------------------------------------------------------------------

PROCESS intro2();

BEGIN
    file = file0;
    x = 320;
    y = 200;
    graph = 4;
    LOOP
        FRAME;
        IF (key(_enter) or key(_esc)) finintro(); END
    END

END

//-----------------------------------------------------------------------------

PROCESS intro3();

PRIVATE;
grapht;

BEGIN
    file = file0;
    m7[z] = 256;
    set_fps(12,0);
    grapht = 1;

    fade_on();
    m7.camera=id;
    m7.height=512;

    start_mode7(0,file0,grapht,0,0,128);
    angle = angle + pi/2;
    x = 400;
    y = 200;

    LOOP
        y = y + 1;
        FRAME;
        IF (y == 1300) BREAK; END
        IF (key(_enter) or key(_esc)) finintro(); END
    END
    finintro();
END

//-----------------------------------------------------------------------------

PROCESS finintro();

BEGIN

stop_sound(isoundcanal);
Videofin = 1;

END

//-----------------------------------------------------------------------------

PROCESS intro();

PRIVATE
    counter = 300;

BEGIN

    file = file1;
    graph = 51;
    x = 640; y = 0;
    soundplayed = sound(music0, 300, 256);

    LOOP
        FRAME;
        IF (graph == 52) counter = counter - 1; END
        IF (graph == 52 and counter =< 120) size = size + 2; END
        IF (key(_enter) or key(_esc)) BREAK; END
        IF (key(_space)) BREAK; END
        IF (mouse.left) BREAK; END
        IF (mouse.right) BREAK; END
        IF (graph == 51) x = x - 5; END
        IF (x == -1360) graph = 52; x = 320; y = 200; END
        IF (counter == 0) BREAK; END
    END
    introfin = 1;
    stop_sound(soundplayed);
    soundplayed = 0;
    RETURN;

END

//-----------------------------------------------------------------------------

PROCESS mainmenu();

PRIVATE
    menunow;

BEGIN


    stop_cd();

    load("options.cfg", offset resgraph);

    sourismenu();

    file = file3;

    LOOP

    clear_screen();
    signal(TYPE button, s_kill);
    menu = 0;

    SWITCH (menunow);

    CASE 0;
        put(file3,1,320,200);

        button(2,0,320,150);
        button(6,0,600,380);
        button(3,1,320,180);
        button(4,1,320,220);
        button(5,1,320,260);
        button(7,1,320,300);
        button(9,0,100,200);
        button(8,0,539,200);
        button(10,0,320,80);

        z = 10000000000000000;
        IF (soundplayed == 0)
        soundplayed = sound(music1, 300, 256); END
    END

    CASE 1;
        clear_screen();

        put(file3,1,320,200);

        button(2,0,320,150);
        button(6,0,600,380);
        IF (resgraph == 1) button(17,1,320,180);
        ELSE button(11,1,320,180); END
        IF (resgraph == 2) button(18,1,320,220);
        ELSE button(12,1,320,220); END
        IF (resgraph == 3) button(19,1,320,260);
        ELSE button(13,1,320,260); END
        button(14,1,320,300);
        button(9,0,100,200);
        button(8,0,539,200);
        button(10,0,320,80);
    END

    CASE 2;
        clear_screen();

        put(file3,1,320,200);

        button(2,0,320,150);
        button(16,0,320,280);
        button(14,1,320,300);
        button(6,0,600,380);
        button(9,1,150,200);
        button(8,1,489,200);
        button(10,0,320,80);
    END

    CASE 3;
        clear_screen();

        put(file3,1,320,200);

        button(2,0,320,150);
        button(15,1,320,200);
        button(14,1,320,300);
        button(6,0,600,380);
        button(9,0,100,200);
        button(8,0,539,200);
        button(10,0,320,80);
    END

    END

    LOOP
        FRAME;
        IF (key(_enter)) BREAK; END;
        IF (menu <> 0) BREAK; END;
    END

    IF (menunow == 0)
        IF (menu == 7) exit("Fin",0); END
        IF (menu == 5) menunow = 1; END
        IF (menu == 3) menunow = 2; END
    END

    IF (menunow == 1)
        IF (menu == 14) menunow = 0;  END
        IF (menu == 11) resgraph = 1; END
        IF (menu == 12) resgraph = 2; END
        IF (menu == 13) resgraph = 3; END
        IF (menu == 11 or menu == 12 or menu == 13)
        save("options.cfg", offset resgraph, sizeof(resgraph)); END
    END

    IF (menunow == 2)
        IF (menu == 8) menunow = 3; END
        IF (menu == 9) menunow = 4; END
        IF (menu == 14) menunow = 0; END
    END

    IF (menunow == 3)
        IF (menu == 14) menunow = 0; END
        IF (menu == 15) BREAK; END
    END

    END

    menu = 0;

    signal(TYPE button, s_kill);
    signal(TYPE sourismenu, s_kill);

    IF (resgraph == 1) set_mode(m640x400);  Xpfin = 20; Ypfin = (12-3); END
    IF (resgraph == 2) set_mode(m800x600);  Xpfin = 25; Ypfin = (18-3); END
    IF (resgraph == 3) set_mode(m1024x768); Xpfin = 32; Ypfin = (23-2); END

    stop_sound(soundplayed);

    //lance le jeu
    charge(0);

    //camps,etat,typeunit,casex,casey,r_angle

    //camps : 0=Empire (bleue) 1=Rebelle(Rouge)
    play_cd(1,1);
    RETURN;

END

//-----------------------------------------------------------------------------

PROCESS button(graph, actif, x, y);

BEGIN

    file = file3;
    z = 0;
    LOOP
        IF (actif == 1 and collision(TYPE sourismenu))
            file = file3b;
        ELSE 
            file = file3; 
        END
        FRAME;
    END

END

//-----------------------------------------------------------------------------

PROCESS sourismenu();

PRIVATE
    idbutton;
    on;

BEGIN

    file = file1;
    graph = 30;
    mouse.x = 320; mouse.y = 100;
    z = -1000;

    LOOP

        x = mouse.x;
        y = mouse.y;

        idbutton = collision(TYPE button);

        IF (mouse.left == 1 and on == 0) on = 1; END
        IF (mouse.left == 0 and on == 1 and idbutton <> 0)
        on = 0; menu = idbutton.graph; END

        FRAME;

    END

END

//-----------------------------------------------------------------------------

//affiche une case puis disparait

PROCESS terrain(type1,xcase,ycase,typecase);

BEGIN

    IF (type1 == 0) file = file5; END
    IF (type1 == 1) file = file2; END
    IF (type1 == 2) file = file1; END
    IF (type1 == 3) file = file4; END
    priority = 0;
    x = xcase*32;
    y = ycase*32;
    graph = typecase;
    put(file, typecase, x, y);
    RETURN;

END

//-----------------------------------------------------------------------------

// gère la souris et le scrolling

PROCESS souris()

PRIVATE
    mode;
    touche;                             //test la sensibilité clavier. 0 = très sensible 6 = peu sensible
    ids;
    c;
    D;
    A;       //groupe
    B;       //groupe
    xb;      //groupe
    yb;      //groupe
    nbr;     //groupe sys
    avant;
    qui;
    oldtext; //dernier id de l'unitée pour qui on a à afficher un texte
    //newtext; //passe en global

    click;
    choix; //clique dans menu
    ouyadelaplace; //ou on va construire l'unité

    //menu de jeu
    xm = 0;
    ym;
    gm;

    //starcraft II
    idtext;

BEGIN

    text_z = -1000;
    //affichage des ressources;
    write_int(font1,Xpfin*16-10,Ypfin*32+64,5, offset collect);     // Xpfin*32-128
    write(font1,Xpfin*16,Ypfin*32+64,4,"/");                        // Xpfin*32-115
    write_int(font1,Xpfin*16+10,Ypfin*32+64,3, offset maxcollect);  // Xpfin*32-100

    // menu de jeu fin d'initialisation et definition de x_max et y_max
    ym = Ypfin*32;
    IF (resgraph == 3) gm = 2+camps; x_max = 639; y_max = 399; END
    IF (resgraph == 2) gm = 4+camps; x_max = 799; y_max = 599; END
    IF (resgraph == 1) gm = 6+camps; x_max = 1023; y_max = 767; END

    // début initialisation souris
    IDSOURIS = ID;
    file = file1;
    priority = 3;
    x =  0; y = 0; z = -1000;
    mouse.z = -1000;
    x2 = (mouse.x+(Xdepart*32))/32;
    y2 = (mouse.y+(Ydepart*32))/32;
    
    LOOP

        //menuclick = 1;
        IF (menuclick == 1)
            file = file1;
            choix = 0;
            graph = 30;

            x = mouse.x;
            y = mouse.y;

            FRAME;

        END

        //menuclick = 0;
        IF (menuclick == 0)

            //gestion des ressources;
            compteur = compteur + 1;
            IF (compteur == 75)
                collect = collect + (recolt/4);
                IF (collect > maxcollect) collect = maxcollect; END
                compteur = 0;
            END

            IF (choix == 0)
                graph = 30;
                file = file1;
                x = mouse.x;
                y = mouse.y;
            END
            IF (choix <> 0 and choix < 10)
                graph = choix;
                file = file4;
                x = mouse.x/32*32;
                y = mouse.y/32*32;
            END
            IF (choix <> 0 and choix == 70)
                graph = choix;
                file = file1;
                x = mouse.x;
                y = mouse.y;
            END

            IF (mouse.right == 1) graph = 31; END

            map();

            casex = (x+(Xdepart*32))/32;
            casey = (y+(Ydepart*32))/32;

            IF (casex > Xtaillemap) casex = Xtaillemap; END
            IF (casey > Ytaillemap) casey = Ytaillemap; END

            touche = touche - 1 ;

            IF (touche =< 0) IF (key(_down))  IF (Ydepart + Ypfin < Ytaillemap+1) Ydepart = Ydepart + 1; touche = 2; END; END; END
            IF (touche =< 0) IF (key(_up))    IF (Ydepart + Ypfin > Ypfin) Ydepart = Ydepart - 1; touche = 2; END; END; END
            IF (touche =< 0) IF (key(_left))  IF (Xdepart + Xpfin > Xpfin) Xdepart = Xdepart - 1; touche = 2; END; END; END
            IF (touche =< 0) IF (key(_right)) IF (Xdepart + Xpfin < Xtaillemap+1) Xdepart = Xdepart + 1; touche = 2; END; END; END

            IF (key(_q)) choix = 0; END
            IF (key(_esc)) retourmenu(1,4); END
            IF (key(_tab)) retourmenu(10,0);END
            IF (key(_s))   retourmenu(4,4); END
            IF (key(_c))   retourmenu(5,4); END
            IF (key(39) and total == 1)   choix = 70; END

            //scrolling souris
            IF (x == x_max and casex < Xtaillemap) Xdepart +=1; graph = 33; END
            IF (x == 0     and casex > 0         ) Xdepart -=1; graph = 35; END
            IF (y == y_max and casey < Ytaillemap) Ydepart +=1; graph = 36; END
            IF (y == 0     and casey > 0         ) Ydepart -=1; graph = 34; END

            IF (y < Ypfin*32)

            IF (mouse.left == 1 and click == 0)
                click = 1;
                x2 = casex;
                y2 = casey;
            END

            IF (choix == 0)

            IF (mouse.left == 1 and click == 1)
                IF (x2 <> casex or y2 <> casey)
                    IF (casex > x2) xb = +1; END
                    IF (casey > y2) yb = +1; END
                    IF (casex < x2) xb = -1; END
                    IF (casey < y2) yb = -1; END
                    A = x2;
                    B = y2;
                    LOOP
                        LOOP
                        xput(file1,32,(A-Xdepart)*32,(B-Ydepart)*32,0,100,4,0);
                        IF (A == casex ) BREAK; END
                        A = A + xb;
                        END
                    A = x2;
                    IF (B == casey) BREAK; END
                    B = B + yb;
                    END
                END
            END

            IF (mouse.left == 0 and click == 1)
                // reset total
                total = 0;
                // déclique
                click = 0;
                // désélectionne
                IF (idcible <> 0)
                    idcible.selectionne = 0;
                END
                // déselectionne tout
                    A = 0;
                    LOOP
                        B = 0;
                        LOOP
                            qui = Xmapunit[A].Ymapunit[B];
                            IF (qui <> 0) qui.selectionne = 0; END
                            B = B + 1;
                            IF (B > Ytaillemap) BREAK; END
                        END
                    A = A + 1;
                    IF (A > Xtaillemap) BREAK; END
                    END
                // groupe
                IF (x2 <> casex or y2 <> casey)
                    IF (casex > x2) xb = +1; END
                    IF (casey > y2) yb = +1; END
                    IF (casex < x2) xb = -1; END
                    IF (casey < y2) yb = -1; END
                    A = x2;
                    B = y2;
                    LOOP
                        LOOP
                        qui = Xmapunit[A].Ymapunit[B];
                        IF (qui <> 0) IF (qui.etat == 1)
                        IF (qui.selectionne == 0) total = total + 1; END
                        qui.selectionne = 2;
                        END; END
                        xput(file1,32,(A-Xdepart)*32,(B-Ydepart)*32,0,100,4,0);
                        IF (A == casex ) BREAK; END
                        A = A + xb;
                        END
                    A = x2;
                    IF (B == casey) BREAK; END
                    B = B + yb;
                    END
                END
                // remise à 0 des groupes
                x2 = casex;
                y2 = casey;
                // non-groupe
                idcible = Xmapunit[casex].Ymapunit[casey];
                IF (idcible <> 0)
                    IF (idcible.selectionne == 0) total = total + 1; END
                    idcible.selectionne = 2;
                END
            END

            END

            IF (total == 1 and idcible == 0)
                A=0;
                LOOP
                    B=0;
                    LOOP
                        idcible = Xmapunit[A].Ymapunit[B];
                        IF (idcible <> 0)
                            IF (idcible.selectionne == 2) BREAK; END
                        END
                        B = B + 1;
                        IF (B == Ytaillemap + 1) BREAK; END
                    END
                    A = A + 1;
                    IF (idcible <> 0)
                        IF (idcible.selectionne == 2) BREAK; END
                    END
                    IF (A == Xtaillemap + 1) BREAK; END
                END
            A = 0;
            B = 0;
            END

            END

            IF (total == 1 and idcible <> 0)
            // reset ou il y a de la place
            ouyadelaplace = 5;
                // cherche si il reste des places de libres pour construires
                IF (idcible.typebat <> 0)
                    IF (idcible.Construit[4] == 0) ouyadelaplace = 4; END
                    IF (idcible.Construit[3] == 0) ouyadelaplace = 3; END
                    IF (idcible.Construit[2] == 0) ouyadelaplace = 2; END
                    IF (idcible.Construit[1] == 0) ouyadelaplace = 1; END
                    IF (idcible.Construit[0] == 0) ouyadelaplace = 0; END
                    // annule construction
                    IF (key(_q) and idcible.construit2 <> 666)
                        WHILE (key(_q))
                        graph = 0;
                        FRAME;
                    END
                    Idcible.vie = 0;
                END

                END
                // caserne
                IF (idcible.typebat == 1 or idcible.typebat == 2)
                    IF (unitallowed[0] == 0) put(file2,3,0,Ypfin*32);  END
                    IF (unitallowed[1] == 0) put(file2,7,32,Ypfin*32); END
                    IF (unitallowed[2] == 0) put(file2,11,64,Ypfin*32);  END
                    IF (ouyadelaplace < 5);
                        IF (choix == 10 and unitallowed[0] == 0)
                        idcible.Construit[ouyadelaplace] = 1;
                        END
                        IF (choix == 20 and unitallowed[1] == 0)
                        idcible.Construit[ouyadelaplace] = 4;
                        END
                        IF (choix == 30 and unitallowed[2] == 0)
                        idcible.Construit[ouyadelaplace] = 8;
                        END
                    END
                // reset choix
                choix = 0;
                END
                // usine
                IF (idcible.typebat == 3 or idcible.typebat == 4)
                    IF (unitallowed[3] == 0) put(file2,15,0,Ypfin*32);  END
                    IF (unitallowed[4] == 0) put(file2,19,32,Ypfin*32); END
                    IF (unitallowed[5] == 0) put(file2,31,64,Ypfin*32);  END  //23
                    IF (ouyadelaplace < 5);
                        IF (choix == 10 and unitallowed[0] == 0)
                        idcible.Construit[ouyadelaplace] = 12;
                        END
                        IF (choix == 20 and unitallowed[1] == 0)
                        idcible.Construit[ouyadelaplace] = 16;
                        END
                        IF (choix == 30 and unitallowed[2] == 0)
                        idcible.Construit[ouyadelaplace] = 28;            //20
                        END
                    END
                // reset choix
                choix = 0;
                END

                IF (idcible.typeunit == 32)
                    IF (unitallowed[20] == 0) put(file1,71,0 ,Ypfin*32+64); END
                    IF (choix == 12 and unitallowed[20] == 0) choix = 70; END
                END

                IF (idcible.typeunit == 20)
                    IF (unitallowed[11] == 0) put(file4,10,0 ,Ypfin*32); END
                    IF (unitallowed[12] == 0) put(file4,11,32,Ypfin*32); END
                    IF (unitallowed[13] == 0) put(file4,12,0 ,Ypfin*32+32); END
                    IF (unitallowed[14] == 0) put(file4,13,32,Ypfin*32+32); END
                    IF (unitallowed[15] == 0) put(file4,14,64,Ypfin*32+32); END
                    IF (unitallowed[16] == 0) put(file4,15,0 ,Ypfin*32+64); END
                    IF (choix == 10 and unitallowed[11] == 0) choix = 5; END
                    IF (choix == 20 and unitallowed[12] == 0) choix = 8; END
                    IF (choix == 11 and unitallowed[13] == 0) choix = 1; END
                    IF (choix == 21 and unitallowed[14] == 0) choix = 6; END
                    IF (choix == 31 and unitallowed[15] == 0) choix = 3; END
                    IF (choix == 12 and unitallowed[16] == 0) choix = 7; END
                END

            END

            IF (y >= Ypfin*32)
                IF (mouse.left == 1 and click == 0) click = 1; END

                IF (mouse.left == 0 and click == 1)
                    IF (x >= 0 and x < 32)
                        IF (y >= Ypfin*32 and y < (Ypfin+1)*32) choix = 10; END
                        IF (y >= (Ypfin+1)*32 and y < (Ypfin+2)*32) choix = 11; END
                        IF (y >= (Ypfin+2)*32 and y < (Ypfin+3)*32) choix = 12; END
                    END
                    IF (x >= 32 and x < 64)
                        IF (y >= Ypfin*32 and y < (Ypfin+1)*32) choix = 20; END
                        IF (y >= (Ypfin+1)*32 and y < (Ypfin+2)*32) choix = 21; END
                        IF (y >= (Ypfin+2)*32 and y < (Ypfin+3)*32) choix = 22; END
                    END
                    IF (x >= 64 and x < 96)
                        IF (y >= Ypfin*32 and y < (Ypfin+1)*32) choix = 30; END
                        IF (y >= (Ypfin+1)*32 and y < (Ypfin+2)*32) choix = 31; END
                        IF (y >= (Ypfin+2)*32 and y < (Ypfin+3)*32) choix = 32; END
                    END
                click = 0;
                END
            END

            IF (y < Ypfin *32 and choix <> 0 and choix < 10)
                IF (mouse.left == 1 and click == 0) click = 1; END

                IF (mouse.left == 0 and click == 1)
                    IF (choix == 5) A = 2; B = 2; END
                    IF (choix == 8) A = 1; B = 1; END
                    IF (choix == 1) A = 2; B = 3; END
                    IF (choix == 6) A = 2; B = 2; END
                    IF (choix == 3) A = 3; B = 4; END
                    IF (choix == 7) A = 2; B = 1; END
                    c = casex;
                    LOOP
                        d = casey;
                        LOOP
                            IF (Xmapunit[c].Ymapunit[d] <> 0) click = 2; END
                            IF (Xmap[c].Ymap[d] >= 5) click = 2; END
                            IF (click == 2) BREAK; END
                            d = d + 1;
                            IF (d == casey + B) BREAK; END
                        END
                        IF (click == 2) BREAK; END
                        c = c + 1;
                        IF (c == casex + A) BREAK; END
                    END
                    IF (click == 1)
                        BAT(1,casex,casey,choix,0);
                        choix = 0;
                    END
                    click = 0;
                END
            END

            IF (y < Ypfin *32 and choix <> 0 and choix == 70)
                IF (mouse.left == 1 and click == 0) click = 1; END

                IF (mouse.left == 0 and click == 1)
                    A = Xmapunit[casex].Ymapunit[casey];
                    IF (A <> 0)
                        idcible.idcible = A;
                        idcible.sort = 1;
                    END
                    choix = 0;
                END
            END

            put(file1,gm,xm,ym);

            //sélection à la total
            /*
            IF (Xmapunit[casex].Ymapunit[casey] <> 0 and Xbrou[casex].Ybrou[casey] == 1)
            newtext = Xmapunit[casex].Ymapunit[casey]; END
            IF (newtext <> oldtext)
            oldtext = newtext;
            IF (newtext <> 0) text(newtext); END; END
            */

            /*
            //s‚lection à la Starcraft
            IF (total == 1 and idcible <> 0) newtext = idcible; END
            IF (newtext <> oldtext)
                oldtext = newtext;
                IF (newtext <> 0) text (newtext); END
            END
            */
            //s‚lection à la Starcraft II
            IF (total == 1 and idcible <> 0)
                IF (idtext <> 0)
                    signal(idtext,s_kill);
                    delete_text(all_text);
                END
                idtext = text(idcible);
            END

            FRAME;

        END //(du menuclick == 0)
    END // end loop
END // end process/begin

//--------------------------------------------------------------------------------------------------------

// lit 20 sur 12 case de la matrice "carte" qui seront afficher à l'écran

PROCESS map();

PRIVATE;
    xcons = 0;
    ycons = 0;
    blob;

BEGIN

    file = file1;
    priority = 2;
    clear_screen();

    LOOP
        LOOP
        typecase =0;

        IF (xcons + Xdepart =< Xtaillemap and ycons + Ydepart =< Ytaillemap)
            typecase = Xmap[xcons + Xdepart].Ymap[ycons + Ydepart];
            IF (Xbrou[xcons + Xdepart].Ybrou[ycons + Ydepart] == 1)
                terrain(0,xcons , ycons , typecase);
                blob = Xmapunit[xcons + Xdepart].Ymapunit[ycons + Ydepart];
                IF (blob <> 0)
                    IF (blob.selectionne == 2)
                        typecase = 9;
                        terrain(2,xcons, ycons, typecase);
                    END
                    IF (blob.typebat == 0)
                        typecase = blob.typeunit + blob.r_angle;
                        IF (typecase <> 0)
                            terrain(1,xcons , ycons , typecase);
                        END
                    END
                    IF (blob.typeunit == 0 and blob.typebat <> 0)
                        typecase = blob.typebat;
                        IF (blob.compteur =< 10 and blob.Construit[0] <> 0) typecase = typecase + 1; END
                        IF (typecase <> 0 and blob.construit2 == 666)
                            terrain(3,blob.casex-Xdepart,blob.casey-Ydepart, typecase);
                        END
                        IF (typecase <> 0 and blob.construit2 <> 666)
                            terrain(3,xcons,ycons, 50);
                        END

                    END
                END
            END
        END
        xcons = xcons + 1;
        if (xcons == Xpfin) BREAK; END;
        END
    ycons = ycons + 1;
    xcons = 0;
    if (ycons == Ypfin) BREAK; END;
    END
    RETURN;

END

//--------------------------------------------------------------------------------------------------------

// remplit la matrice "brouillard" de zéro (pas de vue sur la case)

PROCESS randomize(etatbrou, etatunit);

PRIVATE
A=0;
B;

BEGIN

    LOOP
        B=0;
        LOOP
            Xbrou[A].Ybrou[B]= etatbrou;
            Xmapunit[A].Ymapunit[B] = etatunit;
            B = B + 1;
            IF (B == 32) BREAK; END;
        END
     A = A + 1;
     IF (A == 32) BREAK; END;
     END
     RETURN;

END

//------------------------------------------------------------------------------------------------------------------------------

PROCESS BAT(etat, casex, casey, typebat, construit2);

PRIVATE;

    A;
    B;
    xfin;       //fin de decouvrage du brouillard
    yfin;
    cgraph;     //combien de temps la porte reste ouverte
    consu;
    eng;        //var : oui j'ai compris et je lance la construction
                //et j'en lance pas d'autres.

    idmenucons;
    unitcrée;

    vision;
    viemax;
    typecréé;   //type de l'unité créé
    click;
    xsortie;
    ysortie;

    timemax;    //temps pour construire le bat;

BEGIN

    x2 = 666;
    y2 = 666;

    IF (typebat == 1)   name = "Caserne";
                        rapmax = 0;
                        vision = 0;
                        viemax = 100;
                        vie    = 100;
                        armure = 1;
                        vol    = 0;
                        portee = 0;
                        force  = 0;
                        timemax= 300;
                        xfin  = 3;
                        yfin  = 3;
    END

    IF (typebat == 6)   name = "Usine Robotique";
                        rapmax = 0;
                        vision = 0;
                        viemax = 100;
                        vie    = 100;
                        armure = 1;
                        vol    = 0;
                        portee = 0;
                        force  = 0;
                        timemax=350;
                        xfin  = 3;
                        yfin  = 3;
    END

    IF (typebat == 3)   name = "Usine";
                        rapmax = 0;
                        vision = 0;
                        viemax = 100;
                        vie    = 100;
                        armure = 1;
                        vol    = 0;
                        portee = 0;
                        force  = 0;
                        timemax=400;
                        xfin  = 3;
                        yfin  = 4;
    END

    IF (typebat == 8)   name = "Collecteur";
                        rapmax = 0;
                        vision = 0;
                        viemax = 100;
                        vie    = 100;
                        armure = 1;
                        vol    = 0;
                        portee = 0;
                        force  = 0;
                        timemax=100;
                        xfin  = 1;
                        yfin  = 1;
    END

    IF (typebat == 5)   name = "Recolteur";
                        rapmax = 0;
                        vision = 0;
                        viemax = 100;
                        vie    = 100;
                        armure = 1;
                        vol    = 0;
                        portee = 0;
                        force  = 0;
                        timemax=100;
                        xfin  = 2;
                        yfin  = 2;
    END
    //Arme Secrète
    IF (typebat == 7)   name = "Relai Rayon de Mort";
                        rapmax = 0;
                        vision = 0;
                        viemax = 100;
                        vie    = 100;
                        armure = 1;
                        vol    = 0;
                        portee = 0;
                        force  = 0;
                        timemax=500;
                        xfin  = 2;
                        yfin  = 1;
    END

    playerbat[etat] = playerbat + 1;

    file = file4;
    priority = 2;
    z = 1000;

    //début boucle principale

    LOOP

    IF (vie =< 0)
        LOOP
            B=0;
            LOOP
                Xmapunit[A+casex].Ymapunit[B+casey] = 0;
                B = B + 1;
                IF (B == yfin) BREAK; END;
            END
        A = A + 1;
        IF (A == xfin) BREAK; END;
        END
        A = 0;
        B = 0;
        RETURN;
    END

    IF (vie > viemax)
        vie = viemax;
    END

    //met l'id du bâtiment

    LOOP
        B=0;
        LOOP
            Xmapunit[A+casex].Ymapunit[B+casey] = id;
            B = B + 1;
            IF (B == yfin) BREAK; END;
         END
    A = A + 1;
    IF (A == xfin) BREAK; END;
    END
    A = 0;
    B = 0;

    //boucle brouillard

    LOOP
        B=0;
        LOOP
            IF (A+casex-1 > 0 and B+casey-1 > 0 and A+casex-1 < Xtaillemap and B+casey-1 < Ytaillemap)
                Xbrou[A+casex-1].Ybrou[B+casey-1] = 1;
            END
            B = B + 1;
            IF (B == yfin+2) BREAK; END;
         END
    A = A + 1;
    IF (A == xfin+2) BREAK; END;
    END
    A = 0;
    B = 0;

    IF (construit2 == 666)
        //annule
        IF (key(_q) and Construit[0] <> 0)
            Construit[0] = 0;
            eng = 0;
            Compteur = 0;
            WHILE (key(_q))
                graph = 0;
                FRAME;
            END
            //on remet bien la boucle
            Construit[0] = Construit[1];
            Construit[1] = Construit[2];
            Construit[2] = Construit[3];
            Construit[3] = Construit[4];
            Construit[4] = 0;
        END

        //point de ralliement gérer par souris (x2, y2)
        IF (mouse.right == 1 and selectionne == 2 and total == 1) click = 1; END
        IF (mouse.right == 0 and selectionne == 2 and click == 1 and total == 1)
            x2 = IDsouris.casex;
            y2 = IDsouris.casey;
            click = 0;
        END

        IF (cgraph == 0) graph = typebat; END
        IF (cgraph <> 0) cgraph = cgraph - 1; END

        x = (casex - Xdepart) * 32;
        y = (casey - Ydepart) * 32;

        //on met dans Construit[] les typeunits des unités voulues
        IF (Construit[0] <> 0) IF (eng == 0)
            IF (Construit[0] == 1)  Compteur = 60;  END
            IF (Construit[0] == 4)  Compteur = 90;  END
            IF (Construit[0] == 8)  Compteur = 120; END
            IF (Construit[0] == 12) Compteur = 90;  END
            IF (Construit[0] == 16) Compteur = 100; END
            IF (Construit[0] == 20) Compteur = 120; END
            IF (Construit[0] == 24) Compteur = 200; END
            IF (Construit[0] == 28) Compteur = 300; END
            eng = 1;
        END; END

        IF (Compteur == 1)

            xsortie = 666;
            ysortie = 666;

        //si pas de place bloque le processus en attendant
        LOOP
        graph = 0;
        //on cherche ou mettre l'unité
            A = 0;
            LOOP
                B=0;
                LOOP
                    IF (Xmapunit[A+casex-1].Ymapunit[B+casey-1] == 0);
                        IF (Xmap[A+casex-1].Ymap[B+casey-1] < 5);
                            xsortie = A+casex-1;
                            ysortie = B+casey-1;
                        END
                    END
                    B = B + 1;
                    IF (B == yfin+2) BREAK; END;
                END
            A = A + 1;
            IF (A == xfin+2) BREAK; END;
            END
            A = 0;
            B = 0;
        IF (xsortie == 666 and ysortie == 666) FRAME; END
        IF (xsortie <> 666 or  ysortie <> 666) BREAK; END
        END

            //on construit l'unité en créant un processus
            typecr‚‚ = Construit[0];
            IF (typecr‚‚ == 1) typecr‚‚ = 0; END

            unitcr‚e = unit(etat,typecr‚‚,xsortie,ysortie,3);   //etat, typeunit,x,y,graph

            //si pas de point de ralliement xsortie = x2, ysortie = y2;
            IF (x2 <> 666 or Y2 <> 666)
                unitcr‚e.x2 = x2;
                unitcr‚e.y2 = y2;
            END

            //on remet bien la boucle
            Construit[0] = Construit[1];
            Construit[1] = Construit[2];
            Construit[2] = Construit[3];
            Construit[3] = Construit[4];
            Construit[4] = 0;

            //on remet les compteurs à 0
            Compteur = 0;
            eng = 0;
            graph = typebat + 1;
            cgraph = 20;
            sound(sound1,100,256);
        END

        IF (Compteur <> 0) Compteur = Compteur - 1; END

    END

    IF (construit2 < timemax)
        construit2 = construit2 + 1;
        IF (construit2 >= timemax)
            construit2 = 666;
            IF (typebat == 8) maxcollect = maxcollect + 100; END
            IF (typebat == 5) recolt = recolt + 10; END
        END
    END

    graph = 0;

    FRAME;

    END

END

//-----------------------------------------------------------------------------

PROCESS  text(idmaster)

PRIVATE
    idt;     //nom de l'unité
    idtr;    //pv de l'unité
    idtf;    //armure de l'unité
    idta;
    idtv;
    idtp;
    idtc;    //le compteur
    idtm;    //mana
    idtt;    //nombre de tuer
    idtl;    //level
    carac0;  //text : Vie =, Armure =,...
    carac1;
    carac2;
    carac3;
    carac4;
    carac5;  //mana
    carac6;  //tuer
    A;
    B;
    C; //wait for delete:

BEGIN

    compteur = 0;
    z = -1200;
    text_z = -1200;

    file = file2;

    typeunit = idmaster.typeunit;
    typebat  = idmaster.typebat;
    vie      = idmaster.vie;
    armure   = idmaster.armure;
    rapmax   = idmaster.rapmax;
    force    = idmaster.force;
    portee   = idmaster.portee;
    name     = idmaster.name;
    construit2 = idmaster.construit2;
    mana     = idmaster.mana;
    tuer     = idmaster.tuer;
    level    = idmaster.level;

    //Mech d'assaut AT-ST
    //Robot-Assassiin IG-88

    idt = write(font1,160,(Ypfin)*32+resgraph,0,name);

    IF (typebat == 0) graph = typeunit+3; x = 160; y = (Ypfin+1)*32+resgraph; END

    carac0 = write(font1,288,Ypfin*32+12+resgraph,2,"Vitesse : ");
    carac1 = write(font1,288,Ypfin*32+24+resgraph,2,"Force   : ");
    carac2 = write(font1,288,Ypfin*32+36+resgraph,2,"Armure  : ");
    carac3 = write(font1,288,Ypfin*32+48+resgraph,2,"Vie     : ");
    carac4 = write(font1,288,Ypfin*32+60+resgraph,2,"Portee  : ");

    IF (mana > -1)
    carac5 = write(font1,288,Ypfin*32+72+resgraph,2,"Energie : ");
    idtm = write_int(font1,384,Ypfin*32+72+resgraph,2,OFFSET mana);
    END

    carac6 = write(font1,300,Ypfin*32+resgraph,2,"Tu‚s : ");
    idtt = write_int(font1,320,Ypfin*32+resgraph,2,OFFSET tuer);
    idtl = write(font1,404,Ypfin*32+resgraph,2,level);
    //idtl = write_int(font1,404,Ypfin*32+resgraph,2,OFFSET level);

    idtr = write_int(font1,384,Ypfin*32+12+resgraph,2,OFFSET rapmax);
    idtf = write_int(font1,384,Ypfin*32+24+resgraph,2,OFFSET force);
    idta = write_int(font1,384,Ypfin*32+36+resgraph,2,OFFSET armure);
    idtv = write_int(font1,384,Ypfin*32+48+resgraph,2,OFFSET vie);
    idtp = write_int(font1,384,Ypfin*32+60+resgraph,2,OFFSET portee);
                                                  //      43       52
    IF (typebat <> 0 and construit2 == 666) idtc = write_int(font1,(Xpfin-9)*32,(Ypfin+1)*32,2,OFFSET compteur); END
    IF (typebat <> 0 and construit2 <> 666) idtc = write_int(font1,(Xpfin-9)*32,(Ypfin+1)*32,2,OFFSET construit2); C = 1; END

    LOOP
    //delete_text(idtl);
    //idtl = write(font1,404,Ypfin*32+resgraph,2,level);
    tuer     = idmaster.tuer;
    level    = idmaster.level;
    mana     = idmaster.mana;
    armure   = idmaster.armure;
    force    = idmaster.force;
    construit2 = idmaster.construit2;
    IF (C == 1 and construit2 == 666)
        delete_text(idtc);
        idtc = write_int(font1,(Xpfin-9)*32,(Ypfin+1)*32,2,OFFSET compteur);
        C = 0;
    END
    Construit[0] = idmaster.Construit[0];
    Construit[1] = idmaster.Construit[1];
    Construit[2] = idmaster.Construit[2];
    Construit[3] = idmaster.Construit[3];
    Construit[4] = idmaster.Construit[4];
    IF (typebat <> 0 and construit2 == 666)
        put(file1,camps+13,(Xpfin-9)*32,Ypfin*32);
        compteur = idmaster.compteur;
        A = 0;
        LOOP
            IF (Construit[A] <> 0)
                B = Construit[A];
                IF (B == 1) B = 0; END
                put(file,B+3,(Xpfin-9+A)*32,Ypfin*32);
            END
            A = A + 1;
            IF (A == 5) BREAK; END
        END
    END
    vie = idmaster.vie;

    //à la Total
    /*
    IF (idmaster <> newtext or vie =< 0) BREAK; END
    */

    //à la Starcraft
    IF (IDsouris.idcible <> idmaster or vie =< 0) BREAK; END

    FRAME;
    END

    delete_text(idt);
    delete_text(idtr);
    delete_text(idtf);
    delete_text(idta);
    delete_text(idtv);
    delete_text(idtp);
    delete_text(idtt);
    delete_text(idtl);
    IF (typebat <> 0) delete_text(idtc); END
    delete_text(carac0);
    delete_text(carac1);
    delete_text(carac2);
    delete_text(carac3);
    delete_text(carac4);
    delete_text(carac6);
    IF (mana > -1)
        delete_text(idtm);
        delete_text(carac5);
    END

END


//-----------------------------------------------------------------------------
// Charge la carte
//-----------------------------------------------------------------------------

PROCESS charge(mission);

PRIVATE
A=0;
B=0;
unitee;
etatunitee;
typeunitee;

BEGIN

    clear_screen();
    let_me_alone();
    delete_text(all_text);
    randomize(0,0);
    LOOP
        saveunits[save1].etat1 = 0;
        saveunits[save1].vie1  = 0;
        saveunits[save1].typeunit1 = 0;
        saveunits[save1].typebat1  = 0;
        saveunits[save1].r_angle1  = 0;
        saveunits[save1].xa = 0;
        saveunits[save1].ya = 0;
        saveunits[save1].xb = 0;
        saveunits[save1].yb = 0;
        saveunits[save1].id1  = 0;
        saveunits[save1].construit1 = 0;
    B = B + 1;
    IF (B == 201) BREAK ; END
    END
    B=0;
    minimap();
    IF (mission == 0) retourmenu(10,0); END
    souris();

    //BAT(1,15,15,1,300);
    BAT(1,20,20,3,666);
    unit(1,20,15,15,3);
    unit(1,32,4,4,3);

    //load;
    A = 0;
    B = 0;

    IF (mission == 0)
    load("NEW\SAVE\cart1.sav", offset Xmap.Ymap);
    load("NEW\SAVE\brou1.sav", offset Xbrou.Ybrou);
    load("NEW\SAVE\unit1.sav", offset saveunits);     //4 au lieu de 7
    END
    IF (mission == 31)
    load("NEW\SAVE\cart1.sav", offset Xmap.Ymap);
    load("NEW\SAVE\brou1.sav", offset Xbrou.Ybrou);
    load("NEW\SAVE\unit1.sav", offset saveunits);
    END
    IF (mission == 32)
    load("NEW\SAVE\cart2.sav", offset Xmap.Ymap);
    load("NEW\SAVE\brou2.sav", offset Xbrou.Ybrou);
    load("NEW\SAVE\unit2.sav", offset saveunits);
    END
    IF (mission == 33)
    load("NEW\SAVE\cart3.sav", offset Xmap.Ymap);
    load("NEW\SAVE\brou3.sav", offset Xbrou.Ybrou);
    load("NEW\SAVE\unit3.sav", offset saveunits);
    END
    IF (mission == 34)
    load("NEW\SAVE\cart4.sav", offset Xmap.Ymap);
    load("NEW\SAVE\brou4.sav", offset Xbrou.Ybrou);
    load("NEW\SAVE\unit4.sav", offset saveunits);
    END

    LOOP
        IF (saveunits[B].id1 <> 0)
            IF (saveunits[B].typebat1 == 0)
                A = unit(saveunits[B].etat1,saveunits[B].typeunit1,saveunits[B].xa,saveunits[B].ya,saveunits[B].r_angle1);
                A.x2 = saveunits[B].xb;
                A.y2 = saveunits[B].yb;
                A.vie = saveunits[B].vie1;
                signal(A, s_sleep);
            END
            IF (saveunits[B].typebat1 <> 0)
                A = BAT(saveunits[B].etat1,saveunits[B].xa,saveunits[B].ya,saveunits[B].typebat1,saveunits[B].construit1);
                A.vie = saveunits[B].vie1;
                signal(A, s_sleep);
            END

        END
        B = B + 1;
        IF (B == 200) BREAK; END;
    END
    Xdepart = saveunits[200].xa;
    Ydepart = saveunits[200].ya;
    camps   = saveunits[200].etat1;

    trigger(1,0,0,1);
    trigger(2,3,0,2);

    RETURN;

END


//-----------------------------------------------------------------------------
// notes:
// Xdepart et Ydepart que pou les calculs matricielles et ne sont
// pas traduit à l'‚cran (si l'objet en question est à la base
// matricielle.

//-----------------------------------------------------------------------------

// L'astuce du idselected :
// idselect est globale. C'est l'unit‚ en train d'ˆtre selectionn‚.
// On donne ses r‚f‚rences au process concern‚ qui la retienne sous
// la forme de idselected priv‚. Ainsi si leur idselected n'est plus ‚gale à idselect
// une nouvelle unité a ‚t‚ choisie et donc ils doivent s'‚liminer.
//-----------------------------------------------------------------------------

PROCESS Retourmenu(type1, flag1);

PRIVATE

    A;
    B;
    C;
    D;
    canal1;
    C1;   //nature du signal
    t1;  //texte à supprimer
    t2;
    t3;
    t4;
    t5;
    t6;
    click; //si la souris click
    ouclicke; //bouton activ‚ par click
    
    //sauvegarde
    nosave;

BEGIN

    file = file1;
    menuclick = 1;

    z = -1000;

    IF (resgraph == 1) x = 320; y = 200; END
    IF (resgraph == 2) x = 400; y = 300; END
    IF (resgraph == 3) x = 512; y = 394; END

    WHILE (key(_esc)); FRAME; END

    IF (type1 <  10)
        C1 = 3;
        IF (flag1 <> 9)
            xput(file1,60,x,y,0,100,flag1,0);
        END
    END

    IF (type1 >= 10) C1 = 2;
                    clear_screen();
                    xput(fileobjectif,1,x,y,0,100,0,0);
    END

    signal(TYPE unit,       C1);
    signal(TYPE BAT,        C1);
    signal(TYPE Map,        C1);
    signal(TYPE Terrain,    C1);
    signal(TYPE Minimap,    C1);
    signal(TYPE tir,        C1);
    signal(TYPE move,       C1);
    signal(TYPE trigger,    C1);

    //write(font1,x,y,4,glob);

    IF (type1 == 1) t1 = write(font1,x,y-180,4,"=== Menu ===");
        xput(file1,61,x,y-150,0,100,0,0);
        t2 = write(font1,x,y-150,4,"Reprendre Partie");
        xput(file1,61,x,y-110,0,100,0,0);
        t3 = write(font1,x,y-110,4,"Sauvegarder Partie");
        xput(file1,61,x,y-70,0,100,0,0);
        t4 = write(font1,x,y-70,4,"Charger Partie");
        xput(file1,61,x,y+180,0,100,0,0);
        t5 = write(font1,x,y+180,4,"Quitter Partie");
    END

    IF (type1 == 2) canal1 = sound(sound7,256,256);
        t1 = write(font1,x,y-180,4,"=== D‚faite ! ===");
        t2 = write(font1,x,y-150,4,"Vos forces ont été anéanties");
        xput(file1,61,x,y+180,0,100,0,0);
        t3 = write(font1,x,y+180,4,"Quitter Partie");
    END

    IF (type1 == 3) canal1 = sound(sound6,256,256);
        t1 = write(font1,x,y-180,4,"=== Victoire ! ===");
        t2 = write(font1,x,y-150,4,"Vous avez gagné !");
        xput(file1,61,x,y+180,0,100,0,0);
        t3 = write(font1,x,y+180,4,"Quitter Partie");
    END

    IF (type1 == 4) t1 = write(font1,x,y-180,4,"=== Sauvegarder ===");
        xput(file1,61,x,y-150,0,100,0,0);
        t2 = write(font1,x,y-150,4,"Emplacement 1");
        xput(file1,61,x,y-110,0,100,0,0);
        t3 = write(font1,x,y-110,4,"Emplacement 2");
        xput(file1,61,x,y-70,0,100,0,0);
        t4 = write(font1,x,y-70,4,"Emplacement 3");
        xput(file1,61,x,y-30,0,100,0,0);
        t5 = write(font1,x,y-30,4,"Emplacement 4");
        xput(file1,61,x,y+180,0,100,0,0);
        t6 = write(font1,x,y+180,4,"Annuler");
    END

    IF (type1 == 5) t1 = write(font1,x,y-180,4,"=== Charger ===");
        xput(file1,61,x,y-150,0,100,0,0);
        t2 = write(font1,x,y-150,4,"Emplacement 1");
        xput(file1,61,x,y-110,0,100,0,0);
        t3 = write(font1,x,y-110,4,"Emplacement 2");
        xput(file1,61,x,y-70,0,100,0,0);
        t4 = write(font1,x,y-70,4,"Emplacement 3");
        xput(file1,61,x,y-30,0,100,0,0);
        t5 = write(font1,x,y-30,4,"Emplacement 4");
        xput(file1,61,x,y+180,0,100,0,0);
        t6 = write(font1,x,y+180,4,"Annuler");
    END

    IF (type1 >= 10) xput(file1,61,x,y+180,0,100,0,0);
        t1 = write(font1,x,y+180,4,"Quitter Briefing");
    END

    LOOP

    IF (mouse.left == 1) click = 1; END

    IF (mouse.left == 0 and click == 1)
        IF (IDsouris.x > (x-100) and IDsouris.x < (x+100))
            IF (IDsouris.y > (y-150-15) and IDsouris.y < (y-150+15))
                IF (type1 == 1) ouclicke = 1; END
                IF (type1 == 4 or type1 == 5) ouclicke = 31; END
            END
            IF (IDsouris.y > (y-110-15) and IDsouris.y < (y-110+15))
                IF (type1 == 4 or type1 == 5) ouclicke = 32; END
                IF (type1 == 1)
                    Retourmenu(4,9);
                    delete_text(t1);
                    delete_text(t2);
                    delete_text(t3);
                    delete_text(t4);
                    delete_text(t5);
                    RETURN;
                    ouclicke = 0;
                END
            END
            IF (IDsouris.y > (y-70-15) and IDsouris.y < (y-70+15))
                IF (type1 == 4 or type1 == 5) ouclicke = 33; END
                IF (type1 == 1)
                    Retourmenu(5,9);
                    delete_text(t1);
                    delete_text(t2);
                    delete_text(t3);
                    delete_text(t4);
                    delete_text(t5);
                    RETURN;
                    ouclicke = 0;
                END
            END
            IF (IDsouris.y > (y-30-15) and IDsouris.y < (y-30+15))
                IF (type1 == 4 or type1 == 5) ouclicke = 34; END
            END
            IF (IDsouris.y > (y+180-15) and IDsouris.y < (y+180+15))
                IF (type1 < 4) ouclicke = 2; END
                IF (type1 >= 4) ouclicke = 1; END
            END
        END
        click = 0;
    END

    IF (key(_n) or ouclicke == 1)
        signal(TYPE unit, s_wakeup);
        signal(TYPE BAT, s_wakeup);
        signal(TYPE Map, s_wakeup);
        signal(TYPE Terrain, s_wakeup);
        signal(TYPE Minimap, s_wakeup);
        signal(TYPE Tir, s_wakeup);
        signal(TYPE move, s_wakeup);
        signal(TYPE trigger, s_wakeup);
        stop_sound(canal1);
        menuclick = 0;
        delete_text(t1);
        IF (type1 < 10)
            delete_text(t2);
            delete_text(t3);
        END
        IF (type1 == 4 or type1 == 5)
            delete_text(t4);
            delete_text(t5);
            delete_text(t6);
        END
        IF (type1 == 1)
            delete_text(t4);
            delete_text(t5);
        END
        ouclicke = 0;
        RETURN;
    END;

    IF (key(_y) and type1 =< 10) BREAK; END
    IF (ouclicke == 2) BREAK; END

    IF (ouclicke >= 30 and type1 == 5)
        BREAK;
    END

    IF (ouclicke >= 30 and type1 == 4)

        B = 0;
        LOOP
            saveunits[save1].etat1 = 0;
            saveunits[save1].vie1  = 0;
            saveunits[save1].typeunit1 = 0;
            saveunits[save1].typebat1  = 0;
            saveunits[save1].r_angle1  = 0;
            saveunits[save1].xa = 0;
            saveunits[save1].ya = 0;
            saveunits[save1].xb = 0;
            saveunits[save1].yb = 0;
            saveunits[save1].id1  = 0;
            saveunits[save1].construit1 = 0;
        B = B + 1;
        IF (B == 201) BREAK ; END
        END

        //save;
        save1 = 0;
        A = 0;
        B = 0;

        IF (ouclicke == 31)
        save("NEW\SAVE\cart1.sav",&Xmap.Ymap,32*32);
        save("NEW\SAVE\brou1.sav",&Xbrou.Ybrou,32*32);
        //save(glob,&Xbrou.Ybrou,32*32);
        END
        IF (ouclicke == 32)
        save("NEW\SAVE\cart2.sav",&Xmap.Ymap,32*32);
        save("NEW\SAVE\brou2.sav",&Xbrou.Ybrou,32*32);
        END
        IF (ouclicke == 33)
        save("NEW\SAVE\cart3.sav",&Xmap.Ymap,32*32);
        save("NEW\SAVE\brou3.sav",&Xbrou.Ybrou,32*32);
        END
        IF (ouclicke == 34)
        save("NEW\SAVE\cart4.sav",&Xmap.Ymap,32*32);
        save("NEW\SAVE\brou4.sav",&Xbrou.Ybrou,32*32);
        END

        LOOP
            B=0;
            LOOP
                IF (Xmapunit[A].Ymapunit[B] <> 0)
                    nosave = 0;
                    C=0;
                    D=Xmapunit[A].Ymapunit[B];
                    LOOP
                        IF (saveunits[C].id1 == D) nosave = 1; BREAK; END
                        IF (C == 200) BREAK; END
                        C = C + 1;
                    END
                    IF (nosave == 0)
                        saveunits[save1].etat1 = D.etat;
                        saveunits[save1].vie1  = D.vie;
                        saveunits[save1].typeunit1 = D.typeunit;
                        saveunits[save1].typebat1  = D.typebat;
                        saveunits[save1].r_angle1  = D.r_angle;
                        saveunits[save1].xa = D.casex;
                        saveunits[save1].ya = D.casey;
                        saveunits[save1].xb = D.x2;
                        saveunits[save1].yb = D.y2;
                        saveunits[save1].id1  = D;
                        saveunits[save1].construit1 = D.construit2;
                        save1 = save1 + 1;
                    END
                END
            B = B + 1;
            IF (B == 32) BREAK; END;
            END
        A = A + 1;
        IF (A == 32) BREAK; END;
        END
        saveunits[200].xa = Xdepart;
        saveunits[200].ya = Ydepart;
        saveunits[200].etat1 = camps;

        IF (ouclicke == 31)
        save("NEW\SAVE\unit1.sav",&saveunits,201*11);
        END
        IF (ouclicke == 32)
        save("NEW\SAVE\unit2.sav",&saveunits,201*11);
        END
        IF (ouclicke == 33)
        save("NEW\SAVE\unit3.sav",&saveunits,201*11);
        END
        IF (ouclicke == 34)
        save("NEW\SAVE\unit4.sav",&saveunits,201*11);
        END

        A = 0;
        B = 0;
        ouclicke = 1;
    END

    FRAME;

    END

    randomize(0,0);
    delete_text(t1);
    delete_text(t2);
    delete_text(t3);
    menuclick = 0;
    signal(TYPE Souris,     C1);
    stop_sound(canal1);
    delete_text(all_text);
    let_me_alone();
    clear_screen();
    IF (type1 <> 5) set_mode(m640x400); END

        LOOP
            B=0;
            LOOP
                Xbrou[A].Ybrou[B]= 0;
                Xmapunit[A].Ymapunit[B]= 0;
                B = B + 1;
                IF (B == 32) BREAK; END;
            END
         A = A + 1;
         IF (A == 32) BREAK; END;
         END

    A = 0;

    player[0] = 0;
    player[1] = 0;
    player[2] = 0;
    playerbat[0] = 0;
    playerbat[1] = 0;
    playerbat[2] = 0;

    menu = 0;
    IF (type1 <> 5) mainmenu(); END
    IF (type1 == 5)
        souris();
        charge(ouclicke);
    END

END

//-----------------------------------------------------------------------------

PROCESS minimap();

PRIVATE

    typeterrain;

BEGIN

    file = file1;
    x = (Xpfin - 3)*32;
    y = Ypfin*32;
    z = 0;

    LOOP
        x2 = 0;
        y2 = 0;
        put(file,22,x,y);
        LOOP
            LOOP
            typecase = Xmapunit[x2].Ymapunit[y2];
            IF (Xbrou[x2].Ybrou[y2] == 1)
                //le terrain
                typeterrain = Xmap[x2].Ymap[y2];
                IF (typeterrain == 0) etat = 0; END
                IF (typeterrain == 1) etat = 1; END
                IF (typeterrain == 3) etat = 0; END
                IF (typeterrain == 4) etat = 0; END
                IF (typeterrain == 5) etat = 2; END
                IF (typeterrain == 6) etat = 3; END
                put(file,100+etat,(Xpfin-3)*32+(x2*2),Ypfin*32+(y2*2));
                put(file,100+etat,(Xpfin-3)*32+(x2*2+1),Ypfin*32+(y2*2));
                put(file,100+etat,(Xpfin-3)*32+(x2*2),Ypfin*32+(y2*2+1));
                put(file,100+etat,(Xpfin-3)*32+(x2*2+1),Ypfin*32+(y2*2+1));
                //les unités
                IF (typecase <> 0)
                IF (typecase.etat <> 0)
                etat = typecase.etat;
                put(file,19+etat,(Xpfin-3)*32+(x2*2),Ypfin*32+(y2*2));
                put(file,19+etat,(Xpfin-3)*32+(x2*2+1),Ypfin*32+(y2*2));
                put(file,19+etat,(Xpfin-3)*32+(x2*2),Ypfin*32+(y2*2+1));
                put(file,19+etat,(Xpfin-3)*32+(x2*2+1),Ypfin*32+(y2*2+1));
                END; END
            END
            x2 = x2 + 1;
            if (x2 == 32) BREAK; END;
            END
        y2 = y2 + 1;
        x2 = 0;
        if (y2 == 32) BREAK; END;
        END

        FRAME;
    END

END

//-----------------------------------------------------------------------------

PROCESS unit(etat, typeunit, casex, casey, r_angle);

PRIVATE

    rapidite;
    idsauveur;

    vision;
    viemax;

    A;
    B;
    C;  //variable de comptage pour mana

    xcible;
    ycible;

    manamax=250;
    leveled;

BEGIN

    player[etat] = player[etat] + 1;

    x2 = casex;
    y2 = casey;
    Oldcasex = casex;
    Oldcasey = casey;

    // définition des unités

    IF (typeunit == 0)  name = "Scouttrooper";
        rapmax = 8;
        vision = 3;
        viemax = 40;
        vie    = 40;
        armure = 2;
        vol    = 0;
        portee = 3;
        force  = 4;
        typetir= 2;
        mana   = -1;
    END

    IF (typeunit == 4)  name = "Stormtrooper";
        rapmax = 10;
        vision = 3;
        viemax = 40;
        vie    = 40;
        armure = 3;
        vol    = 0;
        portee = 4;
        force  = 5;
        typetir= 1;
        mana   = -1;
    END

    IF (typeunit == 8)  name = "Ing‚nieur Imp‚rial";
        // Officier Impérial (Ingénieur)
        rapmax = 10;
        vision = 3;
        viemax = 30;
        vie    = 30;
        armure = 2;
        vol    = 0;
        portee = 3;
        force  = 4;
        typetir= 2;
        mana   = -1;
    END

    IF (typeunit == 12) name = "Droïde Sonde";
        rapmax = 6;
        vision = 3;
        viemax = 50;
        vie    = 50;
        armure = 2;
        vol    = 0;
        portee = 3;
        force  = 4;
        typetir= 1;
        mana   = -1;
    END

    IF (typeunit == 16) name = "Droïde Médecin";
        rapmax = 12;
        vision = 3;
        viemax = 45;
        vie    = 45;
        armure = 2;
        vol    = 0;
        portee = 1;
        force  = 1;
        typetir= 3;
        mana   = 0;
    END

    IF (typeunit == 20) name = "Ouvrier";
        rapmax = 12;
        vision = 3;
        viemax = 80;
        vie    = 80;
        armure = 3;
        vol    = 0;
        portee = 1;
        force  = 8;
        typetir= 3;
        mana   = -1;
    END

    IF (typeunit == 24) name = "Tank d'Assaut";
        // + Impérial
        rapmax = 12;
        vision = 3;
        viemax = 80;
        vie    = 80;
        armure = 4;
        vol    = 0;
        portee = 4;
        force  = 8;
        typetir= 1;
        mana   = -1;
    END

    IF (typeunit == 28) name = "AT-ST";
        rapmax = 12;
        vision = 3;
        viemax = 80;
        vie    = 80;
        armure = 4;
        vol    = 0;
        portee = 4;
        force  = 800;  //8
        typetir= 1;
        mana   = -1;
    END

    IF (typeunit == 32) name = "Psyker Imp‚rial";
        //officier Impérial (Psyker)
        rapmax = 12;
        vision = 3;
        viemax = 30;
        vie    = 30;
        armure = 2;
        vol    = 0;
        portee = 3;
        force  = 3;
        typetir= 1;
        mana   = 6000;     //0
    END

    IF (typeunit == 40) name = "Homme des sables";
        rapmax = 10;
        vision = 3;
        viemax = 40;
        vie    = 40;
        armure = 0;
        vol    = 0;
        portee = 1;
        force  = 4;
        typetir= 3;
        mana   = -1;
    END

    //fin des définitions
    level = "Recrue";
    file = file2;
    priority = 2;
    IF (vol == 0) z = 1000; END
    IF (vol == 1) z = 800; END
    //graph = (typeunit + r_angle);
    rapidite = rapmax;

    LOOP

    IF (vie =< 0)
                  Xmapunit[casex].Ymapunit[casey] = 0;
                  player[etat] = player[etat] - 1;
                  IF (vol == 0) Xmapunit[casex].Ymapunit[casey] = 0; END
                  IF (vol == 1) Xplan2[casex].Yplan2[casey]     = 0; END
                  signal(ID, s_kill);
                  RETURN;
    END
    IF (vie > viemax) vie = viemax; END

    //module d'exp‚rience
    IF (tuer == 5 and leveled == 0)
        level = "V‚t‚ran";
        force = force + 1;
        armure = armure + 1;
        viemax = viemax + 10;
        vie = viemax;
        IF (mana <> -1) manamax = manamax + 20; END
        leveled = 1;
    END

    IF (tuer == 15 and leveled == 1)
        level = "Elite";
        force = force + 1;
        armure = armure + 1;
        viemax = viemax + 10;
        vie = viemax;
        IF (mana <> -1) manamax = manamax + 20; END
        leveled = 2;
    END

    C = C + 1;
    IF (mana > -1 and mana < manamax and C == 4) mana = mana + 1; END
    IF (C == 10) C = 0; END

    IF (vol == 0) Xmapunit[casex].Ymapunit[casey] = 0; END
    IF (vol == 1) Xplan2[casex].Yplan2[casey]     = 0; END

    SWITCH (etat)

        CASE 0:

        A = casex - vision;
        LOOP
            B = casey - vision;
            LOOP
                IF (A>-1 and B>-1 and A<32 and B<32)
                idsauveur = Xmapunit[A].Ymapunit[B]; END
                IF (idsauveur <> 0) IF (idsauveur.etat == 1)
                etat = 1; graph = (typeunit + r_angle);
                player[0] = player[0] - 1; player[1] = player[1] + 1;
                BREAK; END; END
                B = B + 1;
                IF (B == (casey + vision + 1)) BREAK; END
            END
            A = A + 1;
            IF (etat == 1) BREAK; END
            IF (A == (casex + vision + 1)) BREAK; END
        END

        graph = 0;

        END

        ////////////////

        CASE 1:

            IF (idcible <> 0)
                IF (Xmapunit[idcible.casex].Ymapunit[idcible.casey] == 0)
                    idcible = 0; 
                END; 
            END
            
            A = casex - vision;
            LOOP
                B = casey - vision;
                LOOP
                    IF (A>-1 and B>-1 and A<32 and B<32)
                        Xbrou[A].Ybrou[B]=1; 
                    END
                    B = B + 1;
                    IF (B == (casey + vision + 1)) BREAK; END
                END
                A = A + 1;
                IF (A == (casex + vision + 1)) BREAK; END
            END

            rapidite = rapidite - 1;

            IF (mouse.right and selectionne == 2)
                IF (IDSouris.y < Ypfin*32)
                    WHILE (mouse.right == 1);
                        x = ((casex - Xdepart) * 32);
                        y = ((casey - Ydepart) * 32);
                        Xmapunit[casex].Ymapunit[casey] = ID;
                        FRAME; 
                    END
                    Xmapunit[casex].Ymapunit[casey] = 0;
                    idcible = Xmapunit[IDsouris.casex].Ymapunit[IDsouris.casey];
                    IF (idcible == 0)
                        x2 = IDsouris.casex;
                        y2 = IDsouris.casey;
                    END
                    IF (idcible <> 0 and Xbrou[IDsouris.casex].Ybrou[IDsouris.casey] == 0)
                        x2 = IDsouris.casex;
                        y2 = IDsouris.casey;
                        idcible = 0;
                    END
                END
            END

            IF (y2 == 32) y2 = 31; END
            IF (x2 == 32) x2 = 31; END

            IF (idcible <> 0)
                x2 = casex;
                y2 = casey;
                IF (idcible.etat  =< 1) A = portee; portee = 0; END
                IF (casex < (idcible.casex-portee)) x2 = idcible.casex - portee; END
                IF (casex > (idcible.casex+portee)) x2 = idcible.casex + portee; END
                IF (casey < (idcible.casey-portee)) y2 = idcible.casey - portee; END
                IF (casey > (idcible.casey+portee)) y2 = idcible.casey + portee; END
                IF (idcible.etat  =< 1) portee = A; A = 0; END
            END

            IF (x2 <> casex or y2 <> casey)
                IF (rapidite =< 0)
                    move(ID,etat,casex,casey,x2,y2,Oldcasex,Oldcasey,vol); rapidite = rapmax;
                END;
            END

            IF (x2 == casex and y2 == casey and idcible <> 0)
                IF (idcible.etat == 2 and tir1 == 0 and rapidite =< 0) tir1 = 1; tir(ID,idcible,sort); rapidite = rapmax;
                END; 
            END

            IF (Oldcasex > casex) r_angle = 4; END
            IF (Oldcasex < casex) r_angle = 2; END
            IF (Oldcasey > casey) r_angle = 1; END
            IF (Oldcasey < casey) r_angle = 3; END

            IF (idcible <> 0)
            IF (casex > idcible.casex) r_angle = 4; END
            IF (casex < idcible.casex) r_angle = 2; END
            IF (casey > idcible.casey) r_angle = 1; END
            IF (casey < idcible.casey) r_angle = 3; END
            END

            //    graph = (typeunit + r_angle);

        END

        ///////////////////

        CASE 2:

            IF (idcible <> 0)
            IF (Xmapunit[idcible.casex].Ymapunit[idcible.casey] == 0)
            idcible = 0; END; END

            rapidite = rapidite - 1;

            IF (idcible == 0)
                A = casex - vision;
                LOOP
                    B = casey - vision;
                    LOOP
                        IF (A > -1) IF (B > -1) IF (A < 32) IF (B < 32) idcible = Xmapunit[A].Ymapunit[B]; END; END; END; END
                        IF (idcible <> 0) IF (idcible.etat == 1) BREAK; END; END
                        B = B + 1;
                        IF (B  == (casey + vision + 1)) BREAK; END
                    END
                    A = A + 1;
                    IF (A == (casex + vision + 1)) BREAK; END
                    IF (idcible <> 0) IF (idcible.etat == 1) BREAK; END; END
                END
            END

            IF (idcible <> 0)
                x2 = casex;
                y2 = casey;
                IF (casex < (idcible.casex-portee)) x2 = idcible.casex - portee; END
                IF (casex > (idcible.casex+portee)) x2 = idcible.casex + portee; END
                IF (casey < (idcible.casey-portee)) y2 = idcible.casey - portee; END
                IF (casey > (idcible.casey+portee)) y2 = idcible.casey + portee; END
            END

            IF (x2 <> casex or y2 <> casey)
                IF (rapidite =< 0)
                    move(ID,etat,casex,casey,x2,y2,Oldcasex,Oldcasey,vol); rapidite = rapmax;
                END;
            END

            IF (x2 == casex and y2 == casey and idcible <> 0)
                IF (idcible.etat == 1 and tir1 == 0 and rapidite =< 0) 
                    tir(ID,idcible,sort); tir1 = 1; rapidite = rapmax;
                END;
            END

            IF (Oldcasex > casex) r_angle = 4; END
            IF (Oldcasex < casex) r_angle = 2; END
            IF (Oldcasey > casey) r_angle = 1; END
            IF (Oldcasey < casey) r_angle = 3; END

            IF (idcible <> 0)
                IF (casex > idcible.casex) r_angle = 4; END
                IF (casex < idcible.casex) r_angle = 2; END
                IF (casey > idcible.casey) r_angle = 1; END
                IF (casey < idcible.casey) r_angle = 3; END
            END

            IF (Xbrou[casex].Ybrou[casey] == 1)
            //    graph = (typeunit + r_angle);
            ELSE graph = 0; END

        END

        DEFAULT:

        END

    END //switch

    Xmapunit[casex].Ymapunit[casey] = ID;

    x = ((casex - Xdepart) * 32);
    y = ((casey - Ydepart) * 32);

    FRAME;

    END //boucle

END //process

    //1566 ligne de code ! 1612 !  1373 version 0.3

//-----------------------------------------------------------------------------

PROCESS tir (idmaster, idciblet, sort);

PRIVATE

    counter;
    Oldx;
    Oldy;
    movetir;
    dommages;
    //volume du tir
    volume;

BEGIN

    idcible = idciblet;
    IF (idcible == 0) RETURN; END
    z = -500;
    IF (sort == 0)
        file = filetir;
        portee = idmaster.portee;
        casex = idmaster.casex;
        casey = idmaster.casey;
        x = (casex-Xdepart)*32+16;
        y = (casey-Ydepart)*32+16;
        Oldx = Xdepart;
        Oldy = Ydepart;
        angle = fget_angle(casex*32+16,casey*32+16,idcible.casex*32+16,idcible.casey*32+16);
        //correction angle
        IF (abs(angle) < 7000 and abs(angle) > 2000)
            IF (angle < 0) angle = -7000; END
            IF (angle > 0) angle = +7000; END
        END

        typetir = idmaster.typetir;

        volume = (200+resgraph*100) - fget_dist(x,y,x_max/2,y_max/2);

        IF (typetir == 1)  sound(sound2, volume, 256);  END //100
        IF (typetir == 2)  sound(sound2, volume, 256);  END //100
        IF (typetir == 3)  sound(sound2b, volume, 256); END //400

        movetir = 0;
        IF (casex > idcible.casex and movetir == 0) movetir = 1; idmaster.Oldcasex = casex+1; idmaster.Oldcasey = casey; END
        IF (casex < idcible.casex and movetir == 0) movetir = 1; idmaster.Oldcasex = casex-1; idmaster.Oldcasey = casey; END
        IF (casey > idcible.casey and movetir == 0) movetir = 1; idmaster.Oldcasey = casey+1; idmaster.Oldcasex = casex; END
        IF (casey < idcible.casey and movetir == 0) movetir = 1; idmaster.Oldcasey = casey-1; idmaster.Oldcasex = casex; END

    END

    IF (sort <> 0)
        graph = 0;
        IF (sort == 1 and idmaster.mana >= 150)
            IF (idcible.etat == 2)
                idcible.etat = 1;
                idcible.idcible = 0;
                idmaster.mana = idmaster.mana - 150;
            END
        END
        idmaster.sort = 0;
        idmaster.idcible = 0;
        idmaster.tir1 = 0;
        RETURN;
    END

    LOOP
        IF (Oldx <> Xdepart or Oldy <> Ydepart)
            x = x + (Oldx*32);       //-
            y = y + (Oldy*32);       //-
            x = x - (Xdepart*32);    //+
            y = y - (Ydepart*32);    //+
            Oldx = Xdepart;
            Oldy = Ydepart;
        END
        advance(4);
        counter = counter + 4;

        //peut-ˆtre mettre Ypfin + 10
        IF (y < Ypfin*32) xput(file,typetir,x,y,angle,100,0,0); END
        FRAME;

        casex = (x+(Xdepart*32))/32;
        casey = (y+(Ydepart*32))/32;
        IF (casex =< Xtaillemap and casey =< Ytaillemap and casex >= 0 and casey >= 0)
        IF (Xmapunit[casex].Ymapunit[casey] == idcible)
        //IF (collision(type unit) == idcible)
            IF (idmaster.force-idcible.armure =< 0)
                dommages = 1;
            ELSE
                dommages = idmaster.force-idcible.armure;
            END
            IF (dommages >= idcible.vie)
                idmaster.idcible = 0;
                idmaster.tuer = idmaster.tuer + 1;
            END
        idcible.vie = idcible.vie - dommages;
        idmaster.tir1 = 0; RETURN; END
        END

        IF (counter >= portee * (32+13)) idmaster.tir1 = 0; BREAK; END
    END

END

//-----------------------------------------------------------------------------

PROCESS move(idmaster, etat, casex, casey, x2, y2, Oldcasex, Oldcasey, vol);

PRIVATE

    mvt;

BEGIN

    Oldcasex = casex;
    Oldcasey = casey;

    mvt = 0;

    IF (vol == 0)

        IF (Xmapunit[x2].Ymapunit[y2] <> 0 or Xmap[x2].Ymap[y2] >= 5)
            IF (Xmapunit[x2].Ymapunit[y2] <> idmaster and vol == 0)
                casex = x2;
                casey = y2;
                x2 = Oldcasex;
                y2 = Oldcasey;

                IF (mvt == 0 and x2 < casex and y2 < casey)
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey-1] == 0 and Xmap[casex-1].Ymap[casey-1] < 5)
                    casex = casex - 1; casey = casey - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey] == 0 and Xmap[casex-1].Ymap[casey] < 5)
                    casex = casex - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey-1] == 0 and Xmap[casex].Ymap[casey-1] < 5)
                    casey = casey - 1; mvt = 1; END; END
                END

                IF (mvt == 0 and x2 == casex and y2 < casey)
                    IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey-1] == 0 and Xmap[casex].Ymap[casey-1] < 5)
                    casey = casey - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey-1] == 0 and Xmap[casex-1].Ymap[casey-1] < 5)
                    casex = casex - 1; casey = casey - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey-1] == 0 and Xmap[casex+1].Ymap[casey-1] < 5)
                    casex = casex + 1; casey = casey - 1; mvt = 1; END; END
                END

                IF (mvt == 0 and x2 > casex and y2 < casey)
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey-1] == 0 and Xmap[casex+1].Ymap[casey-1] < 5)
                    casex = casex + 1; casey = casey - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey-1] == 0 and Xmap[casex].Ymap[casey-1] < 5)
                    casey = casey - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey] == 0 and Xmap[casex+1].Ymap[casey] < 5)
                    casex = casex + 1; mvt = 1; END; END
                END

                IF (mvt == 0 and x2 > casex and y2 == casey)
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey] == 0 and Xmap[casex+1].Ymap[casey] < 5)
                    casex = casex + 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey-1] == 0 and Xmap[casex+1].Ymap[casey-1] < 5)
                    casex = casex + 1; casey = casey - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey+1] == 0 and Xmap[casex+1].Ymap[casey+1] < 5)
                    casex = casex + 1; casey = casey + 1; mvt = 1; END; END
                END

                IF (mvt == 0 and x2 > casex and y2 > casey)
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey+1] == 0 and Xmap[casex+1].Ymap[casey+1] < 5)
                    casex = casex + 1; casey = casey + 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey+1] == 0 and Xmap[casex].Ymap[casey+1] < 5)
                    casey = casey + 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey] == 0 and Xmap[casex+1].Ymap[casey] < 5)
                    casex = casex + 1; mvt = 1; END; END
                END

                IF (mvt == 0 and x2 == casex and y2 > casey)
                    IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey+1] == 0 and Xmap[casex].Ymap[casey+1] < 5)
                    casey = casey + 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey+1] == 0 and Xmap[casex-1].Ymap[casey+1] < 5)
                    casex = casex - 1; casey = casey + 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey+1] == 0 and Xmap[casex+1].Ymap[casey+1] < 5)
                    casex = casex + 1; casey = casey + 1; mvt = 1; END; END
                END

                IF (mvt == 0 and x2 < casex and y2 > casey)
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey+1] == 0 and Xmap[casex-1].Ymap[casey+1] < 5)
                    casex = casex - 1; casey = casey + 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey+1] == 0 and Xmap[casex].Ymap[casey+1] < 5)
                    casey = casey + 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey] == 0 and Xmap[casex-1].Ymap[casey] < 5)
                    casex = casex - 1; mvt = 1; END; END
                END

                IF (mvt == 0 and x2 < casex and y2 == casey)
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey] == 0 and Xmap[casex-1].Ymap[casey] < 5)
                    casex = casex - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey-1] == 0 and Xmap[casex-1].Ymap[casey-1] < 5)
                    casex = casex - 1; casey = casey - 1; mvt = 1; END; END
                    IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey+1] == 0 and Xmap[casex-1].Ymap[casey+1] < 5)
                    casex = casex - 1; casey = casey + 1; mvt = 1; END; END
                END

                x2 = casex;
                y2 = casey;
                casex = Oldcasex;
                casey = Oldcasey;
            END; 
        END
    END

    mvt = 0;

    IF (vol == 0)

        IF (mvt == 0 and x2 < casex and y2 < casey)
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey-1] == 0 and Xmap[casex-1].Ymap[casey-1] < 5)
            casex = casex - 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey] == 0 and Xmap[casex-1].Ymap[casey] < 5)
            casex = casex - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey-1] == 0 and Xmap[casex].Ymap[casey-1] < 5)
            casey = casey - 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 == casex and y2 < casey)
            IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey-1] == 0 and Xmap[casex].Ymap[casey-1] < 5)
            casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey-1] == 0 and Xmap[casex-1].Ymap[casey-1] < 5)
            casex = casex - 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey-1] == 0 and Xmap[casex+1].Ymap[casey-1] < 5)
            casex = casex + 1; casey = casey - 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 > casex and y2 < casey)
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey-1] == 0 and Xmap[casex+1].Ymap[casey-1] < 5)
            casex = casex + 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey-1] == 0 and Xmap[casex].Ymap[casey-1] < 5)
            casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey] == 0 and Xmap[casex+1].Ymap[casey] < 5)
            casex = casex + 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 > casex and y2 == casey)
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey] == 0 and Xmap[casex+1].Ymap[casey] < 5)
            casex = casex + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey-1] == 0 and Xmap[casex+1].Ymap[casey-1] < 5)
            casex = casex + 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey+1] == 0 and Xmap[casex+1].Ymap[casey+1] < 5)
            casex = casex + 1; casey = casey + 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 > casex and y2 > casey)
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey+1] == 0 and Xmap[casex+1].Ymap[casey+1] < 5)
            casex = casex + 1; casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey+1] == 0 and Xmap[casex].Ymap[casey+1] < 5)
            casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey] == 0 and Xmap[casex+1].Ymap[casey] < 5)
            casex = casex + 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 == casex and y2 > casey)
            IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey+1] == 0 and Xmap[casex].Ymap[casey+1] < 5)
            casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey+1] == 0 and Xmap[casex-1].Ymap[casey+1] < 5)
            casex = casex - 1; casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex+1].Ymapunit[casey+1] == 0 and Xmap[casex+1].Ymap[casey+1] < 5)
            casex = casex + 1; casey = casey + 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 < casex and y2 > casey)
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey+1] == 0 and Xmap[casex-1].Ymap[casey+1] < 5)
            casex = casex - 1; casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex].Ymapunit[casey+1] == 0 and Xmap[casex].Ymap[casey+1] < 5)
            casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey] == 0 and Xmap[casex-1].Ymap[casey] < 5)
            casex = casex - 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 < casex and y2 == casey)
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey] == 0 and Xmap[casex-1].Ymap[casey] < 5)
            casex = casex - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey-1] == 0 and Xmap[casex-1].Ymap[casey-1] < 5)
            casex = casex - 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xmapunit[casex-1].Ymapunit[casey+1] == 0 and Xmap[casex-1].Ymap[casey+1] < 5)
            casex = casex - 1; casey = casey + 1; mvt = 1; END; END
        END

    END

    IF (vol == 1)

        IF (mvt == 0 and x2 < casex and y2 < casey)
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey-1] == 0)
            casex = casex - 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey] == 0)
            casex = casex - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex].Yplan2[casey-1] == 0)
            casey = casey - 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 == casex and y2 < casey)
            IF (mvt == 0) IF (Xplan2[casex].Yplan2[casey-1] == 0)
            casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey-1] == 0)
            casex = casex - 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey-1] == 0)
            casex = casex + 1; casey = casey - 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 > casex and y2 < casey)
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey-1] == 0)
            casex = casex + 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex].Yplan2[casey-1] == 0)
            casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey] == 0)
            casex = casex + 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 > casex and y2 == casey)
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey] == 0)
            casex = casex + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey-1] == 0)
            casex = casex + 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey+1] == 0)
            casex = casex + 1; casey = casey + 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 > casex and y2 > casey)
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey+1] == 0)
            casex = casex + 1; casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex].Yplan2[casey+1] == 0)
            casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey] == 0)
            casex = casex + 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 == casex and y2 > casey)
            IF (mvt == 0) IF (Xplan2[casex].Yplan2[casey+1] == 0)
            casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey+1] == 0)
            casex = casex - 1; casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex+1].Yplan2[casey+1] == 0)
            casex = casex + 1; casey = casey + 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 < casex and y2 > casey)
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey+1] == 0)
            casex = casex - 1; casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex].Yplan2[casey+1] == 0)
            casey = casey + 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey] == 0)
            casex = casex - 1; mvt = 1; END; END
        END

        IF (mvt == 0 and x2 < casex and y2 == casey)
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey] == 0)
            casex = casex - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey-1] == 0)
            casex = casex - 1; casey = casey - 1; mvt = 1; END; END
            IF (mvt == 0) IF (Xplan2[casex-1].Yplan2[casey+1] == 0)
            casex = casex - 1; casey = casey + 1; mvt = 1; END; END
        END

    END

    idmaster.casex = casex;
    idmaster.casey = casey;
    idmaster.x2 = x2;
    idmaster.y2 = y2;
    idmaster.Oldcasex = Oldcasex;
    idmaster.Oldcasey = Oldcasey;

END

//-----------------------------------------------------------------------------

PROCESS trigger(condition1, condition2, condition3, consequence1)

PRIVATE

    okcondition0;
    condition0;
    okcondition[2];
    condition[2];
    A;
    B;
    C;
    D;

BEGIN

    condition[0] = condition1;
    condition[1] = condition2;
    condition[2] = condition3;

    IF (condition[1] == 0) okcondition[1] = 1; okcondition[2] = 1; END
    IF (condition[2] == 0) okcondition[2] = 1; END

    LOOP
        FRAME;
        A = A + 1;
        IF (A == 100) BREAK; END
    END

    D = -1;
    LOOP
        D = D + 1;
        condition0 = condition[D];
        LOOP

            IF (condition0 == 1)
                IF (player[1] == 0) okcondition0 = 1; END
            END

            IF (condition0 == 2)
                IF (player[2] == 0) okcondition0 = 1; END
            END

            IF (condition0 == 3)
                IF (player[0] == 0) okcondition0 = 1; END
            END

            IF (okcondition0 == 1) BREAK; END
            FRAME;
        END
    okcondition[D]=okcondition0;   //=1
    okcondition0 = 0;
    IF (okcondition[0] == 1 and okcondition[1] == 1 and okcondition[2] == 1)
    BREAK; END

    END

    LOOP
        okcondition0 = okcondition0 + 1;
        FRAME;
        IF (okcondition0 == 100) BREAK; END
    END

    IF (consequence1 == 1) retourmenu(2,4); RETURN; END
    IF (consequence1 == 2) retourmenu(3,4); RETURN; END

END

//-----------------------------------------------------------------------------
