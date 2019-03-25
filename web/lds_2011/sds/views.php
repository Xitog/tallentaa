<?php

//-----------------------------------------------------------------------------

function f_view_home() {
    include("view_home.php");
}

//-----------------------------------------------------------------------------

function f_view_new() {
    f_head();
    f_body_start();
    //f_info();
    f_title("Create New Pattern");
    f_login();
    if ($_SESSION['page'] != 'End') {
        f_menu();
        f_form_start();    
        include('html/' . $_SESSION['pages'][$_SESSION['page']]);
    } else {
        include('html/form_end.html');
    }

    /*    
    switch($_SESSION['page']) {
        case 'Base':
            include('form_base.html');
            break;
        case 'S&D and RCES':
            include(
            break;
        case 'Quality and Needs':
            break;
        case 'Deployment and Services':
            break;
        case 'Static and dynamic structures':
            break;
    }
    */
    f_form_end();
    f_body_end();
}

//-----------------------------------------------------------------------------

function f_view_browse() {
    f_head();
    f_body_start();
    //f_info();
    f_title('Browse Patterns');
    f_login();

    echo "<div>Display the patterns saved into the repository. Click on one of them to see it in detail and notes attached.</div>";

    $patterns = f_get_patterns();
    echo "<ul>";
    foreach($patterns as $pattern) {
        echo '<li><a href="index.php?action=browse&id=' . $pattern[0] . '">'. $pattern[2] . " ( " . $pattern[3] . ") </a><i>published by " . $pattern[1] . "</i> ( " . $pattern[4] . " notes)</li>";
    }
    echo "</ul>";

    f_body_end();
}

//-----------------------------------------------------------------------------

function f_view_register() {

    f_head();
    f_body_start();
    //f_info();
    f_title("Register a new user");
    f_login();

    include("html/register_form.html");

    f_body_end();
}

//-----------------------------------------------------------------------------

function f_view_admin() {
    $users = User::get_all();

    f_head();
    f_body_start();
    f_title("Adminstrate users");
    f_login();
    echo "<div>This page is for administrators only. Display all the users. You can edit their rights.</div><br/>";
    echo '<table width="100%">';
    foreach($users as $user) {
        echo '<tr><td>' . $user->login . '</td><td>' . $user->name . '</td><td>' . $user->organisation . '</td><td>' . $user->email . '</td>';
        if (in_array('admin', $user->rights)) {
            echo '<td>Admin (<a href="index.php?action=admin&id=' . $user->id . '&remove_admin">remove</a>)</td>';
        } else {
            echo '<td><a href="index.php?action=admin&id=' . $user->id . '&grant_admin">grant admin</a></td>';
        }
        if (in_array('publi', $user->rights)) {
            echo '<td>Publisher (<a href="index.php?action=admin&id=' . $user->id . '&remove_publish">remove</a>)</td><tr>';
        } else {
            echo '<td><a href="index.php?action=admin&id=' . $user->id . '&grant_publish">grant publish</a></td><tr>';
        }
    }
    echo '</table>';
    f_body_end();
}

?>

