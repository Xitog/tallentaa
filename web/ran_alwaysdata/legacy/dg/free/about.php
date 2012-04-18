<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>Onnellinen</title>
        <link rel="stylesheet" type="text/css" href="web5.css" />
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
                    <div class="invisible" align="center"><p class="date">Introduction</p></div>
                    <p class="text">Pour l'instant, le site est encore tout jeune et en construction, alors il n'y a pas grand chose à dire... Chantons alors !</p>
                    <p class="text" align="center">
                        <i>I'm just a little site,<br/>
                        just a little site,<br/>
                        smiling over the web.<br/>
                        </i>
                    </p>
                    <?php
                    
                    include "tools.php";
                    echo '<p class="text">Statistiques : <ul>';
                    echo '<li>Version Béatrice : 1.0.0</li>';
                    $requete = "SELECT count(*) as nb FROM chunks";
                    if ($resultat = get($requete)) {
                        $arr = mysql_fetch_assoc ($resultat);
                        $nb = $arr["nb"];
                        echo '<li>Nombres de billets : ' . $nb . '</li>';
                    }
                    $requete = "SELECT count(*) as nb FROM words";
                    if ($resultat = get($requete)) {
                        $arr = mysql_fetch_assoc ($resultat);
                        $nb = $arr["nb"];
                        echo '<li>Nombres de mots dans Béatrice : ' . $nb . '</li>';
                    }
                    echo '</ul></p>';
                    ?>
                </td>
                <td class="left">
                    <div class="invisible" style="border: 1px dotted black; background-color: #F9FAED;">
                        <p class="rubrique">Historique</p>
                        <ul class="rubrique">
                            <li>15 Fév. : Béatrice 1.0 online.</li>
                            <li>10 Fév. : fondations posées.</li>
                            <li>7 Fév. : mise en ligne avec bd.</li>
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
