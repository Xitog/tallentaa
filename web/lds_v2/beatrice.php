<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>Beatrice</title>
        <link rel="stylesheet" type="text/css" href="web5.css" />
    </head>
    <body>
    <table width="100%" height="100%"><tr height="10%"><td></td></tr><tr height="80%"><td align="center" valign="center">
        <div class="main">
        <span></span>
        <table class="invisible"><tr><td align="left"><h1>Beatrice</h1><td align="right"><img src="beatrice.png" height="60" width="60"/></td></tr></table>
        <hr/>
        <table class="inside">
            <tr>
                <td class="menu">
                    <ul>
                        <li><a href="index.php">News</a></li>
                        <li><a href="beatrice.php">Beatrice</a></li>
                        <li><a href="scriptal.php">Scriptal</a></li>
                        <li><a href="about.php">A propos</a></li>
                </td>
                <td class="middle">
                    <div class="invisible" align="center"><p class="date">Tems > Indicatif > Présent</p></div>
                    <?php
                        $db = mysql_connect("sql.free.fr", "looking.dwarf", "");
                        if(!$db) die("error");
                        mysql_select_db("looking.dwarf", $db);
                        mysql_query("SET NAMES UTF8"); 
                        $requete = "select ID, TITLE, CONTENT from x_test where ID = 1";
                        if (($resultat = mysql_query($requete,$db)))
                        {
                            $r = mysql_num_rows($resultat);
                            if ($r == 1)
                            {
                                $arr = mysql_fetch_assoc ($resultat);
                                //var_dump($arr);
                                echo "<h3>" . $arr["TITLE"] . "</h3>";
                                echo $arr["CONTENT"];
                            }
                        }
                    ?>
                </td>
                <td class="left">
                    <div class="invisible" style="border: 1px dotted black; background-color: #F9FAED;"> <!--EFEFEF-->
                        <p class="rubrique">Dernières nouvelles</p>
                        <ul class="rubrique">
                            <li>>> <a href="">22 Janvier 2012</a></li>
                        </ul>
                    </div>
                    <p class="text">Hello you! I'm here! Yes, right here! Welcome my old friend to this website. It's a test you know. Because I don't want to bother you with more, let's have some code!</p>
                    <p class="code">&nbsp;<span class="k">if</span> a == 5 <span class="k">then</span><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;println(a)<br/><span class="k">&nbsp;end</span></p>
                    <div class="invisible" style="border: 1px dotted black; background-color: #F9FAED;"> <!--EFEFEF-->
                        <p class="rubrique">Verbes essentiels</p>
                        <ul class="rubrique">
                            <li><a href="">avoir</a></li>
                            <li><a href="">être</a></li>
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
