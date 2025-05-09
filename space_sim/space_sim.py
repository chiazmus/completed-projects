import pygame
import random
import math
from langchain_ollama import OllamaLLM

'''To Make:
- Add a PlayerShip class that can move from star system to star system (distance is 1 fuel per AU)
- Add a system allowing the player to visit different planets in a system and take resources from them
- Add trading stations that can be visited to trade resources for money and money for fuel/upgrades
- Add a system for upgrading the ship (speed, fuel capacity, etc)
'''

# Initialize the LLM model
model = OllamaLLM(model="gemma3:1b", temperature=1, max_tokens=500)

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH*2, HEIGHT*2))
pygame.display.set_caption("Space Simulation")
font = pygame.font.Font("jetbrains-mono.ttf", 36)
smallfont = pygame.font.Font("jetbrains-mono.ttf", 16)
tinyfont = pygame.font.Font("jetbrains-mono.ttf", 8)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

GRAVITY = 0.0001

# Description Box Area
DESC_BOX_X = 50
DESC_BOX_Y = 150 # Position it near the top left
DESC_BOX_WIDTH = 300  # Give it some padding from the screen edge
DESC_BOX_HEIGHT = 600 # Height of the box

mouse_pos = (0, 0)
mouse_sel = None
planet_sel = None
visiting_planet = None
description = ''

def generate_unique_attribute():
    if random.random() < 0.3:
        return random.choice(["This planet appears to be home to a small illicit trade station.", "Strange ruins dot the surface of this planet.",
                               "This planet exhibits unusual readings below the surface.", "There appears to be a small unauthorized human settlement on this planet.", "This planet has a variety of rare minerals",
                               "A distress signal is being brodcasted from the surface of this planet.", "This planet is tidally locked.", 
                               "This planet has several small moons, all of which appear to have ancient ruins.", "A human colony on this world seems to be over-run by a large number of undead entities.",
                               "A fleet of hostile ships is orbiting this planet.", "A powerful technomage appears to have set up base on this planet.", "This planet is the site of a huge corporate mining operation."])
    else:
        return None

def draw_triangle(surface, color, center_x, center_y, size, angle):
    """
    Draws an equilateral triangle on the given Pygame surface.

    Args:
        surface: The Pygame surface to draw on.
        color: The color of the triangle (RGB tuple or Pygame Color object).
        center_x: The x-coordinate of the triangle's center.
        center_y: The y-coordinate of the triangle's center.
        size: The length of each side of the equilateral triangle.
        angle_degrees: The rotation angle of the triangle in degrees (clockwise).
    """

    # Calculate the vertices of the triangle relative to the center
    p1_offset_x = size * math.cos(angle)
    p1_offset_y = size * math.sin(angle)

    p2_offset_x = (size) * math.cos(angle + 2 * math.pi / 3)
    p2_offset_y = (size) * math.sin(angle + 2 * math.pi / 3)

    p3_offset_x = (size) * math.cos(angle + 4 * math.pi / 3)
    p3_offset_y = (size) * math.sin(angle + 4 * math.pi / 3)

    # Calculate the absolute coordinates of the vertices
    p1 = (center_x + p1_offset_x, center_y + p1_offset_y)
    p2 = (center_x + p2_offset_x, center_y + p2_offset_y)
    p3 = (center_x + p3_offset_x, center_y + p3_offset_y)

    # Draw the polygon (triangle)
    pygame.draw.polygon(surface, color, [p1, p2, p3])

def generate_planet_description(planet_type, name="", materials="carbon"):
    """Generates a description of a planet using the LLM model."""
    unique_attribute = generate_unique_attribute()
    if unique_attribute == None:
        unique_attribute = ""
    prompt = f"""You are a simple onboard computer for a spaceship.  Generate a short description of a {planet_type} planet.  The planet's designation is {name}. {unique_attribute} 
    Don't ask any questions and keep the tone professional and brief, 3 short sentences or less."""
    response = model.invoke(prompt)
    return f"--{planet_type}--  {response.strip()} -- Scavengable Materials: {materials}"

def generate_star_system_name():
    """Generates a simple, random star system name."""
    prefixes = ["Aetheri", "Boreas", "Cygnus", "Delta", "Epsilon", "Forneus", "Gamma", "Helios", "Iota", "Jupiterian"]
    suffixes = [" Prime", " Expanse", " Reach", " Core", " Nebula", " Cluster", " Void", " Frontier", ""]
    roman_numerals = [" I", " II", " III", " IV", " V", " VI"]
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    numbers = ["-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9"]

    name_parts = [
        random.choice(prefixes),
        random.choice(suffixes),
        random.choice(["", random.choice(roman_numerals)]),
        random.choice(["", f" ({random.choice(letters)}{random.choice(numbers)})"])
    ]

    return "".join(part for part in name_parts if part)

def distance_to(position_1, position_2):
    return math.sqrt((position_1[0] - position_2[0]) ** 2 + (position_1[1] - position_2[1]) ** 2)


class Star:
    def __init__(self, x, y, vx = 0, vy = 0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = random.uniform(2.0, 4.0)
        self.color = random.choice([YELLOW, WHITE, RED])
        self.planets = []
        self.name = generate_star_system_name()
        planet_count = int(max(1, random.gauss(3, 2)))
        for i in range(planet_count):
            self.planets.append(Planet(solar_mass=self.mass, solar_position=(self.x, self.y),number=self.name + " - " + str(i)))
    
    def draw(self, size=1):
        global mouse_sel
        if size < 2:
            pygame.draw.circle(screen, self.color, (int(self.x*2), int(self.y*2)), int((self.mass)*2))

            if mouse_pos[0] > self.x*2 - 10 and mouse_pos[0] < self.x*2 + 10 and mouse_pos[1] > self.y*2 - 10 and mouse_pos[1] < self.y*2 + 10:
                pygame.draw.circle(screen, WHITE, (int(self.x*2), int(self.y*2)), int((self.mass)*size*4), width=2)
                mouse_sel = self

            for planet in self.planets:
                planet.draw()
        else:
            title = font.render(self.name, True, GREEN)
            text_rect = title.get_rect()
            text_rect.center = (WIDTH // 2, 30)
            pygame.draw.circle(screen, self.color, (int(WIDTH), int(HEIGHT)), int((self.mass)*size))

            for planet in self.planets:
                planet.draw(size=size)
            
            screen.blit(title, text_rect)
    
    def update(self):
        for planet in self.planets:
            planet.update()


class Planet:
    def __init__(self, solar_mass=2, solar_position=(0, 0), number=0):
        self.solar_position = solar_position
        self.negator = random.choice([-1, 1])
        self.orbital_radius = random.uniform(0, 10) + solar_mass*2
        #orbital speed = square root of (G * solar mass / orbital radius)
        self.orbital_speed = math.sqrt(GRAVITY * solar_mass / self.orbital_radius)
        self.solar_mass = solar_mass
        self.number = number
        self.angle = random.uniform(0, 2 * math.pi)
        self.x = (solar_position[0] + self.orbital_radius * math.cos(self.angle) )
        self.y = (solar_position[1] + self.orbital_radius * math.sin(self.angle) )
        self.type = random.choice(['forest', 'desert', 'ocean', 'mountain', 'barren', 'radioactive', 'gas giant', 'frozen', 'colonized', 'volcanic'])
        self.materials =[]
        self.description = None
        self.world_map = []

        if self.type in ("desert", "barren", "mountain", "volcanic"):
            self.color = RED
        elif self.type in ("forest", "radioactive", "colonized"):
            self.color = GREEN
        elif self.type in ("ocean", "frozen"):
            self.color = BLUE
        else:
            self.color = WHITE

        match self.type:
            case "forest":
                self.materials = ["carbon", "water", "food"]
            case "desert":
                self.materials = ["sand", "silica", "spice"]
            case "ocean":
                self.materials = ["water", "sodium", "oil"]
            case "mountain":
                self.materials = ["ore", "gems", "oil", "silica", "sodium", "carbon", "methane"]
            case "barren":
                self.materials = ["silica", "technomagical crystals", "ore", "fuel"]
            case "radioactive":
                self.materials = ["uranium", "thorium", "plutonium", "technomagical crystals"]
            case "gas giant":
                self.materials = ["hydrogen", "helium", "methane", "ammonia", "oxygen"]
            case "volcanic":
                self.materials = ["volcanic ash", "ore", "silica", "carbon", "methane"]
            case "frozen":
                self.materials = ["water", "liquid nitrogen", "carbon"]
            case "colonized":
                self.materials = ["scrap", "food", "ore", "fuel", "technomagical crystals"]

        self.materials = random.choice(self.materials)
    
    def update(self):
        self.angle += self.orbital_speed * self.negator
        self.x = (self.solar_position[0] + self.orbital_radius * math.cos(self.angle) )
        self.y = (self.solar_position[1] + self.orbital_radius * math.sin(self.angle) )
    
    def draw(self, size=1):
        global planet_sel
        if size < 2:
            screen.set_at((int(self.x*2), int(self.y*2)), self.color)
        else:
            modified_x = int((self.x - self.solar_position[0])*(size*6)) + WIDTH
            modified_y = int((self.y - self.solar_position[1])*(size*6)) + HEIGHT
            pygame.draw.circle(screen, GRAY, (int(WIDTH), int(HEIGHT)), size*self.orbital_radius*6, width=2)
            pygame.draw.circle(screen, self.color, (modified_x, modified_y), size)
            if mouse_pos[0] > modified_x - 10 and mouse_pos[0] < modified_x + 10 and mouse_pos[1] > modified_y - 10 and mouse_pos[1] < modified_y + 10:
                pygame.draw.circle(screen, WHITE, (modified_x, modified_y), size*4, width=2)
                planet_sel = self
    
    def generate_world(self, size=512):
        pass

class Ship:
    def __init__(self, solar_mass=2, solar_position=(0, 0), number=0):
        self.solar_position = solar_position
        self.negator = -1
        self.orbital_radius = random.choice([5, 6, 7, 8, 9]) + solar_mass*2
        #orbital speed = square root of (G * solar mass / orbital radius)
        self.orbital_speed = math.sqrt(GRAVITY * solar_mass / self.orbital_radius)
        self.solar_mass = solar_mass
        self.number = number
        self.angle = random.uniform(0, 2 * math.pi)
        self.x = (solar_position[0] + self.orbital_radius * math.cos(self.angle) )
        self.y = (solar_position[1] + self.orbital_radius * math.sin(self.angle) )
        self.color = WHITE
        self.speed = 2
        self.target = None
    
    def update(self):
        if self.target is None:
            self.angle += self.orbital_speed * self.negator
            self.x = (self.solar_position[0] + self.orbital_radius * math.cos(self.angle) )
            self.y = (self.solar_position[1] + self.orbital_radius * math.sin(self.angle) )
        else:
            if distance_to((self.x, self.y), (self.target.x, self.target.y)) >= 10:
                self.angle = math.atan2((self.y - self.target.y), (self.x - self.target.x))
                self.x -= ( math.cos(self.angle) * self.speed )
                self.y -= ( math.sin(self.angle) * self.speed )
            else:
                self.solar_position = (self.target.x, self.target.y)
                self.solar_mass = self.target.mass
                self.target = None

    
    def set_target(self, target):
        self.target = target
    
    def draw(self, size=1):
        if size < 2:
            #pygame.draw.circle(screen, self.color, (int(self.x*2), int(self.y*2)), 2)
            #make a triangle that is the player ship oriented at the angle
            if self.target is None:
                draw_triangle(screen, self.color, int(self.x*2), int(self.y*2), size*3, self.angle - (math.pi/2))
            else:
                draw_triangle(screen, self.color, int(self.x*2), int(self.y*2), size*3, self.angle - (math.pi))
        else:
            modified_x = int((self.x - self.solar_position[0])*(size*6)) + WIDTH
            modified_y = int((self.y - self.solar_position[1])*(size*6)) + HEIGHT
            pygame.draw.circle(screen, GRAY, (int(WIDTH), int(HEIGHT)), size*self.orbital_radius*6, width=2)
            draw_triangle(screen, self.color, modified_x, modified_y, size*2, self.angle - (math.pi/2))


def display_tile(x, y, color, text_character, tile_size):
    """Display a tile on the screen with a specific color and text character."""
    pygame.draw.rect(screen, color, (x, y, tile_size, tile_size), width=2)
    text_surface = tinyfont.render(text_character, True, color)
    text_rect = text_surface.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
    screen.blit(text_surface, text_rect)


star_systems = []
for i in range(30):
    star_systems.append(Star(x = random.randint(50, WIDTH - 50), y = random.randint(50, HEIGHT - 50)))

player = Ship()
player.set_target(star_systems[0])

stars = []

for i in range(1000):
    x = random.randint(0, WIDTH*2)
    y = random.randint(0, HEIGHT*2)
    stars.append((x, y))

npc_ships = []
for i in range(10):
    npc_ships.append(Ship(solar_mass=2, solar_position=(random.randint(0, WIDTH), random.randint(0, HEIGHT))))
    npc_ships[-1].color = random.choice([YELLOW, GREEN, RED])
    npc_ships[-1].set_target(random.choice(star_systems))

def draw_starfield():
    for star in stars:
        screen.set_at(star, GRAY)

def update_npc_ships():
    for ship in npc_ships:
        ship.update()
        if random.random() < 0.0003:
            ship.set_target(random.choice(star_systems))

def draw_npc_ships(size=1):
    for ship in npc_ships:
        if size == 1:
            ship.draw()
        else:
            if ship.solar_position == player.solar_position:
                ship.draw(size=size)

def display_systems():
    for i in star_systems:
        i.draw()
    draw_npc_ships()
    player.draw()

def draw_text_wrapped(surface, text, font, color, rect):
    """Draws text wrapped within a given rectangle."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word fits
        test_line = current_line + word + " "
        text_width, text_height = font.size(test_line)

        if text_width <= rect.width:
            current_line = test_line
        else:
            # Word doesn't fit, finalize current line and start new one
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line) # Add the last line

    y = rect.top
    line_spacing = font.get_linesize()

    for line in lines:
        if y + line_spacing <= rect.bottom: # Check if line fits vertically
            line_surface = font.render(line.strip(), True, color)
            surface.blit(line_surface, (rect.left, y))
            y += line_spacing

def display_planetary_system(system):
    global description
    system.draw(size=4)
    draw_npc_ships(size=4)
    player.draw(size=4)
    if description != '':
        desc_rect = pygame.Rect(DESC_BOX_X, DESC_BOX_Y, DESC_BOX_WIDTH, DESC_BOX_HEIGHT)
        draw_text_wrapped(screen, description, smallfont, WHITE, desc_rect)
    display_tile(WIDTH*2-50, 50, GREEN, 'S', 16)


# Main game loop
running = True
sys_display = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not sys_display and (mouse_sel.x, mouse_sel.y) != player.solar_position:
                player.set_target(mouse_sel)
            else:
                if planet_sel == None:
                    sys_display = not sys_display
                    description = ''
                else:
                    if planet_sel.description is None:
                        planet_sel.description = generate_planet_description(planet_type=planet_sel.type, name=planet_sel.number,materials=planet_sel.materials)
                    description = planet_sel.description
                    planet_sel = None


    for i in star_systems:
        i.update()
    
    update_npc_ships()

    player.update()

    mouse_pos = pygame.mouse.get_pos()
    # Clear the screen (fill with black) before drawing
    screen.fill(BLACK)

    draw_starfield()

    if sys_display:
        # Draw the star systems
        display_planetary_system(mouse_sel)
    else:
        display_systems()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate (optional)
    pygame.time.Clock().tick(60)  # Adjust for desired speed

# Quit Pygame
pygame.quit()