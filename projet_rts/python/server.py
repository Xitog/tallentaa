import socketserver

i = 0
g_queue = None

class TCPHandler(socketserver.StreamRequestHandler):
    """
    Instanciated once per connection to the server,
    must override handle().
    BaseRequestHandler => recv
    """

    def handle(self):
        try:
            global i
            print("[INFO] Start of connexion.")
            print(self.request.__class__) # <class 'socket.socket'>
            done = False
            while not done:
                print("i = ", i)
                c = self.rfile.readline().strip()
                print("received = ", c, "(", c.__class__, ")") # c = b'hello toi'
                ##print(self.data.__class__)
                ##print("self.data = ", self.data)
                #print(c.__class__)
                #print(self.handle.__class__)
                
                s = c.decode('utf-8')
                tab = s.split(' ')
                if tab[0] == "shutdown":
                    done = True
                elif tab[0] == "reply":
                    self.wfile.write(b"HELLO\r\n")
                elif tab[0] == "set":
                    if len(tab) < 2:
                        print("[ERROR] No value given for set command.")
                    else:
                        try:
                            i = int(tab[1])
                            g_queue.put_nowait(i)
                        except ValueError:
                            print("[ERROR] The given value is not an integer.")
                si = (str(i) + "\r\n").encode('utf-8')
                self.wfile.write(si)
        except ConnectionAbortedError:
            print("[INFO] Connection aborted.")
        finally:
            print("[INFO] End of connexion.")

class Server:

    def __init__(self, host, port, queue):
        global g_queue
        self.host = host
        self.port = port
        self.queue = queue
        g_queue = queue
    
    def start(self):
        with socketserver.TCPServer((self.host, self.port), TCPHandler) as server:
            try:
                print("[INFO] Server listening on %s:%s" % (self.host, self.port))
                server.serve_forever()
            except KeyboardInterrupt:
                print("[INFO] Keyboard interruption.")
            finally:
                print("[INFO] Goodbye.")

if __name__ == "__main__":
    HOST, PORT = "localhost", 2222
    s = Server(HOST, PORT)
    s.start()
