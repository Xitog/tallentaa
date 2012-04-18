<?php

function test_connexion() {
    $connexion = mysql_connect (***);
    if (!$connexion) {
        die('Erreur à la connexion : ' . mysql_error());
    }
    echo 'Connecté<br>';

    $db = mysql_select_db('ran_db', $connexion);
    if (!$db) {
        die ('Erreur à la sélection : ' . mysql_error());
    }
    echo 'Sélection<br>';

    $r = mysql_set_charset('utf8', $connexion); 
    if (!$r)
    {
        die('Erreur à la configuration'); 
    }
    echo 'Utf8<br>';

    $result = mysql_query('SELECT `form`, `class`, `lang` FROM w_words');
    if (!$result) {
        die('Erreur requête : ' . mysql_error());
    }
    echo 'Select<br>';

    $r = mysql_num_rows($result);
    if ($r == 0) {
        die('Erreur : 0 résultat trouvé');
    } else {
        echo 'Nb de lignes retournées = ' . $r . '<br>';
    }

    echo '<table>';
    while ($row = mysql_fetch_assoc($result)) {
        echo '<tr>';
        echo '<td>' . $row["form"] . '</td>';
        echo '<td>' . $row["class"] . '</td>';
        echo '<td>' . $row["lang"] . '</td>';
        echo '</tr>';
    }
    echo '</table>';
    
    mysql_close($connexion);
}

echo '<html>
        <head>
          <meta charset="UTF-8">
          <title>Dico</title>
          <style type="text/css">
            #footer {
	          position: fixed;
	          width: 100%; 
	          left: 0;
	          bottom: 0;
              background-color: #ff0000;
	          /*background:url(images/bg-footer.gif) repeat-x left bottom;*/
              padding-top: 2px; 
              padding-bottom: 2px;
              background: #4c4c4c; /* Old browsers */
              background: -moz-linear-gradient(top, #4c4c4c 0%, #595959 12%, #666666 25%, #474747 39%, #000000 51%, #111111 60%, #2b2b2b 76%, #1c1c1c 91%, #131313 100%); /* FF3.6+ */
              background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#4c4c4c), color-stop(12%,#595959), color-stop(25%,#666666), color-stop(39%,#474747), color-stop(51%,#000000), color-stop(60%,#111111), color-stop(76%,#2b2b2b), color-stop(91%,#1c1c1c), color-stop(100%,#131313)); /* Chrome,Safari4+ */
              background: -webkit-linear-gradient(top, #4c4c4c 0%,#595959 12%,#666666 25%,#474747 39%,#000000 51%,#111111 60%,#2b2b2b 76%,#1c1c1c 91%,#131313 100%); /* Chrome10+,Safari5.1+ */
              background: -o-linear-gradient(top, #4c4c4c 0%,#595959 12%,#666666 25%,#474747 39%,#000000 51%,#111111 60%,#2b2b2b 76%,#1c1c1c 91%,#131313 100%); /* Opera 11.10+ */
              background: -ms-linear-gradient(top, #4c4c4c 0%,#595959 12%,#666666 25%,#474747 39%,#000000 51%,#111111 60%,#2b2b2b 76%,#1c1c1c 91%,#131313 100%); /* IE10+ */
              background: linear-gradient(top, #4c4c4c 0%,#595959 12%,#666666 25%,#474747 39%,#000000 51%,#111111 60%,#2b2b2b 76%,#1c1c1c 91%,#131313 100%); /* W3C */
            }
          </style>
        </head>
        <body>';
test_connexion();
echo '    <div id="footer"><center><input type="text" maxlength="30" placeholder="entrer un mot…"/> <input type="submit" value="chercher"/></center></div>';
echo '  </body>
      </html>';

?>
