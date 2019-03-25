<?php
include('part_head.php');
include('part_menu_left.php');
?>

<?php

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
                                                    <b>Create a Pattern</b> 
                                                </td> 
                                                <td class="slink10"><img src="pix.gif" height="1" width="1" /></td> 
                                            </tr>
                                            <tr>
                                                <td class="slink7">                                                
                                                <?php

                                                f_connect();

                                                if (!isset($_SESSION['pat'])) { $_SESSION['pat'] = (array) null; }

//-----------------------------------------------------------------------------

                                                if ($_GET['type'] == 'specific' and !isset($_GET['id'])) {
                                                    echo 'Please, choose from which generic pattern you would like to make a specific one:';
                                                    echo '<center><SELECT NAME="selectpattern" id="selectpattern" style="font-size:11px;font-family:arial;width:100%;border-width:1px;border-style:solid;border-color:#ffffff" onchange="document.location.href=this.options[this.selectedIndex].value;">';
                                                    echo '<OPTION style="" Value="" selected="selected">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Select a Pattern</option>';
                                                    $gen_patterns = f_list_patterns('generic');
                                                    foreach($gen_patterns as $p) {
                                                     echo '<option value="index.php?action=new&type=specific&id=' . $p["id"] . '">' . $p["Pattern Name"] . '</option>';
                                                    }
                                                    echo '</select></center>';

//-----------------------------------------------------------------------------

                                                } else if ($_GET['type'] == 'specific' and isset($_GET['id'])) {
                                                    echo '<form id="fx" name="pattern" action="index.php?action=new&type='.$_GET['type'].'&msg=created" method="post">';
                                                    echo '<div id="container">';                                                    
    
    $tbl_id_val = 1;

    function print_cat($cat) {
        global $tbl_id_val;
        
        $name = $cat['name'];

        $fields = f_get_fields_def($_GET['id'], $name);
        $daughters = f_get_daughters($name);

        if ($fields or $daughters) {
            echo '<table id="'. ($tbl_id_val++) .'" border="0" width="100%">';
            
            foreach($fields as $f) {
                if ($f['field_gof']) { $goffy = '@gof'; } else { $goffy = ''; }
                if ($f['field_comment']) { $info = '<span>' . $f['field_comment'] . '</span>'; } else { $info = ''; }
                echo '<tr>'; // 18h18 intuition 18h19 : C BON !!!! TJS FERMER LES FORMS (16h43) ET DONNER UN ID AUX INPUTS !!!!!!!!!!!!!!!!!!!
                echo '<td align="left" class="slink7"><a href="#" class="pop"><u>' . $f['field_name'] . $goffy . '</u>' . $info . '</a> : ' . '</td><td align="right"><input id="_'.$f['field_id'].'" size="40" type="text" name="qsdfghjklm' . $f['field_id'] . '" />' . '</td>';
                echo '</tr>';
            }
            
            $daughters = f_get_daughters($name);
            if (count($daughters) == 0 and count($fields) == 0) {
                // Fin récursion echo '<p><i>No fields in this category for this pattern.</i></p>';
            } else {
                foreach($daughters as $d) {
                    if (count($fields)>0) { echo '<hr/>'; }
                    $ff = f_get_fields_def($_GET['id'], $d['name']);
                    if (count($ff) > 0) { echo '<tr><td colspan="2" class="slink7">'.$d['name'].'</td><tr>'; }
                    foreach ($ff as $aff) {
                        if ($f['field_gof']) { $goffy = '@gof'; } else { $goffy = ''; }
                        echo '<tr>';
                        echo '<td align="left" class="slink7"><u>' . $aff['field_name'] . $goffy . '</u> : ' . '</td><td align="right"><input id="_'.$aff['field_id'].'" size="40" type="text" name="qsdfghjklm' . $aff['field_id'] . '" />' . '</td>';
                        echo '</tr>';
                    }
                    //echo '<tr><td>'.$d['name'].'</td><td><input id="666" name="pipo"/></td></tr>'; 18H38 LIMITE A UNE SOUS CAT. OK OK OK
                    //print_cat($d); C'est la récursion qui fait planter le bouzin. 18h33. OK.      
                }
            }
            
            echo '</table>';
            echo "\n";
        }
        
    }

    $categories = f_get_mothers();
    $cur = 'None';
    $i = 0;
    foreach($categories as $cat) {
        $name = $cat['name'];
        $order = $cat['order'];

        if ($cat['comment']) { $info = '<span>' . $cat['comment'] . '</span>'; } else { $info = ''; }

        if ($name == $cur or $cur == 'None') {
            echo '<a href="#" id="_' . $order . '" class="current" onclick="multiClass(this.id)" alt="menu' . $order . '">' . $name . $info . '</a>';
            $cur = 'Done';
        } else {
             echo '<a href="#" id="_' . $order . '" class="ghost" onclick="multiClass(this.id)" alt="menu' . $order . '">' . $name . $info . '</a>';
        }
        if ($i < count($categories)-1) { 
            echo ' | '; 
            $i = $i + 1; 
        }
    }

    $cur = 'None';
    foreach($categories as $cat) {
        $name = $cat['name'];
        $order = $cat['order'];
        
        if ($name == $cur or $cur == 'None') {
            echo '<div id="menu_' . $order . '" class="on content">';
            $cur = 'Done';
        } else {
            echo '<div id="menu_' . $order . '" class="off content">';
        }
        
        print_cat($cat);

        echo '</div>';
    }

        // 18h18 : j'y ai cru...
        echo '</div>'; //17h17
        echo '<br/>&nbsp;<br/>'; // 16h44
        echo '<div id="placement"></div>';
        echo '<table width="100%"><tr>';
        echo '<td align="left"><input type="button" value="Add another field" onClick="addInput(\'placement\');"></td>'; 
        echo '<td align="right"><input type="submit" value="Submit Pattern"/></td></tr></table>';
        echo '<input type="hidden" name="father" value="' . $_GET['id'] . '"/>';
        echo '<input type="hidden" name="msg" value="created"/>';
        echo '</form>';

//-----------------------------------------------------------------------------

                                                } else if ($_GET['type'] == 'generic') {

        echo '<form id="fx" name="pattern" action="index.php?action=new&type='.$_GET['type'].'&msg=created" method="post">';
        echo '<div id="container">';
        echo '</div>';
        echo '<table>';
        echo '<tr>';
        echo '<td align="left" class="slink7"><a href="#" class="pop"><u>Pattern Name</u></a> : </td>';
        echo '<td align="right"><input id="_5" size="40" type="text" name="qsdfghjklm5" /></td>';
        echo '</tr><tr>';
        echo '<td align="left" class="slink7"><a href="#" class="pop"><u>Publisher Identity</u></a> : </td>';
        echo '<td align="right"><input id="_1" size="40" type="text" name="qsdfghjklm1" /></td>';   
        echo '</tr>';
        echo '</table>';
        echo '<br/>&nbsp;<br/>';
        echo '<div id="placement"></div>';
        echo '<hr>';
        echo '<div id="placement2"></div>';
        echo '<br/>';
        echo '<center><input type="button" value="Add a signature field" onClick="addInput2(\'placement2\');"></center>';
        echo '<br/>';
        echo '<table width="100%"><tr>';
        echo '<td align="left"><input type="button" value="Add another field" onClick="addInput(\'placement\');"></td>'; 
        echo '<td align="right"><input type="submit" value="Submit Pattern"/></td></tr></table>';
        $_GET['id'] = 0;        
        echo '<input type="hidden" name="father" value="' . $_GET['id'] . '"/>';
        echo '<input type="hidden" name="msg" value="created"/>';
        echo '</form>';

                                                }
                                                ?>
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
        </tr>
    </table>
</td>

<?php
include('part_end.php');
?>

