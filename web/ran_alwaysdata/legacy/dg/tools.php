<?php

function fdate($date) {
    setlocale (LC_TIME, 'fr_FR.utf8','fra');
    return ucwords(strftime("%A %e %B %Y",strtotime($date)));
}

function fsdate($date) {
    setlocale (LC_TIME, 'fr_FR.utf8','fra');
    return strftime("%d/%m/%y",strtotime($date));
}

function get($request) {
    $db = mysql_connect("*******", "*******", "*******"); 
    if(!$db) die ('Erreur à la connexion : ' . mysql_error());
    mysql_select_db("ran_db", $db);   
    mysql_query("SET NAMES UTF8");
    $r = mysql_query($request,$db);
    if (!$r) die ('Erreur à la requête : ' . mysql_error() . '<br>' . $request);
    return $r;
}

function check($var) {
    return preg_match("/[a-z_]/", $var);
}

/*
function fword_it($w, $c, $m) {
    $r = $w . ' <span class="typ">' . $c . '</span>';
    if (strcmp($c, "nom") == 0) {
        $vowels = array("a","e","i","o","u");
        $is_voy = False;
        if (in_array($w[0], $vowels, True)) {
            $is_voy = True;
        }
        if (strcmp($m, "m_sg") == 0 or $m[0] === "m") {
            if ($is_voy) {
                $r = "l'". $r;
            } else if (strcmp(substr($w,0,2), "sc") == 0 or $w[0] === "z") {
                $r = "lo " . $r;
            } else {
                $r = "il " . $r;
            }
            if ($m[3] === "i")
                $r = $r . ' <span class="typ">masculin invariable</span>';
            else
                $r = $r . ' <span class="typ">masculin</span>';
        } else if (strcmp($m, "f_sg") == 0  or $m[0] === "f") {
            if ($is_voy) {
                $r = "l'". $r;
            } else {
                $r = "la " . $r;
            }
            if ($m[3] === "i")
                $r = $r . ' <span class="typ">féminin invariable</span>';
            else
                $r = $r . ' <span class="typ">féminin</span>';
        }
    } else if (strcmp($c, "adjectif") == 0) {
        $r = $w . ' <span class="typ">adj. qual.</span>';
        if (strcmp($m, "inv") != 0) {
            if (strcmp($w[strlen($w)-1], "o") == 0) {
                $r = $w . ', ' . substr($w, 0, strlen($w)-1). 'a <span class="typ">adj. qual.</span>';
            }
        } else {
            $r = $w . ' <span class="typ">adj. qual. inv.</span>';
        }
    }
    return $r;
}
*/

/* V2 */

function fword_it($form, $class)
{
    return $form . ' <span class="typ">' . $class . "</span>";
}

function get_word_extended($form, $lang, $class)
{
    if ($class == 'adjectif') {
        $requete = "SELECT `form`, `lang`, `m_sg`, `f_sg`, `m_pl`, `f_pl`, `inv`
                    FROM w_words_adjectives
                    WHERE `form` = '" . $form . "' AND `lang` = '" . $lang . "'";

        $resultat = get($requete);
        $r2 = mysql_fetch_assoc ($resultat);
        return $r2;

    } elseif ($class == 'verbe') {
        $requete = "SELECT `form`, `lang`, `transitivity`, `present`, `past`, `future`, `conditional`, `subjunctive`
                    FROM w_words_verbs
                    WHERE `form` = '" . $form . "' AND `lang` = '" . $lang . "'";
                        
        $resultat = get($requete);
        $r2 = mysql_fetch_assoc ($resultat);
        return $r2;

    } elseif ($class == 'nom') {
        $requete = "SELECT `form`, `lang`, `gender`, `number`, `invariable`, `plural`
                    FROM w_words_nouns
                    WHERE `form` = '" . $form . "' AND `lang` = '" . $lang . "'";

        $resultat = get($requete);
        $r2 = mysql_fetch_assoc ($resultat);
        return $r2;
    } else {
        return array();
    }
}

function get_word_simple($form, $lang)
{
     $requete = "SELECT `form`, `class`, `lang`, `tag`, `subtag`, `order`, `meaning`  
                 FROM w_words WHERE `lang` = '" . $lang . "' AND `form` = '" . $form . "' 
                 ORDER BY `subtag` ASC, `order` ASC, `class` ASC";

    $resultat = get($requete);

    if (!$resultat) {
        die ('Erreur à la requête : ' . mysql_error() . '<br>' . $requete);
    } elseif (mysql_num_rows($resultat) > 1) {
        die ('Multiples résultats');
    } else {
        $r1 = mysql_fetch_assoc ($resultat);
        return $r1;
    }
}

function get_word($form, $lang)
{
    $r1 = get_word_simple($form, $lang);
    $r2 = get_word_extended($form, $lang, $r1['class']);
    //var_dump($r1);
    //echo '<hr>';
    //var_dump($r2);
    return $r1 + $r2;
}

function get_words($tag, $lang) // By tag
{
     $requete = "SELECT `form`, `class`, `lang`, `tag`, `subtag`, `order`, `meaning` 
                 FROM w_words WHERE `lang` = '" . $lang . "' AND `tag` = '" . $tag . "' 
                 ORDER BY `subtag` ASC, `order` ASC, `class` ASC";

    $resultat = get($requete);

    if (!$resultat) {
        die ('Erreur à la requête : ' . mysql_error() . '<br>' . $requete);
    } else {
        $all = array();
        while ($r1 = mysql_fetch_assoc ($resultat)) {
            $r2 = get_word_extended($r1['form'], $lang, $r1['class']);
            //var_dump($r1);
            //echo '<hr>';
            //var_dump($r2);
            $all[] = $r1 + $r2;
        }
        return $all;
    }
}

function get_words_by_form($form, $lang) // By form
{
     $requete = "SELECT `form`, `class`, `lang`, `tag`, `subtag`, `order`, `meaning` 
                 FROM w_words WHERE `lang` = '" . $lang . "' AND `form` = '" . $form . "' 
                 ORDER BY `subtag` ASC, `order` ASC, `class` ASC";

    $resultat = get($requete);

    if (!$resultat) {
        die ('Erreur à la requête : ' . mysql_error() . '<br>' . $requete);
    } else {
        $all = array();
        while ($r1 = mysql_fetch_assoc ($resultat)) {
            $r2 = get_word_extended($r1['form'], $lang, $r1['class']);
            $all[] = $r1 + $r2;
        }
        return $all;
    }
}

function test()
{
    $r = get_word('grande', 'it');
    var_dump($r);
    echo '<br><br><br>';
    $r = get_words('couleurs', 'it');
    var_dump($r);
}

//test();

?>
