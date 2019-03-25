<?php

function f_connect() {
    $host = "sql.free.fr"; //ini_get("mysql.default_host");
    $user = "looking.dwarf"; //ini_get("mysql.default_user");
    $password = "asydug"; //ini_get("mysql.default_password");
    $db = 'looking_dwarf'; //'repository';
    
    return f_connect_target($host, $user, $password, $db);
}

function f_connect_target($host, $user, $password, $db, $new=False, $debug=False)
{
    if ($debug) {
        echo $host . '<br>';
        echo $user . '<br>';
        echo $password . '<br>';
        echo $db . '<br>';
    }

    $connection = mysql_connect($host, $user, $password);
    if (!$connection) {
        f_error("DATABASE SERVER CONNECTION FAILED");
    }
    if($new) {
        $sql = 'CREATE DATABASE ' . $db;
        $create = mysql_query($sql);   
        //$create = mysql_create_db($db);
        if (!$create) {
            f_error("DATABASE CREATION FAILED");
        } 
    }
    $database = mysql_select_db($db);
    if (!$database) {
        f_error("DATABASE SELECTION FAILED");
    }
    return $database;
}

//-----------------------------------------------------------------------------

function f_error($message) {
    echo "<h1>ERROR: " . $message . " : " . mysql_error() . "</h1>";
}

//-----------------------------------------------------------------------------

function f_request($req) {
    $result = mysql_query($req);
    if (!$result) {
        f_error('REQUEST FAILED : <i>' . $req . '</i>');
    }
    return $result;
}

?>

