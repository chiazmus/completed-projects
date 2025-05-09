import pygame
import random
import time

pygame.init()

display_width = 600
display_height = 400

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('title')

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,155)
yellow = (155,155,0)
clock = pygame.time.Clock()
endgame = False
#globals

r_naught = 5.7
deathrate = 27
vaccinated_number = 0
immunation_days = (60*5)
space_hash = {}
people = []
toremove = []
infected_people = 1
for y in range((display_height//10)+1):
    for x in range((display_width//10)+1):
        space_hash[((x*10),(y*10))] = []
#functions

def distance(point_a,point_b):
    dist = ((point_a[0]-point_b[0])**2)
    dist += ((point_a[1]-point_b[1])**2)
    dist = dist ** (1/2)
    return dist

def display_image(x,y,img):
    screen.blit(img, (x,y))

def playsound(sound):
    pygame.mixer.Sound.play(sound)

def playsong(filepath):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)

#classes
class person:
    def __init__(self,x,y,infected=False,immune=False):
        self.masked = False
        self.temprnaught = r_naught
        self.tempdeathrate = deathrate
        self.x = x
        self.y = y
        self.dx = random.randint(-200,200)
        if self.dx != 0:
            self.dx /= 100
        self.dy = random.randint(-200,200)
        if self.dy != 0:
            self.dy /= 100
        self.infected = infected
        self.mutation_rate = 10
        self.to_infect = random.gauss(r_naught,2.0)
        self.daysinfected = 0
        self.immune = immune
        self.immune_days = 1
        self.infectedlist = []
    def update(self):
        #move
        global infected_people
        if self in space_hash[(round(self.x/10)*10,round(self.y/10)*10)]:
            space_hash[(round(self.x/10)*10,round(self.y/10)*10)].remove(self)
        self.x += self.dx
        self.y += self.dy
        if self.x > display_width:
            self.x = (self.x - display_width)
        if self.x < 0:
            self.x = (display_width + self.x)
        if self.y > display_height:
            self.y = (self.y - display_height)
        if self.y < 0:
            self.y = (self.y + display_height)
        space_hash[(round(self.x/10)*10,round(self.y/10)*10)].append(self)
        #change
        if self.immune:
            self.immune_days += 1
            if self.immune_days > immunation_days:
                self.immune_days = 1
                self.immune = False
        if self.infected:
            for i in space_hash[(round(self.x/10)*10,round(self.y/10)*10)]:
                if i is not self:
                    if (self.to_infect > 0) and (i not in self.infectedlist):
                        self.to_infect -= 1
                        if not i.immune:
                            if random.randint(0,1000) < self.tempdeathrate:
                                toremove.append(i)
                            else:
                                if not i.infected:
                                    i.to_infect = random.gauss(self.temprnaught,2.0)
                                    infected_people += 1
                                    i.temprnaught = self.temprnaught
                                    i.tempdeathrate = self.tempdeathrate
                                    if random.randint(1,100) < self.mutation_rate:
                                        i.temprnaught += (random.gauss(0.5,0.2)) * random.choice((-1,1))
                                        i.tempdeathrate += (random.gauss(2,0.5)) * random.choice((-1,1))
                                        i.mutation_rate += (random.gauss(2,0.5)) * random.choice((-1,1))
                                        if i.temprnaught < 0:
                                            i.temprnaught = 1
                                        if i.tempdeathrate < 0:
                                            i.tempdeathrate = 1
                                        if i.mutation_rate < 0:
                                            i.mutation_rate = 1
                                i.infected = True
                                self.infectedlist.append(i)
                                i.infectedlist.append(self)
            if self.to_infect <= 0:
                self.infected = False
                self.immune = True
                self.daysinfected = 0
    def display(self):
        if self.immune:
            nm = int(((self.immune_days+0.01)/400)*255)
            pygame.draw.circle(screen,(nm,nm,255),(self.x,self.y),2,1)
        else:
            if not self.infected:
                pygame.draw.circle(screen,white,(self.x,self.y),3,1)
            else:
                p1 = ((1/(abs(r_naught-self.temprnaught)+0.001))*255)
                p2 = ((1/(abs(deathrate-self.tempdeathrate)+0.001))*255)
                p3 = ((1/(abs(3-self.mutation_rate)+0.001))*155)
                p1 = 255-p1
                p2 = 255-p2
                p3 = 255-p3
                if p1 < 0:
                    p1 = 0
                if p2 < 0:
                    p2 = 0
                if p3 < 100:
                    p3 = 100
                if p1 > 255:
                    p1 = 255
                if p2 > 255:
                    p2 = 255
                if p3 > 255:
                    p3 = 255
                p1 = int(p1)
                p2 = int(p2)
                p3 = int(p3)
                color = (p3,p1,p2)
                pygame.draw.circle(screen,color,(self.x,self.y),3)


#game_start
screen.fill(black)

vaccinated_number = int(300*0.5)

for i in range(300):
    people.append(person(random.randint(0,display_width),random.randint(0,display_height)))
    if i <= vaccinated_number:
        people[-1].immune = True
people[0].immune = False
people[0].infected = True
died = 0

while not endgame:
    
    mousep = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endgame = True 
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in people:
                if (not i.infected) and (not i.immune):
                    if random.randint(0,1) == 1:
                        i.immune = True
    
    for i in people:
        i.update()
    while len(toremove) > 0:
        if toremove[-1] in people:
            people.remove(toremove[-1])
        temp = toremove.pop()
        del(temp)
        died += 1
    screen.fill(black)
    for i in people:
        i.display()
    pygame.display.update()
    clock.tick(60) 

print(str(infected_people),'infected')
print(str(died),'dead')
