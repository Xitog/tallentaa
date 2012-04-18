<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>Onnellinen</title>
        <link rel="stylesheet" type="text/css" href="web5.css" />
        <link rel="shortcut icon" href="favicon.ico" />
    </head>
    <body>
    <table width="100%" height="100%"><tr height="10%"><td></td></tr><tr height="80%"><td align="center" valign="center">
        <div class="main">
        <span></span>
        <table class="invisible"><tr><td align="left"><h1>Onnellinen</h1><td align="right"><img src="leaf_purple.png" height="60" width="60"/></td></tr></table>
        <div class="menu">- <a class="intext" href="index.php">News</a> | <a class="intext" href="beatrice.php">Beatrice</a> | <a class="intext" href="scriptal.php">Scriptal</a> | <a class="intext" href="ariane.php">Ariane</a> | <a class="intext" href="about.php">À propos</a> -</div>
        <table class="inside">
            <tr>
                <td class="menu">
                    <ul>
                        <li><a class="menu" href="index.php">News</a></li>
                        <li><a class="menu" href="beatrice.php">Beatrice</a></li>
                        <li><a class="menu" href="scriptal.php">Scriptal</a></li>
                        <li><a class="menu" href="ariane.php">Ariane</a></li>
                        <li><a class="menu" href="about.php">A propos</a></li>
                </td>
                <td class="middle">
                    <?php
                    if (!isset($_GET['content']))
                    {
                    ?>
                    <div class="invisible" align="center"><p class="date">Introduction</p></div>
                    <p class="text">Bienvenue sur ce site ! Vous y trouverez une <a class="intext" href="beatrice.php">petite grammaire italienne</a>, un <a class="intext" href="scriptal.php">langage de script expérimental</a> et quelques <a class="intext" href="ariane.php">guides</a> sur des sujets divers. Puissiez-vous y trouver quelque chose qui vous soit utile ! Aussi, je maintiens un fil tenu de nouvelles, au cas où vous voudriez lire un peu, qui se trouvent plus bas. Bonne lecture !</p>
                    <?php
                    }
                    include "tools.php";
                    
                    $list = False;
                    $catname = '';
                    $links = array();
                    $display = 'un_nouveau_depart';
                    if (isset($_GET['content']))
                    {
                        if (check($_GET['content'])) {
                            $display = $_GET['content'];
                        }
                        if (strcmp($display, "list") != 0) {
                            $requete = "SELECT id, title, content, creation FROM chunks WHERE id = '" . $display . "'";
                        } else {
                            if (isset($_GET['tag']) and check($_GET['tag'])) {
                                $list = True;
                                $requete = "SELECT label FROM tags WHERE tags.id = '" . $_GET['tag'] . "'";
                                $resultat = get($requete);
                                $temp = mysql_fetch_assoc ($resultat);
                                $catname = $temp["label"];
                                //
                                $requete = "SELECT id, title, content, creation FROM chunks, tagged WHERE tagged.id_chunk = chunks.id AND tagged.id_tag = '" . $_GET['tag'] . "'";
                            }
                        }
                    }
                    else
                        $requete = "SELECT id, title, content, creation FROM chunks WHERE project='news' ORDER BY creation DESC LIMIT 0, 3";

                    if ($resultat = get($requete))
                    {
                        $r = mysql_num_rows($resultat);
                        while ($arr = mysql_fetch_assoc ($resultat))
                        {
                            echo '<div class="invisible" align="center"><p class="date">' . fdate($arr["creation"]) . '</p></div>';
                            echo "<h2>" . $arr["title"] . "</h2>";
                            echo '<p class="text">' . $arr["content"] . '</p>';
                            $links[] = array($arr["id"], $arr["title"]. " <i>(" .  fsdate($arr["creation"]) . ")</i>"); 
                        }
                    }
                    ?>
                </td>
                <td class="left">
                    <div class="invisible" style="border: 1px dotted black; background-color: #F9FAED;">
                        <?php
                        if ($list) {
                            echo '<p class="rubrique">Catégories : ' . $catname . '</p>';
                        } else {
                            echo '<p class="rubrique">Dernières nouvelles</p>';
                        }
                        ?>
                        <ul class="rubrique">
                            <?php
                            foreach ($links as $val)
                            {
                                echo '<li><a href="index.php?content='. $val[0] .'">' . $val[1] . "</a></li>";
                            }
                            ?>
                        </ul>
                    </div>
                    <br/>
                    <div class="invisible" style="border: 1px dotted black; background-color: #F9FAED;">
                        <p class="rubrique">Catégories</p>
                        <ul class="rubrique">
                            <?php
                            $requete = "SELECT id, label, count(*) as nb FROM tags, tagged WHERE tagged.id_tag = tags.id GROUP BY tags.id, tags.label";
                            if ($resultat = get($requete))
                            {
                                $r = mysql_num_rows($resultat);
                                while ($arr = mysql_fetch_assoc ($resultat))
                                {
                                    echo '<li><a href="index.php?content=list&tag='. $arr['id'] .'">' . $arr['label'] . " <i>(" . $arr['nb'] . ")</i></a></li>";
                                }
                            }
                            ?>
                        </ul>
                    </div>
                </td>
            </tr>
        </table>
        </div>
        <p class="footer">Damien Gouteux, 2012</p>
    </td><tr width="10%"><td></td></tr></table>
    </body>
</html>
