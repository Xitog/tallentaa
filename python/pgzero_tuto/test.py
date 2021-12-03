import pgzrun

alien = Actor('alien')
alien.pos = 100, 56

WIDTH = 640
HEIGHT = 480

def draw():
    screen.fill((128, 0, 0))
    alien.draw()

def update():
    alien.left += 2
    if alien.left > WIDTH:
        alien.right = 0

def on_mouse_down(pos):
    if alien.collidepoint(pos):
        print("Eek!")
        sounds.eep.play()
        alien.image = 'alien_hurt'
        clock.schedule_unique(set_alien_normal, 1.0)
    else:
        print("You missed me!")

def set_alien_normal():
    alien.image = 'alien'

pgzrun.go()
