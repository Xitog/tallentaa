<html> 
<head> 
	<title>Security, Dependability, Safety Design Patterns Repository</title> 
	<meta HTTP-EQUIV="Content-Type" CONTENT="text/html"> 
	<meta name="description" content="A community site dedicated to design patterns for Security, Dependability and Safety and the development of a repository."> 
	<meta name="keywords" content="patterns, design patterns, safety, dependability, security">
    <link REL='stylesheet' TYPE='text/css' HREF='main.css' /> 
    <script type="text/javascript">
<!--

// Pop up
// http://www.commentcamarche.net/faq/19477-popup-en-css-sans-javascript
// cf main.cs

// Handling of tab
// http://www.css4design.com/exemples/menu_onglets/

function multiClass(eltId) {
	arrLinkId = new Array('_1','_2','_3','_4');
	intNbLinkElt = new Number(arrLinkId.length);
	arrClassLink = new Array('current','ghost');
	strContent = new String()
	for (i=0; i<intNbLinkElt; i++) {
		strContent = "menu"+arrLinkId[i];
		if ( arrLinkId[i] == eltId ) {
			document.getElementById(arrLinkId[i]).className = arrClassLink[0];
			document.getElementById(strContent).className = 'on content';
		} else {
			document.getElementById(arrLinkId[i]).className = arrClassLink[1];
			document.getElementById(strContent).className = 'off content';
		}
	}	
}

// Handling of dynamic input
// http://www.randomsnippets.com/2008/02/21/how-to-dynamically-add-form-elements-via-javascript/

// For new field for pattern

var counter = 0;
var limit = 10;
function addInput(divName){
     //alert("poulpe");
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs : \n consider starting from another generic pattern");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = '<u class="slink7">Choose a category, a field name and a value for field ' + (counter + 1) + '</u><br><br><span class="slink7">Category: </span><select name="myCategory" class="slink7"><option>Pattern Identity</option><option>Property</option><option>S&D</option><option>Interface</option><option>External Interface</option><option>Internal Structure</option><option>Static Structure</option><option>Dynamic Structure</option><option>Pattern Attributes</option><option>Use Case</option></select><span class="slink7"> Field: </span><input type="text" name="myFields[]" size="31"><br><br><span class="slink7">Value:</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <input type="text" size="50" name="myValues[]"><br><br>';
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}

// For new signature field for the specific pattern of an generic pattern that we are creating
// DANGER : LES CATS SONT FIXES ET IL Y A ENCORE USE CASE !!!
// myCat[] ???

var counter = 0;
var limit = 40;
function addInput2(divName){
     //alert("poulpe");
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs : \n consider starting from another generic pattern");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = '<u class="slink7">Choose a category, a field name and a type for field ' + (counter + 1) + '</u><br><br><span class="slink7">Category: </span><select name="sigCategories[]" class="slink7"><option>Pattern Identity</option><option>Property</option><option>S&D</option><option>Interface</option><option>External Interface</option><option>Internal Structure</option><option>Static Structure</option><option>Dynamic Structure</option><option>Pattern Attributes</option><option>Use Case</option></select><span class="slink7"> Field: </span><input type="text" name="sigFields[]" size="31"><br><br><span class="slink7">Type:</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <select name="sigTypes[]" class="slink7"><option>Number</option><option>String</option><option>Date</option><option>File</option></select>&nbsp;&nbsp;&nbsp;&nbsp;<span class="slink7">Mandatory:</span><select name=sigMandatories[] class="slink7"><option value="1">Yes</option><option value="0">No</option></select><br><br>';
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}

-->
    </script>
</head> 

<body link="blue" vlink="blue" alink="blue" bgcolor="#DDDDDD"> 
 
<table width="700" border="0" borderColor="black" align="center" cellspacing="0" cellpadding="0" bgcolor="white"> 
   <tr> 
    	<td width="700" valign="top" class="slink2" bgcolor="white"> 
		    <table width="700" border="0" borderColor="black" align="center" cellspacing="0" cellpadding="0" bgcolor="white"> 
			    <tr> 
    				<td width="700" valign="top" class="slink2" bgcolor="#000000" colspan="3"> 
					    <table width="100%" border="0" bgcolor="#000000" align="center" cellspacing="0" 
                               cellpadding="0"style="border-width:0px;border-color:#000000;border-style:solid"> 
	                        <tr> 
    		                    <td width="100%" bgcolor="#000000" align="right" style="border-width:0px;border-color:#000000;border-style:solid;"> 
			                        <a href="index.php?action=home" target="_parent"><img border="0" alt="Return to Home Page" src="title.png"></a><br/> 
		                        </td> 
  	                        </tr> 
                        </table> 
				    </td> 
  			    </tr>
