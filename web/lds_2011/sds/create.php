<?php

/*
$filename = 'repository.sql';
$handle = fopen($filename, 'r');
$contents = fread($handle, filesize($filename));
fclose($handle);

echo $contents;
*/

$s_create_table_fields = <<<EOT
CREATE TABLE IF NOT EXISTS `fields` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Label` varchar(50) NOT NULL,
  `Type` varchar(30) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
EOT;
$s_create_table_notes = <<<EOT
CREATE TABLE IF NOT EXISTS `notes` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ID_user` int(11) NOT NULL,
  `ID_pattern` int(11) NOT NULL,
  `Content` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;
EOT;
$s_insert_table_notes = <<<EOT
INSERT INTO `notes` (`ID`, `ID_user`, `ID_pattern`, `Content`) VALUES
(1, 1, 1, 'From Robert : a very good pattern!'),
(2, 2, 1, 'From Maverick : indeed!');
EOT;
$s_create_table_patterns = <<<EOT
CREATE TABLE IF NOT EXISTS `patterns` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `publisher_id` int(11) NOT NULL,
  `name` text NOT NULL,
  `level` enum('Architectural','Design','Implementation') DEFAULT NULL,
  `origin` text,
  `alias` text,
  `related_patterns` text,
  `consequences` text,
  `other` text,
  `RCES_time_delay` int(11) DEFAULT NULL,
  `RCES_rom_size` int(11) DEFAULT NULL,
  `RCES_ram_size` int(11) DEFAULT NULL,
  `RCES_power_consumption` int(11) DEFAULT NULL,
  `RCES_other` text,
  `S&D_security` enum('access_control','integrity','authenticity','confidentiality') DEFAULT NULL,
  `S&D_dependability` enum('fault tolerance') DEFAULT NULL,
  `Quality_EAL` enum('EAL1','EAL2','EAL3','EAL4','EAL5','EAL6','EAL7') DEFAULT NULL,
  `Quality_SIL` enum('SIL1','SIL2','SIL3','SIL4') DEFAULT NULL,
  `Quality_DIN_19250` text,
  `Quality_IEEE_certification` text,
  `Quality_other` text,
  `Property_other` text,
  `Needs_integrity_algorithm` text,
  `Needs_cryptographic_algorithm` text,
  `Needs_flow_control_protocol` text,
  `Needs_other` text,
  `Deployment_ad_hoc_network` text,
  `Deployment_client_server` text,
  `Deployment_distribued_systems` text,
  `Deployment_embedded_systems` text,
  `Deployment_other` text,
  `goal` text,
  `services_secure_administration` text,
  `services_secure_access` text,
  `services_secure_download` text,
  `services_secure_storage` text,
  `services_other` text,
  `intent_other` text,
  `static_structure_definition` text,
  `static_structure_participants` text,
  `static_structure_static_links` text,
  `static_structure_diagram` text,
  `dynamic_structure_definition` text,
  `dynamic_structure_operator` text,
  `dynamic_structure_diagram` text,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23345 ;
EOT;
$s_insert_table_patterns = <<<EOT
INSERT INTO `patterns` (`ID`, `publisher_id`, `name`, `level`, `origin`, `alias`, `related_patterns`, `consequences`, `other`, `RCES_time_delay`, `RCES_rom_size`, `RCES_ram_size`, `RCES_power_consumption`, `RCES_other`, `S&D_security`, `S&D_dependability`, `Quality_EAL`, `Quality_SIL`, `Quality_DIN_19250`, `Quality_IEEE_certification`, `Quality_other`, `Property_other`, `Needs_integrity_algorithm`, `Needs_cryptographic_algorithm`, `Needs_flow_control_protocol`, `Needs_other`, `Deployment_ad_hoc_network`, `Deployment_client_server`, `Deployment_distribued_systems`, `Deployment_embedded_systems`, `Deployment_other`, `goal`, `services_secure_administration`, `services_secure_access`, `services_secure_download`, `services_secure_storage`, `services_other`, `intent_other`, `static_structure_definition`, `static_structure_participants`, `static_structure_static_links`, `static_structure_diagram`, `dynamic_structure_definition`, `dynamic_structure_operator`, `dynamic_structure_diagram`) VALUES
(2, 1, 'A more complex pattern (Robert)', 'Design', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(3, 2, 'Another pattern (Maverick)', 'Implementation', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(1, 1, 'A simple pattern (Robert)', 'Architectural', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
EOT;
$s_create_table_patterns_fields = <<<EOT
CREATE TABLE IF NOT EXISTS `patterns_fields` (
  `ID_pattern` int(11) NOT NULL,
  `ID_field` int(11) NOT NULL,
  `value` varchar(50) NOT NULL,
  PRIMARY KEY (`ID_pattern`,`ID_field`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
EOT;
$s_create_table_rights = <<<EOT
CREATE TABLE IF NOT EXISTS `rights` (
  `code` varchar(5) NOT NULL,
  `label` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
EOT;
$s_insert_table_rights = <<<EOT
INSERT INTO `rights` (`code`, `label`) VALUES
('admin', 'Administrator rights.'),
('publi', 'Publisher rights.');
EOT;
$s_create_table_users = <<<EOT
CREATE TABLE IF NOT EXISTS `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `login` text NOT NULL,
  `password` text NOT NULL,
  `name` text NOT NULL,
  `organization` text NOT NULL,
  `email` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12231 ;
EOT;
$s_insert_table_users = <<<EOT
INSERT INTO `users` (`ID`, `login`, `password`, `name`, `organization`, `email`) VALUES
(12226, 'Mark', 'Azerty', 'Rosewater', 'Magic', 'mark@magic.com'),
(5, 'Damien', 'Azerty', 'Damien Gouteux', 'IRIT', 'gouteux@irit.fr'),
(1, 'Robert', 'Azerty', 'Robert H.', 'RobertCorp', 'rob@corp.com'),
(2, 'Maverik', 'Azerty', 'Mav', 'MavCorp', 'Mac@corp.com'),
(12227, 'Bob', '0f300f33b728cabd2cd5cbde86757722de291ceb', 'Morton', 'OCP', 'morton@ocp.com'),
(12228, 'Slim', '0f300f33b728cabd2cd5cbde86757722de291ceb', 'Os', 'OXO', 'slim@oxo.com'),
(12229, 'Fabien', '0f300f33b728cabd2cd5cbde86757722de291ceb', 'DFG', 'DFG', 'fabien@DFG.com'),
(12230, 'Zembla', '0f300f33b728cabd2cd5cbde86757722de291ceb', 'TheGreat', 'Pulpix', 'zembla@pulpix.com');
EOT;
$s_create_table_users_rights = <<<EOT
CREATE TABLE IF NOT EXISTS `users_rights` (
  `id_user` int(11) NOT NULL,
  `right` varchar(5) NOT NULL,
  PRIMARY KEY (`id_user`,`right`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
EOT;
$s_insert_table_users_rights = <<<EOT
INSERT INTO `users_rights` (`id_user`, `right`) VALUES
(5, 'publi'),
(12227, 'publi'),
(12228, 'publi'),
(12229, 'admin'),
(12230, 'publi');
EOT;

include('tools.php');

$host = ini_get("mysql.default_host");
$user = ini_get("mysql.default_user");
$password = ini_get("mysql.default_password");
$db_name = 'repository';

f_connect_target($host, $user, $password, $db_name, True, True);

f_request($s_create_table_fields);
f_request($s_create_table_notes);
f_request($s_insert_table_notes);
f_request($s_create_table_patterns);
f_request($s_insert_table_patterns);
f_request($s_create_table_patterns_fields);
f_request($s_create_table_rights);
f_request($s_insert_table_rights);
f_request($s_create_table_users);
f_request($s_insert_table_users);
f_request($s_create_table_users_rights);
f_request($s_insert_table_users_rights);

?>
