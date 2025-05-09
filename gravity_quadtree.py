import pygame
import random
import time
import math

pygame.init()

display_width = 1000
display_height = 600

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('title')

black = (0,0,0)
white = (255,255,255)
clock = pygame.time.Clock()
endgame = False

GRAVITY = 0.1

world = []
for x in range(display_width+1):
    world.append([])
    for y in range(display_height+1):
        world[-1].append(0)

particles = []

#functions

def display_image(x,y,img):
    screen.blit(img, (x,y))

def playsound(sound):
    pygame.mixer.Sound.play(sound)

def distance(x1,y1,x2,y2):
    temp1 = (x1-x2) ** 2
    temp2 = (y1-y2) ** 2
    return math.sqrt(temp1+temp2)

def playsong(filepath):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)

#classes

class Particle:
    def __init__(self,x=None,y=None,dx=0,dy=0):
        if x is None:
            x = random.randint(0,display_width)
        if y is None:
            y = random.randint(0,display_height)
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y
        self.dx = 0
        self.dy = 0
    
    def attract(self,part):
        dist = distance(self.x,self.y,part.x,part.y)
        force = GRAVITY
        force /= (dist+0.0001)
        changex = (self.x-part.x) / (dist+0.0001)
        changey = (self.y-part.y) / (dist + 0.0001)
        part.dx += force * changex
        part.dy += force * changey

    def boundry(self):
        if self.x < 0:
            self.tx += display_width
            self.dx *= 0.9
        elif self.x > display_width:
            self.tx -= display_width
            self.dx *= 0.9
        if self.y < 0:
            self.ty += display_height
            self.dy *= 0.9
        elif self.y > display_height:
            self.ty -= display_height
            self.dy *= 0.9
        self.x = int(self.tx)
        self.y = int(self.ty)

    def run(self):
        global lastx
        global lasty
        world[self.x][self.y] = 0
        self.tx += self.dx
        self.ty += self.dy
        self.x = int(self.tx)
        self.y = int(self.ty)
        self.boundry()
        tdx = 0
        tdy = 0
        mxd = (self.dx ** 2) + (self.dy ** 2)
        mxd = math.sqrt(mxd)
        if abs(self.dx) > 0:
            tdx = self.dx/mxd
        if abs(self.dx) > 0:
            tdy = self.dy/mxd
        adj = False
        while world[self.x][self.y] == 1:
            adj = True
            self.tx -= tdx
            self.ty -= tdy
            self.y = int(self.ty)
            self.x = int(self.tx)
            self.boundry()
        if adj:
            self.dx *= -0.9
            self.dy *= -0.9
        world[self.x][self.y] = 1
        for i in particles:
            if i != self:
                self.attract(i)

    def display(self):
        screen.set_at((self.x,self.y),white)

#game_start
screen.fill(black)

for i in range(40):
    #particles.append(Particle())
    pass

while not endgame:
    
    mousep = pygame.mouse.get_pos()
    mousex = mousep[0]
    mousey = mousep[1]

    for i in particles:
        i.run()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endgame = True 
        if event.type == pygame.MOUSEBUTTONDOWN:
            for x in range(3):
                for y in range(3):
                    particles.append(Particle((x*3)+mousex,(y*3)+mousey))
        if event.type == pygame.KEYDOWN:
            dx = random.random()*100-50
            dy = random.random()*100-50
            for x in range(3):
                for y in range(3):
                    particles.append(Particle((x*3)+mousex,(y*3)+mousey,dx,dy))            
    
    screen.fill(black)
    for i in particles:
        i.display()
    pygame.display.update()
    clock.tick(60) 