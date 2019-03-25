<?php

?>

<html>
<body>
	<form method="get" action="verbes_server.php">
		<table>
			<tr>
				<td>
					<p>Entrez un verbe :
						<input type="text" name="verb"/>
					</p>
					<p>ou</p>
					<p>Choisissez parmi :
						<select name="verb_list">
							<option value="none"></option>
							<option value="essere">essere</option>
							<option value="avere">avere</option>
						</select>
					</p>
				</td>
				<td>
					<input type="submit" value="Go!"/>
				</td>
			</tr>
		</table>
	</form>
</body>
</html>