<!-- GENERIC PATTERNS CATALOG -->

<tr> 
    <td valign="top" class="slink2" bgcolor="white" width="155px"> 
    <table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
	    <tr> 
    		<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
			    <table width="100%" border="0" bgcolor="#3BAADA" align="center" cellspacing="2" cellpadding="2"> 
				    <tr> 
    					<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
						    <b><center>Generic Patterns</center></b> 
					    </td> 
				    </tr> 
			    </table> 
		    </td> 
	    </tr> 
    </table> 
    <table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
        <tr>
            <td colspan="2">
                <form method="post" style="margin:0px;padding:0px;width:100%;" name="myform"> 

<SELECT NAME="mylist" id="mylist" style="font-size:11px;font-family:arial;width:100%;border-width:1px;border-style:solid;border-color:#ffffff" onchange="document.location.href=this.options[this.selectedIndex].value;"> 
<OPTION style="" Value="" selected="selected">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Select a Pattern</option>

<?php

f_connect();
$gen_patterns = f_list_patterns('generic');
foreach($gen_patterns as $p) {
    echo '<option value="index.php?action=view&id=' . $p["id"] . '">' . $p["Pattern Name"] . '</option>';
}

?>

</SELECT>

                </form>
            </td>
        </tr>
        <tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		    </td> 
    		<td valign="top" class="slink2"> 
			    <a href="index.php?action=list&type=generic&param=alphabetical" class="slink20">List (alphabetical)</a> 
		    </td> 
	    </tr> 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=generic&param=attributes" class="slink20">List (by S&D attributes)</a> 
		</td> 
	</tr> 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=generic&param=requirements" class="slink20">List (by requirements)</a> 
		</td> 
	</tr> 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=generic&param=text" class="slink20">List (text)</a> 
		</td> 
	</tr> 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=generic&param=gof" class="slink20">List (GoF)</a> 
		</td> 
	</tr> 

	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=generic" class="slink20" target="_parent">Pattern Profiles</a> 
		</td> 
	</tr> 

	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=new&type=generic" class="slink20">Pattern Submission Form</a> 
		</td> 
	</tr> 

</table> 
 
<br/> 

<!-- SPECIFIC PATTERN CATALOG --> 
 
 
<table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
	<tr> 
    		<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
			<table width="100%" border="0" bgcolor="#3BAADA" align="center" cellspacing="2" cellpadding="2"> 
				<tr> 
    					<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
						<b><center>Specific Patterns</center></b> 
					</td> 
				</tr> 
			</table> 
		</td> 
	</tr> 
</table> 
 
<table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
<tr>
<td colspan="2">

<form method="post" style="margin:0px;padding:0px;width:100%;" name="myform"> 
<SELECT NAME="mylist" id="mylist" style="font-size:11px;font-family:arial;width:100%;border-width:1px;border-style:solid;border-color:#ffffff" onchange="document.location.href=this.options[this.selectedIndex].value;"> 
<OPTION style="" Value="" selected="selected">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Select a Pattern</option>

<?php

$spe_patterns = f_list_patterns('specific');

foreach($spe_patterns as $p) {
    echo '<option value="index.php?action=view&id=' . $p["id"] . '">' . $p["Pattern Name"] . '</option>';
}

?>

</SELECT>
</form>

</td>
</tr>

	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=specific&param=alphabetical" class="slink20">List (alphabetical)</a> 
		</td> 
	</tr> 
 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=specific&param=attributes" class="slink20">List (by S&D attributes)</a> 
		</td> 
	</tr> 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=specific&param=requirements" class="slink20" target="_parent">List (by requirements)</a> 
		</td> 
	</tr> 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=specific&param=text" class="slink20" target="_parent">List (text)</a> 
		</td> 
	</tr> 
 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=specific&param=gof" class="slink20">List (GoF)</a> 
		</td> 
	</tr> 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=list&type=specific" class="slink20" target="_parent">Pattern Profiles</a> 
		</td> 
	</tr> 

	</tr> 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=new&type=specific" class="slink20">Pattern Submission Form</a> 
		</td> 
	</tr> 
</table> 
 
<br/> 
 
 
<!-- CANDIDATE DESIGN PATTERNS --> 
 
 
 
<table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
	<tr> 
    		<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
			<table width="100%" border="0" bgcolor="#3BAADA" align="center" cellspacing="2" cellpadding="2"> 
				<tr> 
    					<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
						<b><center>Candidate Patterns</center></b> 
					</td> 
				</tr> 
			</table> 
		</td> 
	</tr> 
</table> 
 
<table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=committee" class="slink20">Patterns Review Committee</a> 
		</td> 
	</tr> 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=browse&type=generic&param=candidate" class="slink20">Generic Candidate <br/>Patterns List</a> 
		</td> 
	</tr> 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="index.php?action=browse&type=specific&param=candidate" class="slink20">Specific Candidate <br/>Patterns List</a> 
		</td> 
	</tr> 
</table> 
 
<br/> 
 
 
<!-- WIKIPEDIA INFORMATION --> 
 
 
<table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
	<tr> 
    		<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
			<table width="100%" border="0" bgcolor="#3BAADA" align="center" cellspacing="2" cellpadding="2"> 
				<tr> 
    					<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
						<b><center>Information</center></b> 
					</td> 
				</tr> 
			</table> 
		</td> 
	</tr> 
</table> 
<table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="http://en.wikipedia.org/wiki/Design_pattern_%28computer_science%29" class="slink20">Design Pattern definition</a> 
		</td> 
	</tr> 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="http://en.wikipedia.org/wiki/Dependability" class="slink20">Dependability definition</a> 
		</td> 
	</tr> 
 
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="http://en.wikipedia.org/wiki/Safety_engineering" class="slink20">Safety definition</a> 
		</td> 
	</tr> 

	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="http://en.wikipedia.org/wiki/Computer_security" class="slink20">Security definition</a> 
		</td> 
	</tr> 

	<tr> 
    	<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    	<td valign="top" class="slink2"> 
			<a href="http://en.wikipedia.org/wiki/Systems_engineering_process" class="slink20">Process definition</a> 
		</td> 
	</tr>
    
    <tr>
        <td width="20" valign="top" class="slink2">
            &nbsp;&nbsp;<img src="bullet.png"/>&nbsp;
        </td>
        <td valign="top" class="slink2"> 
			<!--<?php echo '<a href="http://index.php?action=home" class="slink20">Glossary</a>'; ?> -->
            <a href="index.php?action=home" class="slink20">Glossary</a> 
		</td> 
</table> 
 
<br/> 
 
<!-- LINKS --> 
 
<table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0"> 
	<tr> 
    		<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
			<table width="100%" border="0" bgcolor="#3BAADA" align="center" cellspacing="2" cellpadding="2"> 
				<tr> 
    					<td width="100%" valign="top" class="slink2" bgcolor="#3BAADA"> 
						<b><center>Links</center></b> 
					</td> 
				</tr> 
			</table> 
		</td> 
	</tr> 
</table> 
 
<table width="100%" border="0" bgcolor="white" align="center" cellspacing="0" cellpadding="0">  
	<tr> 
    		<td width="20" valign="top" class="slink2"> 
			&nbsp;&nbsp;<img src="bullet.png" />&nbsp;
		</td> 
    		<td valign="top" class="slink2"> 
			<a href="http://www.teresa-project.org/" class="slink20">Teresa Project</a> 
		</td> 
	</tr> 
</table> 
<br/>

</td>

<!-- COLONNE INVISIBLE SEPARATRICE -->
                <td width="1" align="center" bgcolor="white">
                    <img src="pix.gif" border="0" alt="" width="1" height="1" /> 
				</td>

