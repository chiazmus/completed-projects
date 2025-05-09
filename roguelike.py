import keyboard
import tkinter as tk
import random
  
frame = tk.Tk()
frame.title("Roguelike")
frame.geometry('625x400')

def highlight(x,y,col):
    charpos = str(y+2)+'.'+str(x+1)
    charposn = str(y+2)+'.'+str(x+2)
    outbox.tag_add(col, charpos, charposn)
    outbox.tag_config(col, background="black", foreground=col)

def print_output(to_print):
    outbox.delete(1.0,tk.END)
    outbox.insert(tk.END,to_print)
    highlight(my_player.x,my_player.y,"yellow")
    for i in doors:
        highlight(i[0],i[1],"yellow")
    for i in treasure:
        highlight(i[0],i[1],"yellow")
    for i in monsters:
        highlight(i[0],i[1],"red")
    msgbox.delete(1.0,tk.END)
    msgbox.insert(tk.END,to_message)


# TextBox Creation
outbox = tk.Text(frame,
                   height = 22,
                   width = 47,
                   bg = 'black',
                   fg = 'white')
  
outbox.grid(columnspan=2)

msgbox = tk.Text(frame,
                   height = 10,
                   width = 30,
                   bg = 'black',
                   fg = 'white')
  
msgbox.grid(column=3,row=0,sticky='n')

narrative_box = tk.Text(frame,
                   height = 12,
                   width = 30,
                   bg = 'black',
                   fg = 'white')
  
narrative_box.grid(column=3,row=0,sticky='s')
  
# Label Creation
lbl = tk.Label(frame, text = "")
lbl.grid()

#start of real program
to_message = 'welcome to the dungeon\n'
narrative_msg = ''
width = 45
height = 20
world = []
dirx = [1,-1,0,0]
diry = [0,0,1,-1]
seen_world = []
rooms = [(4,4)]
room_size = {}
room_size[(4,4)] = (3,3)
walls = ['#','+']
darkmode = True
doors = []
madestuff = []
treasure = []
monsters = []
mongoals = {}

for y in range(height):
    world.append([])
    seen_world.append([])
    for x in range(width):
        world[-1].append('#')
        seen_world[-1].append(0)

def clear_messages():
    global to_message
    if len(to_message) > 60:
        to_message = to_message[(len(to_message)-61):]
    else:
        to_message = ''

def message(msg):
    global to_message
    to_message += '\n      ------------------      \n'
    if len(msg) > 30:
        msg = msg.split()
        msg[len(msg)//2] += ('\n' + (' ' * (((30-(len(msg)//2))//2)-1)))
        msg = ' '.join(msg)
        msg = (' ' * ((30-(len(msg)//2))//2)) + msg
    else:
        msg = (' ' * ((30-len(msg))//2)) + msg
    to_message += msg

def los(x0,y0,x1,y1):
    dx = abs(x1-x0)
    sx = 1 if x0<x1 else -1
    dy = -abs(y1-y0)
    sy = 1 if y0<y1 else -1
    err = dx+dy
    while True:
        if (x0 == x1) and (y0 == y1):
            break
        if world[y0][x0] in walls:
            return False
        e2 = 2 * err
        if e2 >= dy:
            if x0==x1:
                break
            err += dy
            x0 += sx
        if e2 <= dx:
            if y0 == y1:
                break
            err += dx
            y0 += sy       
    return True

def get_neighbors(x,y):
    nbs = []
    for i in range(4):
        if (width > (x+dirx[i]) > 0) and (height > (y+diry[i]) > 0):
            nbs.append((x+dirx[i],y+diry[i]))
    return nbs

def get_open_neighbors(x,y):
    nbs = []
    for i in range(4):
        if (width > (x+dirx[i]) > 0) and (height > (y+diry[i]) > 0):
            if world[y+diry[i]][x+dirx[i]] == '.':
                nbs.append((x+dirx[i],y+diry[i]))
    return nbs

def check_neighbor(x,y):
    nbs = 0
    if y > 0:
        nbs += (1 if world[y-1][x] == '#' else 0)
    if y < (height-1):
        nbs += (1 if world[y+1][x] == '#' else 0)
    if x > 0:
        nbs += (1 if world[y][x-1] == '#' else 0)
    if x < (width-1):
        nbs += (1 if world[y][x+1] == '#' else 0)
    return nbs

def place_treasure():
    for y in range(height):
        for x in range(width):
            if len(get_open_neighbors(x,y)) == 4 and world[y][x] == '.':
                if random.randint(1,100) <= 20:
                    world[y][x] = '$'
                    treasure.append((x,y))
                elif random.randint(1,100) <= 10:
                    world[y][x] = 'm'

def make_doors():
    for j in rooms:
        left = j[0]-(int(room_size[j][0]/2)+1)
        top = j[1]-(int(room_size[j][1]/2)+1)
        right = left+room_size[j][0]+1
        bottom = top+room_size[j][1]+1
        world[top][right] = '#'
        world[top][left] = '#'
        world[bottom][right] = '#'
        world[bottom][left] = '#'
        for x in range(left,right):
            if check_neighbor(x,top) == len(get_open_neighbors(x,top)):
                if world[top][x] == '#':
                    world[top][x] = '+'
            if check_neighbor(x,bottom) == len(get_open_neighbors(x,bottom)):
                if world[bottom][x] == '#':
                    world[bottom][x] = '+'
            if world[top][x] == '.':
                world[top][x] = '+'
            if world[bottom][x] == '.':
                world[bottom][x] = '+'
        for y in range(top,bottom):
            if check_neighbor(left,y) == len(get_open_neighbors(left,y)):
                if world[y][left] == '#':
                    world[y][left] = '+'
            if check_neighbor(right,y) == len(get_open_neighbors(right,y)):
                if world[y][right] == '#':
                    world[y][right] = '+'
            if world[y][left] == '.':
                world[y][left] = '+'
            if world[y][right] == '.':
                world[y][right] = '+'        

def carve_worm(x,y):
    global world
    stk = []
    tch = []
    world[y][x] = '.'
    stk.append((x,y))
    tch.append((x,y))
    tx = x
    ty = y
    while len(stk) > 0:
        nbs = get_neighbors(tx,ty)
        cand = []
        for i in nbs:
            if i not in tch:
                if check_neighbor(i[0],i[1]) >= 3:
                    cand.append(i)
        if len(cand) <= 0:
            popped = stk.pop()
            tx = popped[0]
            ty = popped[1]
            del(popped)
            stk = []
        else:
            sel = random.choice(cand)
            tx = sel[0]
            ty = sel[1]
            world[ty][tx] = '.'
            stk.append((tx,ty))
            tch.append((tx,ty))

def fill_holes():
    for y in range(height):
        for x in range(width):
            if check_neighbor(x,y) >= 3 and world[y][x] == '.':
                world[y][x] = '#'

def remove_usless_doors():
    for y in range(height):
        for x in range(width):
            if world[y][x] == '+':
                if len(get_open_neighbors(x,y)) == 1:
                    world[y][x] = '#'
    for y in range(height):
        for x in range(width):
            if world[y][x] == '+':
                for i in get_neighbors(x,y):
                    if world[i[1]][i[0]] == '+':
                        world[y][x] = '#'
    for y in range(height):
        for x in range(width):
            if check_neighbor(x,y) == 2 and world[y][x] == '+':
                geto = get_open_neighbors(x,y)
                if not (((x+1,y) in geto) and ((x-1,y) in geto)) or (((x,y+1) in geto) and ((x,y-1) in geto)):
                    world[y][x] = '.'
    for y in range(height):
        for x in range(width):
            if world[y][x] == '+':
                if check_neighbor(x,y) == 1:
                    geto = get_open_neighbors(x,y)
                    if (((x+1,y) in geto) and ((x-1,y) in geto)):
                        world[y+1][x] = '#'
                        world[y-1][x] = '#'
                    else:
                        world[y][x+1] = '#'
                        world[y][x-1] = '#'
                doors.append((x,y))

def carve_passage(x0,y0,x1,y1,md=False):
    ls = check_neighbor(x0,y0)
    direct = None
    while x0 != x1 or y0 != y1:
        if (world[y0][x0] == '#') and (check_neighbor(x0,y0) == 2):
            geto = get_open_neighbors(x0,y0)
            if (((x0+1,y0) in geto) and ((x0-1,y0) in geto)) or (((x0,y0+1) in geto) and ((x0,y0-1) in geto)):
                world[y0][x0] = '+'
            else:
                world[y0][x0] = '.'
        elif (world[y0][x0] == '#') and (check_neighbor(x0,y0) == 3) and (ls < 3):
            world[y0][x0] = '+'
        elif (world[y0][x0] != '+'):
            world[y0][x0] = '.'
        ls = check_neighbor(x0,y0)
        madestuff.append((x0,y0))
        if x0 != x1 and y0!=y1:
            if direct is None:
                direct = random.randint(0,1)
            if world[y0][x0 + (1 if x0 < x1 else -1)] == world[y0 + (1 if y0 < y1 else -1)][x0]:
                if direct == 1:
                    x0 += 1 if x0 < x1 else -1
                else:
                    y0 += 1 if y0 < y1 else -1
            elif world[y0][x0 + (1 if x0 < x1 else -1)] == '.':
                x0 += 1 if x0 < x1 else -1
            else:
                y0 += 1 if y0 < y1 else -1
        elif x0 != x1:
            x0 += 1 if x0 < x1 else -1
        elif y0 != y1:
            y0 += 1 if y0 < y1 else -1
    madestuff.append((x0,y0))

def build_room(h,w):
    global world
    cand = []
    for y in range(height):
        for x in range(width):
            if (height-(h+1) > y) and (width-(w+1) > x) and (x>0) and (y>0):
                test = True
                for i in range(h):
                    for j in range(w):
                        if world[y+i][x+j] == '.':
                            test = False
                for i in rooms:
                    if (abs(i[0]-x) <= (w+2)) and (abs(i[1]-y) <= (h+2)):
                        test = False
                if test:
                    cand.append((x,y))
    if len(cand) > 0:
        sel = random.choice(cand)
        for i in range(h):
            for j in range(w):
                world[sel[1]+i][sel[0]+j] = '.'
        rooms.append((sel[0]+int(w/2),sel[1]+int(h/2)))
        room_size[rooms[-1]] = (w,h)

def distance(x0,y0,x1,y1):
    acc = ((x1-x0) ** 2)
    acc += ((y1-y0) ** 2)
    acc = acc ** 0.5
    return acc

def connect_rooms():
    global rooms
    rm = [rooms.pop(random.randint(0,(len(rooms)-1)))]
    carve_passage(4,4,rm[0][0],rm[0][1])
    while len(rooms) > 0:
        
        dist = 10000

        ch2 = rooms.pop(random.randint(0,len(rooms)-1))
        
        temploc = []
        
        if random.randint(0,1) == 1:
            if ch2[0] > width/2:
                temploc = [ch2[0]-5,ch2[1]]
            else:
                temploc = [ch2[0]+5,ch2[1]]
        else:
            if ch2[1] > height/2:
                temploc = [ch2[0],ch2[1]-5]
            else:
                temploc = [ch2[0],ch2[1]+5]      
        
        for y in range(height):
            for x in range(width):
                tdist = distance(x,y,temploc[0],temploc[1])
                if (tdist < dist) and ((x,y) in madestuff):
                    dist = tdist
                    ch1 = (x,y)     

        carve_passage(ch1[0],ch1[1],ch2[0],ch2[1])
        #carve_passage(temploc[0],temploc[1],ch2[0],ch2[1],True)
        rm.append(ch2)
    rooms = rm

def simulation_step():
    tempworld=[]

    for y in range(height):
        tempworld.append([])
        for x in range(width):
            tempworld[-1].append(world[y][x])
            if check_neighbor(x,y) < 2:
                tempworld[y][x] = '.'
            elif check_neighbor(x,y) > 2:
                tempworld[y][x] = '#'
    return tempworld

for i in range(random.randint(4,8)):
    build_room(random.randint(3,5),random.randint(3,5))

world[4][4] = '.'
world[4][5] = '.'
world[4][3] = '.'
world[5][4] = '.'
world[5][5] = '.'
world[5][3] = '.'
world[3][4] = '.'
world[3][5] = '.'
world[3][3] = '.'

connect_rooms()

remove_usless_doors()

fill_holes()

place_treasure()

def move_monsters():
    global world
    tempworld=[]
    global monsters
    monsters = []

    for y in range(height):
        tempworld.append([])
        for x in range(width):
            tempworld[-1].append(world[y][x])
    
    for y in range(height):
        for x in range(width):
            if world[y][x] == 'm':
                monsters.append((x,y))
                togo = True
                if los(my_player.x,my_player.y,x,y):
                    togo = False
                    if mongoals.setdefault((x,y),None) != None:
                        togo = True
                    else:
                        message('a monster sees you!')
                    mongoals[(x,y)] = (my_player.x,my_player.y)
                if (mongoals.setdefault((x,y),None) != None) and togo:
                    cands = []
                    for i in range(4):
                        distx = abs(mongoals[(x,y)][0]-x)
                        disty = abs(mongoals[(x,y)][1]-y)
                        tempx = abs(mongoals[(x,y)][0]-(dirx[i]+x))
                        tempy = abs(mongoals[(x,y)][1]-(diry[i]+y))
                        if (distx > tempx) or (disty > tempy):
                            if world[diry[i]+y][dirx[i]+x] == '.':
                                cands.append((x+dirx[i],y+diry[i]))
                    if len(cands) > 0:
                        sel = random.choice(cands)
                        tempworld[sel[1]][sel[0]] = 'm'
                        tempworld[y][x] = '.'
                        mongoals[(sel[0],sel[1])] = mongoals[(x,y)]
                        mongoals[(x,y)] = None
                        monsters[-1] = (sel[0],sel[1])
                    else:
                        mongoals[(x,y)] = None
                        message('a monster has lost sight of you!')
    
    world = tempworld
                        


class Main_player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def move_up(self):
        if self.y > 0:
            self.y -= 1
            if world[self.y][self.x] == '#':
                self.y += 1
            elif world[self.y][self.x] == '+':
                doors.remove((self.x,self.y))
        move_monsters()
        update_seen()
    def move_down(self):
        if self.y < (height-1):
            self.y += 1
            if world[self.y][self.x] == '#':
                self.y -= 1
            elif world[self.y][self.x] == '+':
                doors.remove((self.x,self.y))
        move_monsters()
        update_seen()
    def move_left(self):
        if self.x > 0:
            self.x -= 1
            if world[self.y][self.x] == '#':
                self.x += 1
            elif world[self.y][self.x] == '+':
                doors.remove((self.x,self.y))
        move_monsters()
        update_seen()
    def move_right(self):
        if self.x < (width-1):
            self.x += 1
            if world[self.y][self.x] == '#':
                self.x -= 1
            elif world[self.y][self.x] == '+':
                doors.remove((self.x,self.y))
        move_monsters()
        update_seen()

world[5][3] = '#'

my_player = Main_player(4,4)

def update_seen():
    for y in range(height):
        for x in range(width):
            ls = los(my_player.x,my_player.y,x,y)
            if seen_world[y][x] == 0:
                if ls:
                    seen_world[y][x] = 1
            if seen_world[y][x] >= 1:
                if ls:
                    seen_world[y][x] = 2
                else:
                    seen_world[y][x] = 1


def update_world():
    for y in range(height):
        for x in range(width):
            if (x,y) == (my_player.x,my_player.y):
                if world[y][x] == '$':
                    message('you got ' + str(random.randint(1,10)) + ' gold!')
                elif world[y][x] == 'm':
                    message('you killed a monster!')
                world[y][x] = '@'
            elif (world[y][x] not in walls) and (world[y][x] not in ('$','m')):
                world[y][x] = '.'
                if (x,y) in treasure:
                    treasure.remove((x,y))

def world_string():
    string = ' '
    for x in range(width):
        string += ' '
    string += '\n'
    for y in range(height):
        string += ' '
        for x in range(width):
            if seen_world[y][x] >= 1:
                string += world[y][x]
            else:
                if darkmode:
                    string += ' '
                else:
                    string += world[y][x]
        string += ' \n'
    string += ' '
    for x in range(width):
        string += ' '
    string += '\n'
    return string

#gameloop
keypressed = False
update_seen()
while True:
    if len(to_message) > (300-30):
        clear_messages()
    update_world()
    print_output(world_string())
    if keyboard.is_pressed('q'):
        break
    elif keyboard.is_pressed('up'):
        if not keypressed:
            my_player.move_up()
            keypressed = True
    elif keyboard.is_pressed('down'):
        if not keypressed:
            my_player.move_down()
            keypressed = True
    elif keyboard.is_pressed('left'):
        if not keypressed:
            my_player.move_left()
            keypressed = True
    elif keyboard.is_pressed('right'):
        if not keypressed:
            my_player.move_right()
            keypressed = True 
    elif keyboard.is_pressed('space'):
        if not keypressed:
            keypressed = True
            darkmode = not darkmode
    else:
        keypressed = False
    frame.update()
