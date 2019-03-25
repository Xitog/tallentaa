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
                                                    <b>View a Pattern</b> 
                                                </td> 
                                                <td class="slink10"><img src="pix.gif" height="1" width="1" /></td> 
                                            </tr>
                                            <tr>
                                                <td class="slink7">
                                                    This is the pattern you requested. It has the following predefined parameters:
                                                    <ul>
                                                        <li>Id : <?=$_GET['id']?></li>
                                                    </ul>
                                                    <!--Here you can see a detailed description of this pattern:<br/>-->
                                                </td>
                                            </tr>
                                            <tr><td><hr/></td></tr>
                                            <tr><td>
<table align="left" style="font-family: arial; font-size: 11px; color: black;">
<tr>
<td>

<div id="container">
<?php

    function print_cat($cat) {
        echo '<table width="100%">';
        $name = $cat['name'];

        $fields = f_get_fields($_GET['id'], $name);
        foreach($fields as $f) {
            if ($f['field_gof']) { $goffy = '@gof'; } else { $goffy = ''; }
            echo '<tr><td align="left" class="slink7"><u>' . $f['field_name'] . $goffy . '</u> : </td><td align="left" class="slink7">' . $f['field_value'] . '</td></tr>';
        }

        $daughters = f_get_daughters($name);
        if (count($daughters) == 0 and count($fields) == 0) {
            // Fin récursion echo '<p><i>No fields in this category for this pattern.</i></p>';
        } else {
            //foreach($daughters as $d) {
                //if (count($fields)>0) { echo '<hr/>'; }
                //print_cat($d);       
            //}
        }
        echo '</table>';
    }

    $categories = f_get_mothers();
    $cur = 'None';
    $i = 0;
    foreach($categories as $cat) {
        $name = $cat['name'];
        $order = $cat['order'];

        if ($name == $cur or $cur == 'None') {
            echo '<a href="#" id="_' . $order . '" class="current" onclick="multiClass(this.id)" alt="menu' . $order . '">' . $name . '</a>';
            $cur = 'Done';
        } else {
             echo '<a href="#" id="_' . $order . '" class="ghost" onclick="multiClass(this.id)" alt="menu' . $order . '">' . $name . '</a>';
        }
        if ($i < count($categories)-1) { 
            echo ' | '; 
            $i = $i + 1; 
        }
    }
    echo '<br/><br/>';

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

        // Il reste un truc : les categories filles. En recursif !!!
        // Puis après les champs dynamiques. Mais ça va marcher !!!
        //echo '<h1>' . $name . '</h1>';
        //echo '<p>' . $name . '<p>';

        echo '</div>';
    }

    if (f_is_gen($_GET['id'])) {
        echo '<div>';
        //echo '<hr/>';
        echo '<p class="slink7" align="center"><u>Element defined for future specific patterns:</u></p>';
        echo '<table width="100%">';
        $categories = f_get_mothers();
        foreach($categories as $cat) {
            $fields = f_get_fields_def($_GET['id'], $cat['name']);
            foreach($fields as $f) {
                if ($f['field_gof']) { $goffy = '@gof'; } else { $goffy = ''; }
            echo '<tr class="slink7"><td width="10%">&nbsp;</td><td align="left"><u>' . $f['field_name'] . $goffy . '</u>' . '</td><td align="right">'.$cat['name'].'</td></tr>';
            }
        }
        echo '</table></div>';
    }
?>

</div>
</td>
</tr>
</table>
<!--
                                                <table border="1" width="95%" style="border-style: solid; border-width: 1px; border-color: #3BAADA;">
                                                    <tr>
                                                        <th class="slink8">Field</th>
                                                        <th class="slink8">Value</th>
                                                        <th class="slink8">Type</th>
                                                        <th class="slink8">@ gof</th>
                                                        <th class="slink8">Category</th> --><!-- innermost --><!--
                                                    </tr>
                                                    <?php
                                                        $pattern = f_view_pattern($_GET['id']);
                                                        foreach ($pattern as $field) {
                                                            echo '<tr class="slink7">';
                                                            echo '<td>' . $field['field_name'] . '</td>';
                                                            echo '<td>' . $field['field_value'] . '</td>';
                                                            echo '<td>' . $field['field_type'] . '</td>';
                                                            echo '<td>' . $field['field_gof'] . '</td>';
                                                            echo '<td>' . $field['innermost_category'] . '</td>';
                                                            echo '</tr>';
                                                        }
                                                    ?>
                                            </tr>
                                        </table>-->
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
