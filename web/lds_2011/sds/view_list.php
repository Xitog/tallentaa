<?php
include('part_head.php');
include('part_menu_left.php');
?>

<td width="544" valign="top">

    <table width="520" border="0" bgcolor="white" align="center" cellspacing="3" cellpadding="3"> 
        <tr> 
            <td width="520" valign="top" class="body"> 
                <table border="0" bgcolor="white" cellspacing="0" cellpadding="0"> 
                    <tr> 
                        <td align="left" valign="top" width="530" class="body"> 
                            <table width="530" border="0" cellspacing="0" cellpadding="0" > 
                                <tr> 
                                    <td width="50px">&nbsp;</td> 
                                    <td class="slink7" width="95%" valign="top" align="center">	

                                        <table border="0" bgcolor="white" cellspacing="0" cellpadding="4" width="100%" align="center"> 
                                            <tr> 
                                                <td width="100%" class="slink10" bgcolor="#3BAADA" align="center"> 
                                                    <b>List of pattern</b> 
                                                </td> 
                                                <td class="slink10"><img src="pix.gif" height="1" width="1" /></td> 
                                            </tr>
                                            <tr>
                                                <td class="slink7">Here is the list of patterns with the following parameters:
                                                <ul>
                                                    <?php
                                                        echo '<li> Type : ';
                                                        if ($_GET['type'] == 'generic') {
                                                            echo 'Generic Patterns';
                                                        } else if ($_GET['type'] == 'specific') {
                                                            echo 'Specific Patterns';
                                                        }
                                                        echo '</li>';
                                                        if (isset($_GET['param'])) {
                                                            echo '<li>Searched by : ';
                                                            echo $_GET['param'];
                                                            echo '</li>';
                                                        }
                                                    ?>
                                                </ul>
                                                </td>
                                            </tr>
                                            <tr>
                                                <table border="1" width="95%" style="border-style: solid; border-width: 1px; border-color: #3BAADA;">
                                                    <tr>
                                                        <th class="slink8">Name</th>
                                                        <th class="slink8">Publisher</th>
                                                    </tr>
                                                    <?php
                                                    $patterns = (array) null;
                                                    if ($_GET['type'] == 'generic') {
                                                        $patterns = f_list_patterns('generic');
                                                    } else if ($_GET['type'] == 'specific') {
                                                        $patterns = f_list_patterns('specific');
                                                    }
                                                    // ici le tri avec http://www.php.net/manual/fr/function.array-multisort.php
                                                    if (isset($_GET['param']) and $_GET['param'] == 'alphabetical') {
                                                        // Tri alphabétique non sensible à la casse
                                                        foreach ($patterns as $key => $row) {
                                                            // On fait des tableaux de colonne ayant pour chaque valeur la même clé que l'original
                                                            $patterns_id[$key]  = $row['id'];
                                                            $patterns_name[$key] = $row['Pattern Name'];
                                                        }
                                                        // On réduit tout au lowercase pour ne pas gérer la différence min/maj
                                                        $patterns_name_lowercase = array_map('strtolower', $patterns_name);
                                                        // On multitri !
                                                        array_multisort($patterns_name_lowercase, SORT_STRING, $patterns_id, SORT_ASC, $patterns);
                                                    }
                                                    foreach($patterns as $pattern) {
                                                        echo '<tr>';
                                                        echo '<td class="slink7" style="border-style: solid; border-width: 1px; border-color: grey;">';
                                                        echo '<a href="index.php?action=view&id=' . $pattern['id'] . '">' . $pattern['Pattern Name'];
                                                        echo '</a></td>';
                                                        echo '<td class="slink7" style="border-style: solid; border-width: 1px; border-color: grey;">';
                                                        echo $pattern['Publisher Identity'];
                                                        echo '</td>';
                                                    }
                                                    ?>
                                                </table>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</td>

<?php
include('part_end.php');
?>
