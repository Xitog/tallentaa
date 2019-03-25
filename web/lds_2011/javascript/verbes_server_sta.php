<?php

//talk("<html charset='utf8'> <body>");

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

$inf = utf8_decode($lines[$found]);
$pre = utf8_decode($lines[$found+1]);
$pap = utf8_decode($lines[$found+2]);
$imp = utf8_decode($lines[$found+3]);
$fut = utf8_decode($lines[$found+4]);

$out = "<table><tr><td>" . $inf . "</td></tr><tr><td>" . $pre . "</td></tr><tr><td>" . $pap . "</td></tr><tr><td>" . $imp . "</td></tr><tr><td>" . $fut . "</td></tr><table>";

// Send

$pageContents = <<< EOPAGE
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html lang="en" xml:lang="en">
	<head>
		<meta http-equiv="Content-Type" content="txt/html; charset=utf-8" />
		<style type="text/css">
			table {
				border: 1px solid black;
			}
			tr.tb {
				border-top: 1px solid grey;
				border-bottom: 1px solid grey;
			}
			td.sub {
				border: 1px solid black;
			}
			
			img {
				bottom: 4px;
				position: relative;
			}
			
			div.opt {
				background-color: aliceblue;
				display: none;
			}
			
		</style>
		
		<script type="text/javascript">
			
			function show(d, i) {
				target = document.getElementById(d);
				if (target.style.display != 'block') {
					target.style.display = 'block';
					document.getElementById(i).src = 'less.png';
				} else {
					target.style.display = 'none';
					document.getElementById(i).src = 'plus.png';
				}
			}
			
		</script>
		
	</head>
	<body>
		<div id="id_div_1"> <img id='i1' src="plus.png" align="middle" onclick="show('p1', 'i1')"/> <i>$verb</i><div id='p1' class='opt'>$out</div></div>
	</body>
</html>
EOPAGE;

talk($pageContents);

?>
