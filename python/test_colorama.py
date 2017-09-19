from colorama import Fore, Back, init

# after every print statement color is reset back to normal terminal colors
init(autoreset=True) 

print(Fore.RED + 'This looks like a servere warning')
print('back to normal now')
print(Back.GREEN + 'Here is text on a green background')

up = "\u001b[1A"
down = "\u001b[{n}B"
right = "\u001b[{n}C"
left = "\u001b[{n}D"

# 9h25 : ça marche !
print(up + "AAA")

import sys
import tty
tty.setraw(sys.stdin) # marche pas sur windows :-( nécessaire pour capter les entrées
