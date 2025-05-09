import pygame
import random
import time
import numpy as np

pygame.init()

display_width = 1000
display_height = 600

sz = 6

world_width = int(display_width/sz)
world_height = int(display_height/sz)

noise = np.random.normal(0,0.5,world_width)

world = np.zeros((world_width,world_height),np.int8)
for x in range(world_width):
    for y in range(world_height):
        world[x,y] = (1 if noise[x] > (random.random()*2) else 0)

dirx = [-1,1,0,0]
diry = [0,0,-1,1]

antx = int(world_width/2)
anty = int(world_height-5)
antdir = 0

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('title')

black = (0,0,0)
white = (255,255,255)
clock = pygame.time.Clock()
endgame = False
#functions

def display_image(x,y,img):
    screen.blit(img, (x,y))

def temp_world():
    new_world = np.zeros((world_width,world_height),np.int8)
    return new_world

def get_state(x,y):
    t_arr = [0,0,0]
    if y >= world_height-1:
        return (1,1,1)
    if x <= 0:
        t_arr[0] = 1
    else:
        t_arr[0] = world[x-1,y+1]
    if x >= world_width-1:
        t_arr[2] = 1
    else:
        t_arr[2] = world[x+1,y+1]
    t_arr[1] = world[x,y+1]
    return tuple(t_arr)

def bound(num,mx,mn):
    num = max((num,mn))
    num = min((num,mx))
    return num

def update_world():
    global world
    global antx
    global anty
    global antdir
    new_world = temp_world()
    for x in range(world_width):
        for y in range(world_height):
            '''if (x,y) == (antx,anty):
                tx = antx-dirx[antdir]
                tx = bound(tx,world_width-1,1)
                ty = anty-diry[antdir]
                ty = bound(ty,world_height-1,1)
                if world[x,y] == 1:
                    world[x,y] = 0
                    world[tx,ty] = 0
                    antdir += 1
                    antdir = antdir%4
                else:
                    world[x,y] = 1
                    world[tx,ty] = 1
                    antdir -= 1
                    antdir = antdir%4
                antx += dirx[antdir]
                anty += diry[antdir]
                antx = bound(antx,world_width-1,1)
                anty = bound(anty,world_height-1,1)'''
            if world[x,y] == 1:
                tstate = get_state(x,y)
                if tstate[1] == 0:
                    new_world[x,y+1] = 1
                elif tstate == (1,1,0):
                    new_world[x+1,y+1] = 1
                elif tstate == (0,1,1):
                    new_world[x-1,y+1] = 1
                elif tstate == (0,1,0):
                    if random.random() < 0.5:
                        new_world[x+1,y+1] = 1
                    else:
                        new_world[x-1,y+1] = 1
                elif tstate == (1,1,1):
                    new_world[x,y] = 1
                
    world = new_world
    
def display_world(n):
    for x in range(world_width):
        for y in range(world_height):
            tx = x * n
            ty = y * n
            if world[x][y] == 1:
                for a in range(n):
                    for b in range(n):
                        screen.set_at((tx+a,ty+b),white)

def playsound(sound):
    pygame.mixer.Sound.play(sound)

def playsong(filepath):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)

#game_start
screen.fill(black)
update_time = 0

clicked = False

while not endgame:
    
    update_time += 1

    mousep = pygame.mouse.get_pos()
    mousex = round(mousep[0]/sz)
    mousey = round(mousep[1]/sz)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endgame = True 
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = False
    if clicked:
        if (world_width-1) > mousex > 0 and (world_height-1) > mousey > 0:
            world[mousex][mousey] = 1
    if update_time % 1 == 0:
        update_world()
    
    screen.fill(black)
    display_world(6)
    pygame.display.update()
    clock.tick(60) 