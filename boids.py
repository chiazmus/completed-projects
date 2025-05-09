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
gray = (155,155,155)
green = (0,255,0)
red = (255,0,0)
blue = (20,80,155)
sky_blue = (0,204,255)
clock = pygame.time.Clock()
endgame = False
boids = []
obs = []
sharks = []
world = []

for x in range(display_width+1):
    world.append([])
    for y in range(display_height+1):
        world[-1].append(-1)
        if x == 0 or x == display_width or y == 0 or y == display_height:
            world[-1][-1] = -2

#functions

def display_image(x,y,img):
    screen.blit(img, (x,y))

def playsound(sound):
    pygame.mixer.Sound.play(sound)

def playsong(filepath):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)

def to_rad(deg):
    deg *= math.pi
    deg /= 180
    return deg

def to_deg(rad):
    rad *= 180
    rad /= math.pi
    return rad

def distance(x1,y1,x2,y2):
    temp = abs(x1-x2)
    temp += abs(y1-y2)
    return temp

def bound(x,y):
    if x < 0:
        x += display_width
    elif x > display_width:
        x -= display_width
    if y < 0:
        y += display_height
    elif y > display_height:
        y -= display_height
    return (x,y)

def angular_ave(angs):
    cosum = 0
    sinsum = 0
    num = len(angs)
    for i in angs:
        cosum += math.cos(to_rad(i))
        sinsum += math.sin(to_rad(i))
    cosum /= num
    sinsum /= num
    deg = math.atan2(sinsum,cosum)
    return deg

def simple_round(num):
    num = int(num * 1000)
    num /= 1000
    return num

def angle_to(x1,y1,x2,y2):
    return math.atan2(y2-y1,x2-x1)

#classes

class Obsticle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        world[self.x][self.y] = -2
        obs.append(self)

    def draw(self):
        screen.set_at((self.x,self.y),red)

class Shark:
    def __init__(self,x=None,y=None,theta=None):
        if theta is None:
            theta = random.randint(1,360)
        if x is None:
            x = random.randint(0,display_width+1)
        if y is None:
            y = random.randint(0,display_height+1)
        self.x = x
        self.tx = x
        self.y = y
        self.ty = y
        self.theta = theta
        self.speed = 3
        self.s_range = 40
        sharks.append(self)
    
    def prey(self):
        angs = []
        for x in range(self.x-self.s_range,self.x+self.s_range+1):
            for y in range(self.y-self.s_range,self.y+self.s_range+1):
                pos = bound(x,y)
                if world[pos[0]][pos[1]] > -1 and (pos[0],pos[1]) != (self.x,self.y):
                    ang = to_deg(angle_to(self.x,self.y,x,y))
                    dist = distance(self.x,self.y,x,y)
                    if dist >= 0:
                        angs.append(ang)
                else:
                    if world[pos[0]][pos[1]] == -2 and pos != (self.x,self.y):
                        ang = to_deg(angle_to(self.x,self.y,x,y))
                        angs.append(ang+180)
        if angs == []:
            return self.theta
        else:
            return to_deg(angular_ave(angs))

    def update(self):
        self.theta += random.randint(-15,15)
        an = self.prey()
        if abs(an-self.theta) > abs((an+360)-self.theta):
            an += 360
        self.theta += simple_round((an-self.theta)/4)
        self.theta = self.theta % 360
        self.move()

    def move(self):
        world[self.x][self.y] = -1
        self.last_x = self.x
        self.last_y = self.y
        self.tx += math.cos(to_rad(self.theta))*self.speed
        self.ty += math.sin(to_rad(self.theta))*self.speed
        pos = bound(self.tx,self.ty)
        self.tx = pos[0]
        self.ty = pos[1]
        self.x = int(self.tx)
        self.y = int(self.ty)
        world[self.x][self.y] = -2    

    def draw(self):
        screen.set_at((self.x,self.y),red)  
        screen.set_at((self.x+1,self.y),red)
        screen.set_at((self.x-1,self.y),red)
        screen.set_at((self.x,self.y+1),red)
        screen.set_at((self.x,self.y-1),red)

class Boid:
    def __init__(self,x=None,y=None,theta=None):
        if x is None:
            x = random.randint(0,display_width+1)
        if y is None:
            y = random.randint(0,display_height+1)
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y
        self.last_x = x
        self.last_y = y
        if theta is None:
            theta = random.randint(1,360)
        self.theta = theta
        self.speed = 4
        self.s_range = 20
        boids.append(self)
    
    def boundries(self):
        if self.tx < 0:
            self.tx += display_width
        elif self.tx > display_width:
            self.tx -= display_width
        if self.ty < 0:
            self.ty += display_height
        elif self.ty > display_height:
            self.ty -= display_height
        self.x = int(self.tx)
        self.y = int(self.ty)

    def align_neighbor(self):
        angs = [self.theta]
        for x in range(self.x-self.s_range,self.x+self.s_range+1):
            for y in range(self.y-self.s_range,self.y+self.s_range+1):
                pos = bound(x,y)
                ang = 0
                if world[pos[0]][pos[1]] > -1 and (pos[0],pos[1]) != (self.x,self.y):
                    ang = world[pos[0]][pos[1]]
                    angs.append(ang)
        return to_deg(angular_ave(angs))
    
    def separation(self):
        angs = []
        for x in range(self.x-self.s_range,self.x+self.s_range+1):
            for y in range(self.y-self.s_range,self.y+self.s_range+1):
                pos = bound(x,y)
                if world[pos[0]][pos[1]] > -1 and (pos[0],pos[1]) != (self.x,self.y):
                    ang = to_deg(angle_to(self.x,self.y,x,y))
                    dist = distance(self.x,self.y,x,y)
                    if dist <= 16:
                        angs.append(ang+180)
                    elif dist >= 32:
                        angs.append(ang)
                else:
                    if world[pos[0]][pos[1]] == -2:
                        ang = to_deg(angle_to(self.x,self.y,x,y))
                        angs.append(ang+180)
        if angs == []:
            return self.theta
        else:
            return to_deg(angular_ave(angs))

    def update(self):
        self.theta += random.randint(-2,2)
        an = self.align_neighbor()
        if abs(an-self.theta) > abs((an+360)-self.theta):
            an += 360
        self.theta += simple_round((an-self.theta)/4)
        an = self.separation()
        if abs(an-self.theta) > abs((an+360)-self.theta):
            an += 360
        self.theta += simple_round((an-self.theta)/4)
        self.theta = self.theta % 360
        self.fly()

    def fly(self):
        world[self.x][self.y] = -1
        self.last_x = self.x
        self.last_y = self.y
        self.tx += math.cos(to_rad(self.theta))*self.speed
        self.ty += math.sin(to_rad(self.theta))*self.speed
        self.x = int(self.tx)
        self.y = int(self.ty)
        self.boundries()
        world[self.x][self.y] = self.theta
    
    def draw(self):
        screen.set_at((self.x,self.y),white)


#game_start
screen.fill(black)

for i in range(80):
    Boid()

tick = 0

while not endgame:
    tick += 1
    
    mousep = pygame.mouse.get_pos()

    if tick%2 == 0:
        for i in boids:
            i.update()
        
        for i in sharks:
            i.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endgame = True 
        if event.type == pygame.MOUSEBUTTONDOWN:
            Shark(mousep[0],mousep[1])
    
    screen.fill(black)

    for i in boids:
        i.draw()
    
    for i in obs:
        i.draw()
    
    for i in sharks:
        i.draw()

    pygame.display.update()
    clock.tick(60) 