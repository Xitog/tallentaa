#!/usr/bin/python3
# lundi 5 nov

import time, threading

start = time.time()
print(f"Start: {start}")

global_var = 2

def update():
    global global_var
    global_var *= 2

def render():
    print(f"--- time : {time.time()-start:.1f}s global_var : {global_var:06d}")

MAX = 5 # in seconds
EVERY = 0.33
previous = start
now = time.time()
while (now - start) < MAX:
    elapsed = now - previous
    if elapsed >= EVERY:
        update()
        render()
        previous = time.time()
    now = time.time()

end = time.time()
print(f"End: {end}")
print(f"Elapsed: {end-start}")
