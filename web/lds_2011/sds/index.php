<?php

session_start();

include('tools.php');
include('views.php');
include('controls.php');
include('models.php');

//-----------------------------------------------------------------------------

f_control();

//-----------------------------------------------------------------------------

function f_info() {
    var_dump($_SESSION);
    var_dump($_GET);
    //echo "Poulpi ! ";
    if (isset($_GET['page'])) {
        echo f_get_page_from_code($_GET['page']);
    } else if (isset($_GET['submit'])) {
        echo 'submit : ' . $_GET['submit'] . '<br/>';
    }
    if ($_SESSION['page'] != 'End') {    
        echo $_SESSION['pages'][$_SESSION['page']];
    }
}

//-----------------------------------------------------------------------------

function f_init() {
    $_SESSION['state'] = 'started';
    $_SESSION['page'] = 'Base';
    $_SESSION['login'] = 'None';

    $pages = array("Base" => 'form_base.html', 
                   "S&D and RCES" => 'form_rces.html', 
                   "Quality and Needs" => 'form_quality.html', 
                   "Deployment and Services" => 'form_deployment.html', 
                   "Static and dynamic structures" => 'form_structures.html',
                   "Save" => 'form_end.html');

    $codes = array("Base" => '1',
                   "S&D and RCES" => '2',
                   "Quality and Needs" => '3',
                   "Deployment and Services" => '4',
                   "Static and dynamic structures" => '5',
                   "Save" => '6');

    $patron = array('name' => '',
                    'publisher' => '',
                    'level' => '',
                    'origin' => '',
                    'goal' => '',
                    'alias' => '',
                    'related_patterns' => '',
                    'consequences' => '',
                    'other_base' => '',
                    'time_delay' => '',
                    'rom_size' => '',
                    'ram_size' => '',
                    'power_consumption' => '',
                    'other_rces' => '',
                    'eal' => ''
                    
                   );
    
    $user = array('login' => '',
                  'name' => '',
                  'organisation' => '',
                  'email' => '');

    $_SESSION['pages'] = $pages;
    $_SESSION['codes'] = $codes;
    $_SESSION['patron'] = $patron;
    $_SESSION['user'] = new User();
}

//-----------------------------------------------------------------------------

function f_head() {
    $s = <<<EOT
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Create a new pattern</title>
    <link rel="stylesheet" type="text/css" href="css/main.css" media="all">
    <link rel="stylesheet" type="text/css" href="css/menu.css" media="all">
    <script type="text/javascript" src="view.js"></script>
</head>
EOT;
    echo $s;
}

//-----------------------------------------------------------------------------

function f_body_start() {
    $s = <<<EOT
<body id="main_body" bgcolor="#ccc">
<table id="main_table">
<tr>
<td>
EOT;
    echo $s;
}

//-----------------------------------------------------------------------------

function f_body_end() {
    $s = <<<EOT
</td>
</tr>
<tr><td>&nbsp;</td></tr>
<tr><td>&nbsp;</td></tr>
</table>
</body>
</html>
EOT;
    echo $s;
}

//-----------------------------------------------------------------------------

function f_form_start() {
    echo '<div id="main_container">';
	echo '<form id="main_form" class="main_form" method="post" action="index.php?action=new&submit=' . $_SESSION['codes'][$_SESSION['page']] . '">';
}

//-----------------------------------------------------------------------------

function f_form_end() {
    echo '<br/>';
    echo '</form>';
    echo '</div>';
}

//-----------------------------------------------------------------------------

function f_title($title) {
    echo '<h1>' . $title . '</h1>';
}

//-----------------------------------------------------------------------------

function f_get_page_from_code($code) {
    foreach($_SESSION['codes'] as $index => $value) {
        if ($code == $value) {
            return $index;
        }
    }
    return 'None';
}

//-----------------------------------------------------------------------------

function f_login() {

    $puremenu = <<<EOT
<center>
<table>
<tr>
<td>
<form method="post" action="index.php?action=login">
<!-- Start PureCSSMenu.com MENU -->
<ul class="pureCssMenu pureCssMenum">
	<li class="pureCssMenui"><a class="pureCssMenui" href="index.php?action=home" title="Back to the home page.">Home</a></li>
	<li class="pureCssMenui"><a class="pureCssMenui" href="#" title="Create a new pattern."><span>New Pattern</span><![if gt IE 6]></a><![endif]><!--[if lte IE 6]><table><tr><td><![endif]-->
	<ul class="pureCssMenum">
		<li class="pureCssMenui"><a class="pureCssMenui" href="index.php?action=new&type=generic" title="Create a new generic pattern.">Generic Pattern</a></li>
		<li class="pureCssMenui"><a class="pureCssMenui" href="index.php?action=new&type=specific" title="Create a new specific pattern.">Specific Pattern</a></li>
	</ul>
	<!--[if lte IE 6]></td></tr></table></a><![endif]--></li>
	<li class="pureCssMenui"><a class="pureCssMenui" href="#" title="Browse all patterns."><span>Browse</span><![if gt IE 6]></a><![endif]><!--[if lte IE 6]><table><tr><td><![endif]-->
	<ul class="pureCssMenum">
		<li class="pureCssMenui"><a class="pureCssMenui" href="index.php?action=browse&type=generic" title="View all generic patterns.">Generic Patterns</a></li>
		<li class="pureCssMenui"><a class="pureCssMenui" href="index.php?action=browse&type=specific" title="View all specific patterns.">Specific Patterns</a></li>
	</ul>
	<!--[if lte IE 6]></td></tr></table></a><![endif]--></li>
EOT;

    $not_logged = <<<EOT
    <li class="pureCssMenui"><a class="pureCssMenui" href="index.php?action=register" title="Register a new user.">New User</a></li>
    <li class="pureCssMenui"><a class="pureCssMenui">Login&nbsp;<input type="text" name="login" size="10"/></a></li>
    <li class="pureCssMenui"><a class="pureCssMenui">Password&nbsp;<input type="password" size="10" name="password"/></a></li>
    <li class="pureCssMenui"><input type="submit" value="Connect"/></li>
</ul>
</form>
</td>
</tr>
</table>
</center>
<br/>
<!-- End PureCSSMenu.com MENU -->
EOT;

    $logged =  '<li class="pureCssMenui"><a class="pureCssMenui"><i>&nbsp;&nbsp;logged as ' . $_SESSION['user']->login . '</i></ul></form></td></tr></table></center><br/>';

    if (in_array('admin', $_SESSION['user']->rights)) {
        $logged = '<li class="pureCssMenui"><a class="pureCssMenui" href="index.php?action=admin" title="Admin users.">Admin</a></li>' . $logged;
    }

    echo $puremenu;

    if ($_SESSION['user']->login == '') {
        echo $not_logged;
    } else {
        echo $logged;
    }
}

//-----------------------------------------------------------------------------

function f_menu() {
    echo '<p>';

    foreach($_SESSION['codes'] as $index => $value) {
        if ($index == $_SESSION['page']) {
            echo '<b>';
        } else {
            echo '<a href="http://localhost/repo/index.php?action=new&page=' . $value . '" >';
        }
        echo $index;
        if ($index == $_SESSION['page']) {
            echo '</b>';
        } else {
            echo '</a>';
        }
        if ($index != 'Save') {
            echo " -> ";
        }
    }
    echo '</p>';
}

//-----------------------------------------------------------------------------

?>
