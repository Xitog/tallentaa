<?php

// Load data

$filename = './todo.data';

if (!is_file($filename))
    die ('Unable to open data file.');

if (filesize($filename) == 0)
	die ('Data file empty');

$fp = fopen($filename,'r');
$data = fread ($fp, filesize ($filename));
fclose ($fp);

// Prepare data

$lines = explode("\n", $data);
$out = "<table>";
$i = 0;
foreach($lines as $line) {
	$out .= "<tr>";
	$rows = explode('|', $line);
	foreach($rows as $row) {
		$out .= "<td class='tb'>$row</td>";
	}
	$out .= "</tr>";
}
$out .= "</table>";

// Load page

$pageContents = <<< EOPAGE
<?xml version="1.0" encoding="iso-8859-1"?>
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
			// 15h07 : working 100%
			
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
		<div id="id_div_1"> <img id='i1' src="plus.png" align="middle" onclick="show('p1', 'i1')"/> <i>Essere</i><div id='p1' class='opt'>$out</div></div>
	</body>
</html>
EOPAGE;

echo $pageContents;

?>
