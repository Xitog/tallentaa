import datetime

def update():
    print("Youpi!")

while True:
    start_time = datetime.datetime.now()
    delta = datetime.datetime.now() - start_time
    update()
    while delta.total_seconds() < 1: # each second
        delta = datetime.datetime.now() - start_time
    print(delta.total_seconds())

