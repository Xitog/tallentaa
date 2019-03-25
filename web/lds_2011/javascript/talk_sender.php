<?php
//header('Content-Type: text/xml;charset=utf-8');

function talk($s) {
	echo(utf8_encode($s));
}

talk("<?xml version='1.0' encoding='UTF-8' ?>");
if (isset($_GET['operation']) and isset($_GET['op1']) and isset($_GET['op2'])) {
    $operation = utf8_decode($_GET['operation']);
	$op1 = utf8_decode($_GET['op1']);
	$op2 = utf8_decode($_GET['op2']);
} else {
    talk("<text>error</text>");
	die();
}
$operation = strtolower($operation);
$op1 = intval($op1);
$op2 = intval($op2);
if ($operation == "add") {
	$r = $op1 + $op2;
	talk("<text>");
	talk(strval($r));
	talk("</text>");
}

//$liste = array([...]);

//function generateOptions($debut,$liste) {
//    $MAX_RETURN = 10;
//    $i = 0;
//    foreach ($liste as $element) {
//        if ($i<$MAX_RETURN && substr($element, 0, strlen($debut))==$debut) {
//           talk("<option>".$element."</option>");
//            $i++;
//        }
//    }
//}

//generateOptions($debut,$liste);

//talk("</options>");

?>