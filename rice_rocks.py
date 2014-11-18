# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
ANGLE_VEL = 0.15
FRICT_CONST = 0.18
SPRITE_ANGLE_VEL = 0.1

score = 0
lives = 3
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 150)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def generate_randoms(a, b):    
    return a + (b-a) * random.random()

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):                
        self.angle  += self.angle_vel        
        fwd_vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += fwd_vector[0]
            self.vel[1] += fwd_vector[1]
        
        self.vel[0] *= (1 - FRICT_CONST)
        self.vel[1] *= (1 - FRICT_CONST)
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1] 
        
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
    def change_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
       
    def update_thrust(self, flag):
        self.thrust = flag
        if flag:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
   
    def shoot(self):
        global missile_group
        fwd_vector = angle_to_vector(self.angle)
        vel = [0, 0]
        vel[0] = self.vel[0] + fwd_vector[0]
        vel[1] = self.vel[1] + fwd_vector[1]
        pos = [0, 0]
        pos[0] = self.radius * fwd_vector[0] + self.pos[0]
        pos[1] = self.radius * fwd_vector[1] + self.pos[1]
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):        
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
        self.age += 1
        if self.age >= self.lifespan:           
            return True
        else:            
            return False
        
    def collide(self, other_object):
        r1 = self.radius
        pos1 = self.pos
        r2 = other_object.get_radius()
        pos2 = other_object.get_position()
        distance = dist(pos1, pos2)
        if distance <= r1 + r2:
            return True
        else:
            return False
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    

def group_collide(group, other_object):
    if other_object == None:
        return False
    collided_obj = set()
    for sprite in group:
        if sprite.collide(other_object):
            collided_obj.add(sprite)
            
    if len(collided_obj) >= 1:
        group.difference_update(collided_obj)
        return True
    else:
        return False

def group_group_collide(sprites1, sprites2):
    grp1 = set(sprites1)
    grp2 = set(sprites2)
    tmp = set([])
    cnt = 0
    for sprite in grp1:
        if group_collide(grp2, sprite):
            tmp.add(sprite)
            cnt += 1
            sprites1.discard(sprite)    
    return cnt
            
def process_sprite_group(canvas, sprites):        
    remove_set = set()
    for sprite in sprites:
        if sprite.update():
            remove_set.add(sprite)
        sprite.draw(canvas)
    
    sprites.difference_update(remove_set)
        
def draw(canvas):
    global time, rock_group, lives, score, started
    global soundtrack
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    #draw score and lives
    canvas.draw_text("Lives", [40, 40], 25, "white", "serif")
    canvas.draw_text(str(lives), [40, 70], 25, "white", "serif")
    canvas.draw_text("Score", [WIDTH - 100, 40], 25, "white", "serif")
    canvas.draw_text(str(score), [WIDTH - 100, 70], 25, "white", "serif")
    
    if lives == 0:
        started = False
        

    # draw ship and sprites
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        rock_group = set()
        soundtrack.pause()
        return
        
    my_ship.draw(canvas)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    
    
    # update ship and sprites
    my_ship.update()    
    if group_collide(rock_group, my_ship):
        lives -= 1
        
    score += group_group_collide(rock_group, missile_group)
    
    

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    
    position = [random.randrange(0, WIDTH),  random.randrange(0, HEIGHT)]
    vel = [generate_randoms(-1, 1), generate_randoms(-1, 1)]
    angle_vel = generate_randoms(-0.1, 0.1)    
    a_rock = Sprite(position, vel, 0, angle_vel, asteroid_image, asteroid_info)
    if len(rock_group) < 12:
        rock_group.add(a_rock)

def key_down(key):
    global my_ship
    if key == simplegui.KEY_MAP['right']:        
        my_ship.change_angle_vel(ANGLE_VEL)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.change_angle_vel(-1 * ANGLE_VEL)        
    elif key == simplegui.KEY_MAP['up']:
        my_ship.update_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
    

def key_up(key):
    global my_ship
    if key == simplegui.KEY_MAP['left']:
        my_ship.change_angle_vel(0)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.change_angle_vel(0)        
    elif key == simplegui.KEY_MAP['up']:
        my_ship.update_thrust(False)
    
def click(pos):
    global started, lives, score, soundtrack
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    print "In click", started
    if not started:# and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
       
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0.5, 0.5], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

