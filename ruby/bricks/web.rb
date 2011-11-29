require 'webrick'

# Accès sur : http://localhost:2000/

#C:\Documents and Settings\Damien\Bureau>ruby web.rb
#[2006-05-12 19:57:20] INFO  WEBrick 1.3.1
#[2006-05-12 19:57:20] INFO  ruby 1.8.2 (2004-12-25) [i386-mswin32]
#[2006-05-12 19:57:20] INFO  WEBrick::GenericServer#start: pid=2780 port=2000
#[2006-05-12 20:04:31] INFO  going to shutdown ...
#[2006-05-12 20:04:31] INFO  WEBrick::GenericServer#start done.

#
# Daytime server 
# 19h58 : Fri May 12 19:58:26 Paris, Madrid (heure d'été) 2006
#
def daytime
	# Création du serveur
	s = WEBrick::GenericServer.new( :Port => 2000 )
	trap("INT"){ s.shutdown }
	# Démarrage
	s.start{ |sock|
		sock.print(Time.now.to_s + "\r\n")
	}
end

#daytime

#
# Autre façon d'avoir un daytime (plus propre)
#
class DaytimeServer < WEBrick::GenericServer
  # Méthode appelée après le start
  def run(sock)
    sock.print(Time.now.to_s + "\r\n")
  end
end

# Lancement
# s = DaytimeServer.new( :Port => 2000 )
# trap("INT"){ s.shutdown }
# s.start

#
# HTTP Server
# 20h08 : Webrick rules !
#
def http_server
	include WEBrick

	s = HTTPServer.new(
	  :Port            => 2000,
	  :DocumentRoot    => Dir::pwd + "/htdocs"
	)

	# mount subdirectories A voir ...
	s.mount("C:/Documents and Settings/Damien/Bureau",HTTPServlet::FileHandler,"/zorba",true)
	#s.mount("/ipr", HTTPServlet::FileHandler, "/proj/ipr/public_html")
	#s.mount("/~gotoyuzo",
	#        HTTPServlet::FileHandler, "/home/gotoyuzo/public_html",
	#        true)  #<= allow to show directory index.

	trap("INT"){ s.shutdown }
	s.start
end

http_server

#
# HTTPS Server (nécessite Ruby/OpenSSL)
#
#!/usr/local/bin/ruby
#require 'webrick'
#require 'webrick/https'

#s = WEBrick::HTTPServer.new(
#  :Port            => 2000,
#  :DocumentRoot    => Dir::pwd + "/htdocs",
#  :SSLEnable       => true,
#  :SSLVerifyClient => ::OpenSSL::SSL::VERIFY_NONE,
#  :SSLCertName => [ ["C","JP"], ["O","WEBrick.Org"], ["CN", "WWW"] ]
#)
#trap("INT"){ s.shutdown }
#s.start

#
# Serveur de Servlet
# 20h15 : hello, world.
# 20h16 : hello (again) TROP PUISSANT !
#
require 'webrick'
include WEBrick

s = HTTPServer.new( :Port => 2000 )

# HTTPServer#mount(path, servletclass)
#   When a request referring "/hello" is received,
#   the HTTPServer get an instance of servletclass
#   and then call a method named do_"a HTTP method".

class HelloServlet < HTTPServlet::AbstractServlet
  def do_GET(req, res)
    res.body = "<HTML>hello, world.</HTML>"
    res['Content-Type'] = "text/html"
  end
end
s.mount("/hello", HelloServlet)


# HTTPServer#mount_proc(path){|req, res| ...}
#   You can mount also a block by `mount_proc'.
#   This block is called when GET or POST.

s.mount_proc("/hello/again"){|req, res|
  res.body = "<HTML>hello (again)</HTML>"
  res['Content-Type'] = "text/html"
}

trap("INT"){ s.shutdown }
s.start