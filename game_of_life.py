import pygame
import random
import time

pygame.init()

display_width = 400
display_height = 400

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('title')

black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
clock = pygame.time.Clock()
endgame = False

#globals

width = 100
height = 100
world = []
for y in range(height):
    world.append([])
    for x in range(width):
        world[-1].append(int(random.choice([0])))

world[30][30] = 1
world[29][30] = 1
world[31][30] = 1
world[29][31] = 1
world[30][29] = 1

#functions

def display_image(x,y,img):
    screen.blit(img, (x,y))

def playsound(sound):
    pygame.mixer.Sound.play(sound)

def playsong(filepath):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)

def display_world(world):
    for y in range(height):
        for x in range(width):
            tempy = (y * 4)+1.5
            tempx = (x * 4)+1.5
            if world[y][x] == 1:
                pygame.draw.circle(screen,white,(tempx,tempy),2,0)

def update_world(world):
    tempworld = []
    
    for y in range(height):
        tempworld.append([])
        for x in range(width):
            tempworld[-1].append(0)
    
    for y in range(height):
        for x in range(width):
            neighbors = []
            if x > 0:
                neighbors.append(world[y][x-1])
                if y > 0:
                    neighbors.append(world[y-1][x-1])
                if y < (height-1):
                    neighbors.append(world[y+1][x-1])
            if x < (width-1):
                neighbors.append(world[y][x+1])
                if y > 0:
                    neighbors.append(world[y-1][x+1])
                if y < (height-1):
                    neighbors.append(world[y+1][x+1])
            if y > 0:
                neighbors.append(world[y-1][x])
            if y < (height-1):
                neighbors.append(world[y+1][x])
            summation = 0
            if len(neighbors) > 0:
                summation = sum(neighbors)
            tempworld[y][x] = world[y][x]
            if (summation == 3):
                tempworld[y][x] = 1
            elif (summation > 3) or (summation < 2):
                tempworld[y][x] = 0
    return tempworld

#game_start
screen.fill(black)
running = False

while not endgame:
    
    mousep = pygame.mouse.get_pos()
    mousex = mousep[0]//4
    mousey = mousep[1]//4

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endgame = True 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not(running)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                world[mousey][mousex] = 1
            if event.button == 3:
                world[mousey][mousex] = 0                
    
    screen.fill(black)
    if running:
        world = update_world(world)
    display_world(world)
    if (mousex > -1) and (mousex < width) and (mousey > -1) and (mousey < height):
        tempy = (mousey * 4)+1.5
        tempx = (mousex * 4)+1.5
        pygame.draw.circle(screen,yellow,(tempx,tempy),2,0)
    pygame.display.update()
    clock.tick(10) 