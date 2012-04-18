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
    if(!$db) die("error");
    mysql_select_db("damien.gouteux", $db);
    mysql_query("SET NAMES UTF8"); 
    return mysql_query($request,$db);
}

function check($var) {
    return preg_match("/[a-z_]/", $var);
}

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

?>
