import pygame
import random
import time

pygame.init()

display_width = 1000
display_height = 600

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('title')

black = (0,0,0)
white = (255,255,255)
clock = pygame.time.Clock()
endgame = False
dirstuff = {0:[1,0],1:[0,1],2:[-1,0],3:[0,-1]}
prob = [2,20,40,60,80]
world_pop = {}
world_pop_dir = {}
#globals

population = []
toremove = []
width = int(1000/8)
height = int(600/8)
world = []
for y in range(height):
    world.append([])
    for x in range(width):
        world[-1].append(random.choice((0,1)))


#functions

def display_image(x,y,img):
    screen.blit(img, (x,y))

def playsound(sound):
    pygame.mixer.Sound.play(sound)

def playsong(filepath):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)

def draw_world():
    for y in range(height):
        for x in range(width):
            if world[y][x] == 1:
                tempx = x*8
                tempy = y*8
                tempx += 1.5
                tempy += 1.5
                pygame.draw.circle(screen,(0,155,0),(tempx,tempy),3,1)
            elif world[y][x] == 2:
                tempx = x*8
                tempy = y*8
                tempx += 1.5
                tempy += 1.5
                cellcol = world_pop.setdefault((x,y),(155,0,0))
                tempdir = world_pop_dir.setdefault((x,y),0)
                pygame.draw.circle(screen,cellcol,(tempx,tempy),3) 
                nx = (dirstuff[tempdir][0]*4)+tempx
                ny = (dirstuff[tempdir][1]*4)+tempy
                pygame.draw.line(screen,cellcol,(tempx,tempy),(nx,ny),1)
                 

def update_world():
    for y in range(height):
        for x in range(width):
            if world[y][x] == 0:
                neighbors = []
                numalive = 0
                if x < width-1:
                    neighbors.append((x+1,y))
                if x > 0:
                    neighbors.append((x-1,y))
                if y < height-1:
                    neighbors.append((x,y+1))
                if y > 0:
                    neighbors.append((x,y-1))
                for i in neighbors:
                    if world[i[1]][i[0]] == 1:
                        numalive += 1
                if random.randint(1,100) <= prob[numalive]:
                    world[y][x] = 1
                


#classes

class Organism:
    def __init__(self,x,y,health,name):
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.x = x
        self.y = y
        world_pop[(x,y)] = self.color
        self.name = name
        self.lifespan_degrade = random.choice([0.01,0.03,0.05,0.07])
        self.dir = random.randint(0,3)
        self.health = health
        self.memory_1 = 0
        self.memory_2 = 0
        self.memory_3 = 0
        self.tosee = 0
        self.genetic_instructions = {}
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    for a in range(4):
                        self.genetic_instructions[(x,y,z,a)] = random.choice((-1,0,1))
    def move(self):
        neighbors = []
        dirpos = [i for i in dirstuff[self.dir]]
        dirpos[0] += self.x
        dirpos[1] += self.y
        if self.x < width-1:
            neighbors.append((self.x+1,self.y))
        if self.x > 0:
            neighbors.append((self.x-1,self.y))
        if self.y < height-1:
            neighbors.append((self.x,self.y+1))
        if self.y > 0:
            neighbors.append((self.x,self.y-1))
        if (self.health > self.lifespan_degrade*90):
            loc = 0
            for i in neighbors:
                if world[i[1]][i[0]] in (0,1):
                    loc = i
            if loc != 0:
                mutations = 0
                self.health = (self.lifespan_degrade * 15)
                population.append(Organism(loc[0],loc[1],(self.lifespan_degrade * 15),7))
                population[-1].lifespan_degrade = self.lifespan_degrade
                if random.randint(1,100) <= 5:
                    mutations += 1
                    population[-1].lifespan_degrade += random.choice((-0.01,0.01))
                    if population[-1].lifespan_degrade > 1:
                        population[-1].lifespan_degrade = 1
                    if population[-1].lifespan_degrade < 0.01:
                        population[-1].lifespan_degrade = 0.01
                for i in self.genetic_instructions:
                    population[-1].genetic_instructions[i] = self.genetic_instructions[i]
                for i in population[-1].genetic_instructions:
                    if random.randint(1,100) <= 5:
                        mutations += 1
                        population[-1].genetic_instructions[i] = random.choice((-1,0,1))
                population[-1].color = self.color
                if mutations > 0:
                    toadd = int(mutations * random.choice((-0.1,0.1)))
                    col = random.choice((1,2,3))
                    if col == 1:
                        population[-1].color = ((self.color[0]+toadd)%256,self.color[1],self.color[2])
                    elif col == 2:
                        population[-1].color = (self.color[0],(self.color[1]+toadd)%256,self.color[2])
                    else:
                        population[-1].color = (self.color[0],self.color[1],(self.color[2]+toadd)%256)

            else:
                toremove.append(self)
        if tuple(dirpos) not in neighbors:
            self.tosee = 3
        else:
            self.tosee = world[dirpos[1]][dirpos[0]]
        straight = (self.genetic_instructions[(self.tosee,self.memory_1,self.memory_2,self.memory_3)] == 0)
        self.dir += self.genetic_instructions[(self.tosee,self.memory_1,self.memory_2,self.memory_3)]
        self.dir %= 4
        self.memory_3 = self.memory_2
        self.memory_2 = self.memory_1
        self.memory_1 = self.tosee
        dirpos = [i for i in dirstuff[self.dir]]
        dirpos[0] += self.x
        dirpos[1] += self.y
        if (tuple(dirpos) in neighbors) and straight:
            next = dirpos
        else:
            next = (self.x,self.y)
        if world[next[1]][next[0]] == 1:
            self.health += 1
        elif world[next[1]][next[0]] == 2:
            next = (self.x,self.y)
        world[self.y][self.x] = 0
        self.x = next[0]
        self.y = next[1]
        world[self.y][self.x] = 2
        world_pop[(self.x,self.y)] = self.color
        world_pop_dir[(self.x,self.y)] = self.dir
        if straight:
            self.health -= self.lifespan_degrade
        else:
            self.health -= (self.lifespan_degrade/2)
        if self.health <= 0:
            toremove.append(self)

#game_start
screen.fill(black)
t = 0

for i in range(10):
    population.append(Organism(random.randint(0,width-1),random.randint(0,height-1),3,7))
population[-1].name = 'bob'

while not endgame:
    t += 1
    
    mousep = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endgame = True 
    
    tempop = []
    while len(population) > 0:
        mychoice = random.choice(population)
        population.remove(mychoice)
        tempop.append(mychoice)
    population = [i for i in tempop]
    for i in population:
        i.move()

    if t%75 == 0:
        update_world()

    while len(toremove) > 0:
        population.remove(toremove[-1])
        temp = toremove.pop()
        world[temp.y][temp.x] = 0
        del(temp)

    screen.fill(black)
    draw_world()
    pygame.display.update()
    clock.tick(10) 