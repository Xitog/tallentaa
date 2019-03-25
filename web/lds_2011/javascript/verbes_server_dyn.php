<?php

talk("<?xml version='1.0' encoding='UTF-8' ?>");

function talk($s) {
	echo(utf8_encode($s));
}

// Checks

$filename = './verbes_it.txt';

if (!is_file($filename)) {
    talk ('Unable to open data file.');
	die();
}

if (filesize($filename) == 0) {
	talk ('Data file empty');
	die();
}

$verb = "";
if (isset($_GET['verb'])) {
	$verb = utf8_decode($_GET['verb']);
} else {
	talk('No verb specified');
	die();
}

// Go
$fp = fopen($filename,'r');
$data = fread ($fp, filesize ($filename));
fclose ($fp);

// Search

$lines = explode("\n", $data);
$first = True;
$found = -1;
$i = 0;

//talk("Looking for $verb <br/>");
//talk("Nb lines : " . strval(count($lines)) . "<br/>");

foreach($lines as $line) {
	$rows = explode(',', $line);
	foreach($rows as $row) {
		$row = trim(rtrim(utf8_decode($row)));
		$sim = 0.0;
		similar_text($row, $verb, $sim);
		$ssim = strval($sim);
		//talk("Try $row vs $verb % $ssim<br/>");
		if (strcmp($row,$verb) == 0) { // if ($sim > 90.00) {
			//talk("Match<br/>");
			if ($first) {
				$first = False;
			} else {
				$found = $i;
			}
		}
	}
	$i += 1;
}
$out = $found;

// Send

talk("<answer>");
talk(strval($out));
talk("</answer>");