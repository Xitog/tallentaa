<?php

class User { // Php 4 pose des erreurs pour User
}

/*
class User {
    
    var $login = '';
    var $name = '';
    var $organisation = '';
    var $email = '';
    var $rights;
    var $id = 0;

    function __construct() {
        $this->rights = (array) null;
    }

    static function get_all() {
        f_connect();
        $result = mysql_query("SELECT login, name, organization, email, ID FROM users");
        if (!$result) {
            f_error('SELECT ALL USERS FAILED');
        }
        $users = (array) null;
        while ($u = mysql_fetch_array($result)) {
            $user = new User();
            $user->login = $u[0];
            $user->name = $u[1];
            $user->organisation = $u[2];
            $user->email = $u[3];
            $user->id = $u[4];
            // Rights
            $result2 = mysql_query("SELECT `right` FROM users_rights WHERE id_user=" . $u[4]);
            if (!$result2) {
            f_error('SELECT RIGHTS FOR USER ' . $u[4] . ' FAILED');
            }
            while($r = mysql_fetch_array($result2)) {
                $user->rights[] = $r[0];
            }

            $users[] = $user;
        }
        return $users;
    }

    static function get($id) {
        f_connect();
        $result = mysql_query("SELECT login, name, organization, email, ID FROM users WHERE ID=" . $id);
        if (!$result) {
            f_error('SELECT USER ' . $id . ' FAILED');
        }
        $u = mysql_fetch_array($result);
        $user = new User();
        $user->login = $u[0];
        $user->name = $u[1];
        $user->organisation = $u[2];
        $user->email = $u[3];
        $user->id = $u[4];

        $result = mysql_query("SELECT `right` FROM users_rights WHERE id_user=" . $id);
        if (!$result) {
            f_error('SELECT RIGHTS FOR USER ' . $id . ' FAILED');
        }
        while($r = mysql_fetch_array($result)) {
            $user->rights[] = $r[0];
        }
        
        return $user;
    }
    
}
*/

/*
//-----------------------------------------------------------------------------

// level enum('Architectural','Design','Implementation')
// security enum('access_control','integrity','authenticity','confidentiality')
// dependability enum('fault tolerance')
// EAL enum('EAL1','EAL2','EAL3','EAL4','EAL5','EAL6','EAL7')
// SIL enum('SIL1','SIL2','SIL3','SIL4')
function f_get_pattern($id) {
    f_connect();
    $result = mysql_query("SELECT ID, publisher_id, name, level, origin, alias, related_patterns, consequences, other, RCES_time_delay, RCES_rom_size, RCES_ram_size, RCES_power_consumption, RCES_other, S&D_security, S&D_dependability, Quality_EAL, Quality_SIL, Quality_DIN_19250, Quality_IEEE_certification, Quality_other, Property_other, Needs_integrity_algorithm, Needs_cryptographic_algorithm, Needs_flow_control_protocol, Needs_other, Deployment_ad_hoc_network, Deployment_client_server, Deployment_distribued_systems, Deployment_embedded_systems, Deployment_other, goal, services_secure_administration, services_secure_access, services_secure_download, services_secure_storage, services_other, intent_other, static_structure_definition	text, static_structure_participants, static_structure_static_links, static_structure_diagram, dynamic_structure_definition, dynamic_structure_operator, dynamic_structure_diagram FROM patterns WHERE ID = ". $id);
    if (!$result) {
        f_error('SELECT A PATTERN FAILED');
    }
    $pattern = mysql_fetch_array($result);
    return $pattern;
}

//-----------------------------------------------------------------------------

function f_get_patterns() {
    f_connect();

    $req = <<<EOT
SELECT patterns.ID, users.login, patterns.name, patterns.level, count(notes.ID)
FROM users, patterns LEFT JOIN notes ON notes.id_pattern = patterns.ID
WHERE patterns.publisher_id = users.ID
GROUP BY patterns.ID
EOT;

    $result = mysql_query($req);
    if (!$result) {
        f_error('SELECT ALL PATTERNS FAILED');
    }
    $patterns = (array) null;
    while ($pattern = mysql_fetch_array($result)) {
        $patterns[] = $pattern;
    }
    return $patterns;
}
*/
//-----------------------------------------------------------------------------

// NEO

function f_list_patterns ($type, $param='None') {
    //if ($type == 'generic') {
        $req = <<<EOT
SELECT sds_patterns.id as pattern, 
       sds_fields_def.id as field_id, 
       sds_fields_def.name as field_name, 
       sds_patterns_fields.value as field_value, 
       sds_fields_def.type as field_type, 
       sds_fields_def.gof as field_gof
FROM sds_patterns, sds_patterns_fields, sds_fields_def
WHERE sds_patterns.type = '####'
AND sds_patterns.id = sds_patterns_fields.id_pattern
AND sds_patterns_fields.id_field_def in (1, 5)
AND sds_fields_def.id = sds_patterns_fields.id_field_def
ORDER BY sds_patterns.id
EOT;
    //}
    $req = str_replace('####', $type, $req);
    $result = f_request($req);
    $patterns = (array) null;
    $old_id = -1;
    $index = 0;
    while ($row = mysql_fetch_array($result)) {
        if ($old_id != $row['pattern']) {
            $old_id = $row['pattern'];
            $index += 1;
            $patterns[$index] = (array) null;
            $patterns[$index]['id'] = $row['pattern'];
        }
        $key = $row['field_name'];
        $val = $row['field_value'];
        $patterns[$index][$key] = $val;
    }
    //var_dump($patterns);
    return $patterns;
}

//-----------------------------------------------------------------------------

function f_view_pattern($id) {
    $req = <<<EOT
SELECT sds_fields_def.name as field_name,
 sds_patterns_fields.value as field_value,
 sds_fields_def.ref_category as innermost_category,
 sds_fields_def.type as field_type,
 sds_fields_def.gof as field_gof
FROM sds_patterns_fields, sds_fields_def, sds_categories 
WHERE id_pattern = ####
AND sds_patterns_fields.id_field_def = sds_fields_def.id
AND sds_categories.name = sds_fields_def.ref_category
EOT;
    $req = str_replace('####', $id, $req);
    $result = f_request($req);
    $pattern = (array) null;
    while ($row = mysql_fetch_array($result)) {
        $pattern[] = $row;
    }
    return $pattern;
}

//-----------------------------------------------------------------------------

function f_get_mothers() {
    $req = <<<EOT
SELECT name, `order`, `comment`
FROM sds_categories
WHERE mere = 'None'
AND name != 'None'
ORDER BY `order` ASC
EOT;
    $result = f_request($req);
    $categories = (array) null;
    while ($row = mysql_fetch_array($result)) {
        $categories[] = $row;
    }
    return $categories;
}

//-----------------------------------------------------------------------------

function f_get_daughters($id) {
    $req = <<<EOT
SELECT name
FROM sds_categories
WHERE mere = '####'
ORDER BY `order` ASC
EOT;
    $req = str_replace('####', $id, $req);
    $result = f_request($req);
    $subcategories = (array) null;
    while ($row = mysql_fetch_array($result)) {
        $subcategories[] = $row;
    }
    return $subcategories;
}

//-----------------------------------------------------------------------------

function f_get_fields($id_pattern, $category) {
    $req = <<<EOT
SELECT sds_fields_def.name as field_name,
 sds_patterns_fields.value as field_value,
 sds_fields_def.ref_category as innermost_category,
 sds_fields_def.type as field_type,
 sds_fields_def.gof as field_gof
FROM sds_patterns_fields, sds_fields_def, sds_categories 
WHERE id_pattern = ####
AND sds_patterns_fields.id_field_def = sds_fields_def.id
AND sds_categories.name = sds_fields_def.ref_category
AND sds_categories.name = '????'
EOT;
    $req = str_replace('####', $id_pattern, $req);
    $req = str_replace('????', $category, $req);
    $result = f_request($req);
    $pattern = (array) null;
    while ($row = mysql_fetch_array($result)) {
        $pattern[] = $row;
    }
    return $pattern;
}

//-----------------------------------------------------------------------------

// La meme sans value a alle chercher
function f_get_fields_def($id_pattern_gen, $category) {
    $req = <<<EOT
SELECT pdf.id as id, pdf.id_field_def as field_id,fd.name as field_name, fd.type as field_type, fd.ref_category as field_category, pdf.obligatoire as obligatoire, fd.gof as field_gof, fd.comment as field_comment
FROM sds_patterns_def_fields as pdf, sds_fields_def as fd
WHERE id_pattern_def = ####
AND fd.id = pdf.id_field_def
AND fd.ref_category = '????'
EOT;
    $req = str_replace('####', $id_pattern_gen, $req);
    $req = str_replace('????', $category, $req);
    $result = f_request($req);
    $pattern = (array) null;
    while ($row = mysql_fetch_array($result)) {
        $pattern[] = $row;
    }
    return $pattern;
}

//-----------------------------------------------------------------------------

function f_get_max_id_pattern() {
    $req = 'select max(id) as id from sds_patterns';
    $result = f_request($req);
    $id = 1;
    $row = mysql_fetch_array($result);
    //var_dump($row);
    if($row) { $id = $row['id']; }
    return $id;
}

//-----------------------------------------------------------------------------

function f_get_max_fields_def() {
    $req = 'select max(id) as id from sds_fields_def';
    $result = f_request($req);
    $id = 1;
    $row = mysql_fetch_array($result);
    //var_dump($row);
    if($row) { $id = $row['id']; }
    return $id;
}

function f_is_gen($id) {
    $req = 'select type from sds_patterns where id = ' . $id;
    $result = f_request($req);
    $row = mysql_fetch_array($result);
    return $row['type'] == 'generic'; 
}

?>
