<?php

//-----------------------------------------------------------------------------

function f_control($action = 'home', $ignore_get = False) {

    if (!isset($_SESSION['user'])) {
        f_init();
    }

    if (isset($_GET['action']) and !$ignore_get) {
        $action = $_GET['action'];
    }

    switch($action) {
        case 'home':
            f_control_home();
            break;
        case 'committee':
            f_control_committee();
            break;
        case 'list':
            f_control_list();
            break;
        case 'view':
            f_control_view();
            break;
        case 'new':
            f_control_new();
            break;
        default:
            f_control_home();
            echo 'Action unknown. Dumping parameters:<br/>';            
            foreach($_GET as $key => $value) {
                echo $key . ' : ' . $value . '<br>';  
            }
            //f_error('ACTION UNKNOWN');
            break;
    }
}

//-----------------------------------------------------------------------------

function f_control_new() {
    f_connect();
    //var_dump($_GET);
    //var_dump($_POST);
    if(isset($_POST['msg'])) {
        if ($_POST['msg'] == 'created') {
            /*
            echo '<table>';
            foreach($_POST as $k => $v) {
                echo '<tr><td>' . $k . '</td><td>' . $v . '</td></tr>' ;
            }
            echo '</table>';
            echo '<br/>';
            if (isset($_POST["myFields"])) { var_dump($_POST["myFields"]); } else { echo "myFields is not set<br/>"; }
            if (isset($_POST["myValues"])) { var_dump($_POST["myValues"]); } else { echo "myValues is not set<br/>"; }
            die('end');
            */

            $idp = intval(f_get_max_id_pattern()) + 1;
            $type = $_GET['type'];
            $id_pattern_def = $_POST['father'];
            $req = 'INSERT INTO sds_patterns VALUES ('. $idp .','. $id_pattern_def .",'". $type ."')";
            $result = f_request($req);
            if ($result) {
                foreach($_POST as $key => $field) {
                    $pos = strpos($key, "sdfghjklm");
                    //if (is_int($pos)) { echo '<br/>' . substr($key, $pos+9) ; }
                    //continue;
                    if (is_int($pos)) {
                        $k = substr($key, $pos+9);
                        //echo '>> ' . $k . ' : ' . $field . '<br/>';
                        $req = 'INSERT INTO sds_patterns_fields (id_pattern,id_field_def,value) values ('.$idp.','.intval($k).",'".$field."')";
                        $result = f_request($req);
                    }
                }
                // Champs dynamiques
                if (isset($_POST["myFields"])) {
                    $myFields = $_POST["myFields"];
                    $myValues = $_POST["myValues"];
                    $catego = $_POST["myCategory"];
                    $i = 0;
                    while ($i < count($myFields)) {
                        $field = $myFields[$i];
                        $value = $myValues[$i];
                        $idf = intval(f_get_max_fields_def()) + 1;
                        $req = "INSERT INTO sds_fields_def (id, ref_category, name, type, gof) VALUES (".$idf.",'".$catego."','".$field."','string', 0)";
                        $result = f_request($req);
                        $req = "INSERT INTO sds_patterns_fields (id_pattern, id_field_def,value) values (".$idp.",".$idf.",'".$value."')";
                        $result = f_request($req);
                        $i++;
                    }
                }
                // Champs dynamiques des patterns génériques BROUILLON PAS DE GOF GERE
                $req = "INSERT INTO sds_patterns_def_fields (id_pattern_def, id_field_def, obligatoire) values (".$idp.",1,1)";
                $result = f_request($req);
                $req = "INSERT INTO sds_patterns_def_fields (id_pattern_def, id_field_def, obligatoire) values (".$idp.",5,1)";
                $result = f_request($req);
                //
                if (isset($_POST['father']) and $_POST['father'] == 0) {
                    $sigFields = $_POST["sigFields"];
                    $sigCategories = $_POST["sigCategories"];
                    $sigTypes = $_POST["sigTypes"];
                    $sigMandatories = $_POST["sigMandatories"];
                    $i = 0;
                    while ($i < count($sigFields)) {
                        $idf = intval(f_get_max_fields_def()) + 1;
                        $fld = $sigFields[$i];
                        $cat = $sigCategories[$i];
                        $typ = $sigTypes[$i];
                        $man = $sigMandatories[$i];
                        $req = "INSERT INTO sds_fields_def (id, ref_category, name, type, gof) VALUES (".$idf.",'".$cat."','".$fld."','".$typ."', 0)";
                        $result = f_request($req);
                        $req = "INSERT INTO sds_patterns_def_fields (id_pattern_def, id_field_def, obligatoire) values (".$idp.",".$idf.",".$man.")";
                        $result = f_request($req);
                        $i++;
                    }
                }
            }
            f_control('home', True);
        }
    } else {
        include('view_new.php');
    }
}

//-----------------------------------------------------------------------------

function f_control_view() {
    f_connect();
    include('view_pattern.php');
}

//-----------------------------------------------------------------------------

function f_control_list() {
    f_connect();
    include('view_list.php');
}

//-----------------------------------------------------------------------------

function f_control_committee() {
    include('view_committee.php');
}

//-----------------------------------------------------------------------------

function f_control_admin() {
    
    if (!isset($_SESSION) or !isset($_SESSION['user']) or !in_array('admin', $_SESSION['user']->rights)) {
        f_control('home', True);
        return;
    }
    
    $req = '';
    if (isset($_GET['remove_admin'])) {
        //$req = "UPDATE users SET can_admin = 'no' WHERE id = " . $_GET['id'];
        $req = "DELETE FROM users_rights WHERE id_user = " . $_GET['id'] . " AND `right` = 'admin' ";    
    } else if (isset($_GET['grant_admin'])) {
        //$req = "UPDATE users SET can_admin = 'yes' WHERE id = " . $_GET['id'];
        $req = "INSERT INTO users_rights VALUES ( " . $_GET['id'] . " , 'admin' )";
    } else if (isset($_GET['remove_publish'])) {
        //$req = "UPDATE users SET can_publish = 'no' WHERE id = " . $_GET['id'];
        $req = "DELETE FROM users_rights WHERE id_user = " . $_GET['id'] . " AND `right` = 'publi' ";  
    } else if (isset($_GET['grant_publish'])) {
        //$req = "UPDATE users SET can_publish = 'yes' WHERE id = " . $_GET['id'];
        $req = "INSERT INTO users_rights VALUES ( " . $_GET['id'] . " , 'publi' )";
    }
    if ($req != '') {
        f_connect();
        $result = mysql_query($req);
        if (!$result) {
            f_error('ERROR UPDATING USERS');
        }
    }

    f_view_admin();
}

//-----------------------------------------------------------------------------

function f_control_browse() {
    f_view_browse();
}

//-----------------------------------------------------------------------------
/*
function f_control_new() {
    if(isset($_GET['page'])) {
        $_SESSION['page'] = f_get_page_from_code($_GET['page']);
    } else if (isset($_GET['submit'])) {
        //if ($_GET['submit'] != count($_SESSION['codes'])) {
            $_SESSION['page'] = f_get_page_from_code($_GET['submit']+1);
            foreach ($_POST as $posted => $value) {
                if (isset($_SESSION['patron'][$posted])) {
                    $_SESSION['patron'][$posted] = $value;
                }
            }
        //}
        if (isset($_POST['valid'])) {
            $req = 'INSERT INTO patterns VALUES ( NULL, ';
            $first = True;
            foreach($_SESSION['patron'] as $value) {
                if(!$first) {
                    $req = $req . ",";
                } else {
                    $first = False;
                }
                $req = $req . "'" . $value . "'";
            }
            $req = $req . ")";
            f_connect();
            $result = mysql_query($req);
            if(!$result) {
                echo $req;
                f_error("INSERT NEW PATTERN FAILED");
            }
            f_control('home', True);
            return;
        }
    }
    f_view_new();
}
*/
//-----------------------------------------------------------------------------

function f_control_register() {
    f_connect();

    if (!isset($_POST['valid'])) { // POST !
        f_view_register();
        return;
    }
    
    // Already exist?
    $exist = False;
    $result = mysql_query("SELECT login FROM users");
    if (!$result) {
        f_error('SELECT USERS');
    }
    while ($user = mysql_fetch_array($result)) {
        if ($user[0] == $_POST['login']) {
            $exist = True;
            break;
        }
    }
    if ($exist) {
        f_error("USER ALREADY EXIST");
        die("arg");
    }

    $result = mysql_query("INSERT INTO users (login, password,name,organization,email) VALUES ('" . $_POST['login'] . "','" . sha1($_POST['password']) . "','" . $_POST['name'] . "','" . $_POST['organisation'] . "','" . $_POST['email'] ."')");
    if (!$result) {
        f_error("USER CREATION FAILED");
        die("arg");
    } else { // OK
        
        $req = "SELECT id FROM users WHERE login = '" . $_POST['login'] . "'";
        $result = mysql_query($req);
        $line = mysql_fetch_array($result);
        $id = $line[0];

        $req = "INSERT INTO users_rights VALUES ( " . $id . ", 'publi')";
        $result = mysql_query($req);
        
        $_SESSION['user'] = new User();
        $_SESSION['user']->id = $id;
        $_SESSION['user']->login = $_POST['login'];
        $_SESSION['user']->name = $_POST['name'];
        $_SESSION['user']->organisation = $_POST['organisation'];
        $_SESSION['user']->email = $_POST['email'];
        $_SESSION['user']->rights[] = 'publi';

        f_control('home', True);
    }
}

//-----------------------------------------------------------------------------

function f_control_login() {
    f_connect();
    $result = mysql_query("SELECT login, password, id FROM users");
    $valid = False;
    $id = null;
    while ($user = mysql_fetch_array($result)) {
        if ($user[0] == $_POST['login'] and $user[1] == sha1($_POST['password'])) {
            $valid = True;
            $id = $user[2];
            break;
        }
    }
    if (!$valid) {
        f_error("INVALID USER");
        die("arg");
    } else { // OK
        $_SESSION['user'] = User::get($id);
    }
    f_control('home', True);
}

//-----------------------------------------------------------------------------

function f_control_home() {
    f_view_home();
}

?>

