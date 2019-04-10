from twisted.internet import reactor
from datetime import datetime

FPS = 30
turn = 0

def f(): #(s)
    global turn
    turn += 1
    print(turn, '@', datetime.now())
    #print("hello", s)
    reactor.callLater(1/FPS, f)
    #reactor.callLater(1/FPS, f, s + 'a')

reactor.callLater(1/FPS, f) #, "b")
reactor.run()
