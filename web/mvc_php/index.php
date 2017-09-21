<?php

//
// Normalement tu devrais avoir 3 fichiers :
// - le index.php dans lequel tu fais include model.php et inlude view.php
// - model.php dans lequel tu t'occupes des objets métiers et de la base de données avec tes requêtes SQL
// - view.php dans lequel tu t'occupes de l'HTML
// Normalement, TU NE DEVRAIS JAMAIS AVOIR de SQL et d'HTML dans ton fichier index.php
// Là, pour que ça soit plus simple, j'ai fusionné les 3 fichiers en un seul : index.php
// J'ai divisé chaque partie avec ce type de bandeau :
//

//------------------------------------------------------------------------------------
// PARTIE MODEL (M)
//------------------------------------------------------------------------------------

//
// Cette partie se charge d'interagir avec la base de données.
// En gros, elle va chercher des informations dans la base, les convertit en un bel objet PHP et s'occupe, si l'objet est modifié, de le sauvegarder dans la base à nouveau.
// On appelle ça une couche ORM : Object-relational mapping. C'est très chiant à écrire car très répétitif. Typiquement, CakePHP et Symfony2 s'occupe de ça automatiquement.
// Tu files ta classe Book écrite en PHP et hop! ils se charge de créer toutes les fonctions nécessaires.
//
// Là, j'ai fait juste un rapide prototype.
//

class Book
{
    private static $last_id = 0;

    private $id;
    private $name;
    private $author;

    public function __construct($name, $author) {
        self::$last_id += 1;
        $this->id = self::$last_id;
        $this->name = $name;
        $this->author = $author;
    }

    public function getId() {
        return $this->id;
    }

    public function getName() {
        return $this->name;
    }
    
    public function getAuthor() {
        return $this->author;
    }
     
}

//
// C'est là où le prototype est pipo. Normalement, tu devrais dans load_all_books ouvrir une connexion à ta base de données, faire un SELECT de tous les enregistrements dans la table BOOKS.
// Puis tu itères sur le résultat, tu stockes chaque enregistrement dans un nouvel objet Book PHP que tu mets dans une liste. À la fin, tu renvoies la liste.
// Là je fais juste 3 objets rapido que je réexpédie.
//
function load_all_books() {
    $b1 = new Book("Le retour des zombies", "Bob Sanplon");
    $b2 = new Book("La 9e planète", "Vincent Diesel");
    $b3 = new Book("Zembla contre Maciste", "Hercule Poirot");
    return array($b1, $b2, $b3);
}

//
// Pareil, c'est aussi du pipo ici. Normalement tu devrais faire un SELECT avec un 'WHERE ID = ' . strval($id) (tu concatènes une variable PHP qui contient un entier à une chaîne qui sera ta requête)
//
function load_book($id) {
    $b = NULL;
    if ($id === '1') {
        $b = new Book("Le retour des zombies", "Bob Sanplon");
    } elseif ($id === '2') {
        $b = new Book("La 9e planète", "Vincent Diesel");
    } elseif ($id === '3') {
        $b = new Book("Zembla contre Maciste", "Hercule Poirot");
    } else {
        die("Book not found");
    }
    return $b;
}

//
// Et voilà, normalement tu devrais avoir aussi une fonction save_book($book) qui prend un objet PHP et soit met à jour son enregistrement, soit créé un nouvel enregistrement (selon que l'id du Book existe déjà dans la table).
// Comme tu le vois, ce genre de code est très répétitif donc parfait pour être généré. En plus, tu n'es jamais à l'abri de faire une erreur stupide dans tes requêtes assemblées.
// Je te conseille de ne faire que les fonctions dont tu as besoin, tu les ajoutes au fur et à mesure.
//

//------------------------------------------------------------------------------------
// PARTIE VIEW (V)
//------------------------------------------------------------------------------------

//
// Dans cette partie, on construit nos vues, donc notre HTML.
// L'important ici, c'est les liens qui repassent tous par index.php avec des "ordres".
// Un ordre c'est un peu comme un appel de fonction, tu mets l'ordre que tu veux avec ses paramètres.
//

// Là, c'est juste une fonction pour passer les bons header HTTP et le titre dans les headers HTML
function view_header() {
    header('Content-Type: html');
    echo('<head><title>Test MVC PHP</title></head>'); 
}

// Avec cette fonction, on affiche la page d'accueil.
// À partir de là, on peut donner l'ordre d'afficher un livre (action = view, type = book, id = id du livre)
function view_home($books) {
    echo('<h1>Hello!</h1>');
    echo('<ul>');
    foreach ($books as $bo) {
        echo('<li><a href="index.php?action=view&type=book&id=' . strval($bo->getId()) . '">' . $bo->getName() . '</a> by ' . $bo->getAuthor() . '</li>');
    }
    echo('</ul>');
}

// Avec cette fonction, on affiche un livre.
// À partir de là, on peut revenir sur la page d'accueil (action = home)
function view_book($book) {
    echo('<h1>' . $book->getName() . '</h1>');
    echo('<h2>by ' . $book->getAuthor() . '</h2>');
    echo('<a href="index.php?action=home">Retourner à l\'accueil</a>');
}

//------------------------------------------------------------------------------------
// PARTIE CONTROLLER (C)
//------------------------------------------------------------------------------------

// C'est un peu comme la fonction main en C
function main_controller () {
    view_header();

    if (isset($_GET['action']) && isset($_GET['type'])) {
        $action = $_GET['action'];
        $type = $_GET['type'];
    } else { // QUAND TU N'AS AUCUNE DONNÉE GET, tu fais par défaut l'action 'home' (afficher la page d'accueil)
        $action = 'home';
        $type = '';
    }
    
    // LE NOYAU DU CONTROLLER EST ICI
    // Le controller, c'est un aiguilleur. Il comprend ton ordre, va chercher ce qu'il a besoin pour le faire, et l'affiche
    switch($action) {
        case 'home':
            $books = load_all_books(); // J'utilise la partie MODEL pour aller chercher un truc
            view_home($books);         // Que j'affiche grâce à la partie VIEW
        break;
        case 'view':
            switch($type) {
                case 'book':
                    if (isset($_GET['id'])) {
                        $id = $_GET['id'];
                        $book = load_book($id); // J'utilise la partie MODEL pour aller chercher un truc
                        view_book($book);       // Que j'affiche grâce à la partie VIEW
                    } else {
                        echo('<h1>ERROR : ACTION -VIEW- OF TYPE -BOOK- WITH NO -ID- DEFINED</h1>');
                    }   
                break;
                default:
                    echo('<h1>ERROR : TYPE UNKNOWN : ' . $type . '</h1>');
            }
        break;
        default:
            echo('<h1>ERROR : ACTION UNKNOWN : ' . $action . '</h1>');
    }
}

// Il ne faut oublier de l'appeler !
main_controller();

?>			