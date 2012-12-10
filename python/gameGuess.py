#python compare string and int without problem!
import random
goal  = random.randint(1,100)
guess = -1
trial = 0
#print 'goal = ', goal

def getval():
    try:
        return int(raw_input('guess? = '))
    except ValueError:
        # no retry in Python
        return None
    except Exception:
        return None

while guess != goal:
    # no do while in Python    
    guess = getval()
    while guess == None:
        guess = getval()
    #print 'guess = ', guess
    if guess > goal: print 'lower'
    if guess < goal: print 'upper'
    trial += 1
print 'you won in', trial

import string
print string.letters
print random.choice(string.letters)
l = [1,2,3,4,5]
random.shuffle(l)
for i in l:
    print i

