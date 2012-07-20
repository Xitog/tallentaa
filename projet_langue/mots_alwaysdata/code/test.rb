#!/usr/bin/ruby

ENV['GEM_PATH'] += ':/home/mots/www/code/gems/'

require 'rubygems'
require 'mysql'
#my = Mysql.new(hostname, username, password, databasename)
con = Mysql.new('mysql2.alwaysdata.com', 'mots', 'pass', 'mots_db')
rs = con.query('select * from nouns')
rs.each_hash { |h| puts h['base']}
con.close
