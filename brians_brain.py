import pygame
import random
import time

pygame.init()

display_width = 600
display_height = 600

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Brian\'s Brain')

black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
blue = (0,0,255)
clock = pygame.time.Clock()
endgame = False

#globals

width = 100
height = 100
world = []
for y in range(height):
    world.append([])
    for x in range(width):
        world[-1].append(random.choice([0]))

world[33][49] = 1
world[33][50] = 1
world[66][49] = 1
world[66][50] = 1
world[49][33] = 1
world[50][33] = 1
world[49][66] = 1
world[50][66] = 1

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
            tempy = (y * 6)+2.25
            tempx = (x * 6)+2.25
            if world[y][x] == 1:
                pygame.draw.circle(screen,white,(tempx,tempy),3,0)
            if world[y][x] == 0.01:
                pygame.draw.circle(screen,blue,(tempx,tempy),3,0)


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
            if (summation >= 2) and (summation < 3):
                tempworld[y][x] = 1
            if world[y][x] == 1:
                tempworld[y][x] = 0.01
            if world[y][x] == 0.01:
                tempworld[y][x] = 0
    return tempworld

#game_start
screen.fill(black)
running = False

while not endgame:
    
    mousep = pygame.mouse.get_pos()
    mousex = mousep[0]//6
    mousey = mousep[1]//6

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endgame = True 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not(running)
            if event.key == pygame.K_ESCAPE:
                endgame = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                world[mousey][mousex] = 1
            if event.button == 2:
                world[mousey][mousex] = 0.01
            if event.button == 3:
                world[mousey][mousex] = 0                
    
    screen.fill(black)
    if running:
        world = update_world(world)
    display_world(world)
    if (mousex > -1) and (mousex < width) and (mousey > -1) and (mousey < height):
        tempy = (mousey * 6)+2.25
        tempx = (mousex * 6)+2.25
        pygame.draw.circle(screen,yellow,(tempx,tempy),3,0)
    pygame.display.update()
    clock.tick(10) 