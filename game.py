"""
Game player for AIsteroids
"""

import math
import random
from action import action

try:
    import simplegui
    import codeskulptor
    codeskulptor.set_timeout(120)

except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    from SimpleGUICS2Pygame.simplegui_lib_loader import Loader

# Globals for user interface
WIDTH = 960 #! Normally 800
HEIGHT = 720 #! Normally 600
ROCK_SPEED = 1.7 #! For easier control of rock speed for AI experiment
LIVES = 1000 #! Normally 3
TRAINING_RUNS = 2

# Globals for logic
score = 0
time = 0.05
started = False
ship_angle_vel = 0
init_ship_angle_vel = 0.15 #! Normally 0.05

acc = 0.9
friction = 0.96
missile_extra_vel = 8
max_rocks = 8
rock_spawn_padding = 5

rock_vel_multiplier_factor = 0.35
free_lives = False
extra_lives_set = set([])
extra_life_multple = 0

while extra_life_multple < 1000000:
    extra_life_multple += 1000
    extra_lives_set.add(extra_life_multple)

life_given = False
lives = LIVES #! For AI setup to easily change number of lives

# Initialize sets
rock_group = set([])
missile_group = set([])
explosion_group = set([])
explosion_group_ship = set([])

# Class definitions
class ImageInfo:
    '''
    For manipulating images used in the game
    '''
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
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


# Art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
# Debris images: debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png,
#     debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# Nebula images: nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# Splash image:
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# Ship image:
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# Missile images: shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# Asteroid images: asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# Animated explosions: explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# Sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# Helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


class Ship:
    """
    Ship class generates player's ship.
    """
    global ship_angle_vel
    def __init__(self, pos, vel, angle, image, info):
        """
        Initializes ship's state - position, initial physics,
        and radius for calculations.
        """
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.launch = False

    def draw(self,canvas):
        """
        Draws ship shown with fire when thrusting, without fire when not.
        """
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] +
            self.image_size[0], self.image_center[1]],self.image_size,
            self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
            self.pos, self.image_size, self.angle)

    def update(self):
        """
        Update's ships position and associated physics with each game loop.
        """
        global friction, acc
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * acc
            self.vel[1] += forward[1] * acc
        self.vel[0] *= friction
        self.vel[1] *= friction
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += ship_angle_vel

    def thrusters(self, upkey_or_downkey):
        """
        Used to add sound when thrusters are turned on.
        """
        global acc
        self.thrust = upkey_or_downkey
        if display:
            if self.thrust:
                ship_thrust_sound.play()
            else:
                ship_thrust_sound.rewind()

    def shoot(self):
        """
        Fires a missle in the direction that the ship is pointing.
        Max number of allowed missles defined in globals above.
        """
        global a_missile, missile_extra_vel
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + forward[0] * self.radius, self.pos[1] +
                       forward[1] * self.radius]
        missile_vel = [self.vel[0] + forward[0] * missile_extra_vel,
                       self.vel[1] + forward[1] * missile_extra_vel]
        missile_group.add(Sprite(missile_pos, missile_vel, 0, 0, missile_image,
        missile_info, missile_sound))


class Sprite:
    """
    Generates non-ship sprites, ie. asteroids and bullets.
    """
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.image = image
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle_vel = ang_vel
        self.angle = ang
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if display:
            if sound:
                sound.rewind()
                sound.play()

    def draw(self, canvas):
        """
        Redraws the sprite on each update.
        If animated, a change to the tile center is made.
        """
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] +
                              self.image_size[0] * (self.age + 1),
                              self.image_center[1]], self.image_size, self.pos,
                              self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        """
        Updates each sprite's position and age.
        Age is used for defining how long a missle would stay on screen.
        """
        pos_or_neg = random.choice([-1, 1])
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False

    def collide(self, other_object, buffer=0):
        """
        Returns true if ship or sprite, and another sprite
        collide. This is based on the radii of their combined
        images.
        """
        tot_distance = dist(self.pos, other_object.pos)
        combined_radii = self.radius + other_object.radius
        if tot_distance < combined_radii + buffer:
            return True
        else:
            return False

    def zone(self, other_object, inner_buffer=1, outer_buffer=100):
        """
        Returns true if ship or sprite, and another sprite
        collide. This is based on the radii of their combined
        images.
        """
        tot_distance = dist(self.pos, other_object.pos)
        combined_radii = self.radius + other_object.radius
        inner_edge = combined_radii + inner_buffer
        outer_edge = combined_radii + outer_buffer
        if tot_distance > inner_edge and tot_distance < outer_edge:
            return True
        else:
            return False


def click(pos):
    """
    Originally a mouseclick handler that reset UI.
    Also set conditions whether splash image is drawn.
    Or for this game, by calling click and giving a position for the ship.
    """
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = LIVES
        if display:
            soundtrack.rewind()
            soundtrack.play()


def group_collide(group, other_object):
        copy_of_group = set(group)
        collision = False
        for item in copy_of_group:
            collision = item.collide(other_object)
            if collision:
                explosion_group.add(Sprite(item.pos, item.vel, 0, 0,
                                           explosion_image, explosion_info,
                                           explosion_sound))
                group.remove(item)
                if other_object.image == ship_image:
                    explosion_group_ship.add(Sprite(my_ship.pos, my_ship.vel, 0, 0,
                                           explosion_image2, explosion_info,
                                           explosion_sound))
                return collision


def group_collide(group, other_object):
        copy_of_group = set(group)
        collision = False
        for item in copy_of_group:
            collision = item.collide(other_object)
            if collision:
                explosion_group.add(Sprite(item.pos, item.vel, 0, 0,
                                           explosion_image, explosion_info,
                                           explosion_sound))
                group.remove(item)
                if other_object.image == ship_image:
                    explosion_group_ship.add(Sprite(my_ship.pos, my_ship.vel, 0, 0,
                                           explosion_image2, explosion_info,
                                           explosion_sound))
                return collision


def group_zone(group, other_object, inner_buff, outer_buff):
        copy_of_group = set(group)
        zone = False
        for item in copy_of_group:
            zone = item.zone(other_object, inner_buff, outer_buff)
            if zone:
                return zone


def group_group_collide(group, other_group):
        copy_of_group = set(group)
        collision = False
        num_collisions = 0
        for item in copy_of_group:
            collision = group_collide(other_group, item)
            if collision:
                num_collisions += 1
                group.discard(item)
        return num_collisions


def process_sprite_group(a_set):
    copy_of_a_set = set(a_set)
    for item in copy_of_a_set:
        time_to_die = item.update()
        if time_to_die:
            a_set.remove(item)


def process_sprite_group_1(a_set, canvas):
    copy_of_a_set = set(a_set)
    for item in copy_of_a_set:
        if display:
            item.draw(canvas)
        time_to_die = item.update()
        if time_to_die:
            a_set.remove(item)

zone1_count = 0
zone2_count = 0
zone3_count = 0
def ai(in_zone1, in_zone2, in_zone3):
    """
    Put your AI function here
    """
    global zone1_count, zone2_count, zone3_count
    global ship_angle_vel

    thrustit = random.randint(0, 1000)
    # print time

    # Check if in zone
    if in_zone1:
        zone1_count += 1
    if in_zone2:
        zone2_count += 1
    if in_zone3:
        zone3_count += 1

    # Count times in zone
    if (time - 0.05) % 100 == 0:
        print "\nGame Loops:", time - 0.05, "Times Killed:", -(lives - 1000)
        print "Rocks Destroyed:", score / 100
        print "zone1:", zone1_count, "zone2:", zone2_count, "zone3:", zone3_count

    '''
    # Make Ship Thrust
    if thrustit < 500 and in_zone2 or in_zone1:
        my_ship.thrusters(True)
    elif thrustit < 10:
        my_ship.thrusters(True)
    else:
        my_ship.thrusters(False)

    # Make Ship Shoot
    shootit = random.randint(0, 1000)
    if in_zone2 and shootit < 500:
        my_ship.shoot()
    elif shootit < 5:
        my_ship.shoot()

    # Make Ship Turn
    if  6.283 < my_ship.angle or my_ship.angle < -6.283:
        my_ship.angle = 0.0
    direction = random.choice([-0.15,0,0,0,0,0,0,0,0,0,0,0,0,0.15,0.15,0.15,0.15])
    my_ship.angle += direction
    '''

    #########TESTING
    action(['moveF', 12], my_ship)

#@! def draw(canvas):
def draw_1():
    global time, started, lives, score, rock_group, life_given

    # animiate background
    time += 1

    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    '''#@!
    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (
                      wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (
                      wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    '''#@!

    # draw score and lives
    '''#@!
    canvas.draw_text("Lives", (WIDTH * 0.25, HEIGHT * 0.1), 28, "White")
    canvas.draw_text(str(lives), (WIDTH * 0.25, HEIGHT * 0.2), 42, "White")
    canvas.draw_text("Score", (WIDTH * 0.67, HEIGHT * 0.1), 28, "White")
    canvas.draw_text(str(score), (WIDTH * 0.67, HEIGHT * 0.2), 42, "White")
    '''

    # draw ship and sprites
    #@! my_ship.draw(canvas)
    '''#@!
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    process_sprite_group(explosion_group_ship, canvas)
    '''
    process_sprite_group(rock_group)
    process_sprite_group(missile_group)
    process_sprite_group(explosion_group)
    process_sprite_group(explosion_group_ship)

    # update ship and sprites
    my_ship.update()

    # check for missle/rock collisions
    missiles_hit_rocks = group_group_collide(missile_group, rock_group)
    score += missiles_hit_rocks * 100

    # free lives if score 10,000
    if free_lives:
        if score in extra_lives_set and (not life_given):
            lives += 1
            life_given = True
        elif score not in extra_lives_set:
            life_given = False


    # check for ship/rock collisions
    ship_hit_rocks = group_collide(rock_group, my_ship)
    if ship_hit_rocks:
        lives -= 1
        # check if game over
        if lives <= 0:
            started = False


    # draw splash screen if not started
    if not started:
        rock_group = set([])
        soundtrack.pause()
        '''#@!
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())
        '''


    """ Use this for AI if you want"""
    # check if rocks are in the ship's zone
    rocks_in_zone1 = group_zone(rock_group, my_ship, 2, 50)
    rocks_in_zone2 = group_zone(rock_group, my_ship, 51, 100)
    rocks_in_zone3 = group_zone(rock_group, my_ship, 101, 150)


    if started:
        """Call your AI code here"""
        ai(rocks_in_zone1, rocks_in_zone2, rocks_in_zone3)


def draw(canvas):
    global time, started, lives, score, rock_group, life_given

    # animiate background
    time += 1

    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()

    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (
                      wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (
                      wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))


    # draw score and lives

    canvas.draw_text("Lives", (WIDTH * 0.25, HEIGHT * 0.1), 28, "White")
    canvas.draw_text(str(lives), (WIDTH * 0.25, HEIGHT * 0.2), 42, "White")
    canvas.draw_text("Score", (WIDTH * 0.67, HEIGHT * 0.1), 28, "White")
    canvas.draw_text(str(score), (WIDTH * 0.67, HEIGHT * 0.2), 42, "White")


    # draw ship and sprites
    my_ship.draw(canvas)

    process_sprite_group_1(rock_group, canvas)
    process_sprite_group_1(missile_group, canvas)
    process_sprite_group_1(explosion_group, canvas)
    process_sprite_group_1(explosion_group_ship, canvas)

    # update ship and sprites
    my_ship.update()

    # check for missle/rock collisions
    missiles_hit_rocks = group_group_collide(missile_group, rock_group)
    score += missiles_hit_rocks * 100

    # free lives if score 10,000
    if free_lives:
        if score in extra_lives_set and (not life_given):
            lives += 1
            life_given = True
        elif score not in extra_lives_set:
            life_given = False


    # check for ship/rock collisions
    ship_hit_rocks = group_collide(rock_group, my_ship)
    if ship_hit_rocks:
        lives -= 1
        # check if game over
        if lives <= 0:
            started = False


    # draw splash screen if not started
    if not started:
        rock_group = set([])
        soundtrack.pause()

        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())



    """ Use this for AI if you want"""
    # check if rocks are in the ship's zone
    rocks_in_zone1 = group_zone(rock_group, my_ship, 2, 50)
    rocks_in_zone2 = group_zone(rock_group, my_ship, 51, 100)
    rocks_in_zone3 = group_zone(rock_group, my_ship, 101, 150)


    if started:
        """Call your AI code here"""
        ai(rocks_in_zone1, rocks_in_zone2, rocks_in_zone3)


# timer handler that spawns a rock
def rock_spawner():
    global rock_group, score, rock_vel_multiplier_factor
    # rock_vel_multiplier = (score // 1000 + 1) * rock_vel_multiplier_factor
    rock_vel_multiplier = ROCK_SPEED #! for the ai game
    if len(rock_group) <= max_rocks - 1 and started:
        a_rock_pos = [random.choice(range(WIDTH)),
                      random.choice(range(HEIGHT))]
        a_rock_vel = [random.choice([-1.5, -1, -0.5, 0.5, 1, 1.5]) *
                      rock_vel_multiplier,
                      random.choice([-1.5, -1, -0.5, 0.5, 1, 1.5]) *
                      rock_vel_multiplier]
        a_rock_angle_vel = random.choice([-0.02, -0.01, 0.01, 0.02])
        a_rock_image = random.choice([asteroid_image, asteroid_image2])
        potential_rock = Sprite(a_rock_pos, a_rock_vel, 0, a_rock_angle_vel,
                                a_rock_image, asteroid_info)
        if potential_rock.collide(my_ship, rock_spawn_padding):
            pass
        else:
            rock_group.add(potential_rock)

# key down handler
def keydown(key):
    global ship_angle_vel
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters(True)
    elif key == simplegui.KEY_MAP["right"]:
        ship_angle_vel += init_ship_angle_vel
    elif key == simplegui.KEY_MAP["left"]:
        ship_angle_vel -= init_ship_angle_vel
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

# key up handler
def keyup(key):
    global ship_angle_vel
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters(False)
    elif key == simplegui.KEY_MAP["right"]:
        ship_angle_vel -= init_ship_angle_vel
    elif key == simplegui.KEY_MAP["left"]:
        ship_angle_vel += init_ship_angle_vel


# initialize frame

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
#frame.set_keyup_handler(keyup)
#frame.set_keydown_handler(keydown)
#frame.set_mouseclick_handler(click)


for x in xrange(TRAINING_RUNS):
    display = False
    click([WIDTH / 2, HEIGHT / 2])
    print "\n\n\n####### game_started #######"
    y = 0
    while y < 10000:
        y += 1
        draw_1()
        if y % 10 == 0:
            rock_spawner()


display = True
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)
timer.start()
frame.start()
click()
click([WIDTH / 2, HEIGHT / 2])


#timer = simplegui.create_timer(1000.0, rock_spawner)
#timer2 = simplegui.create_timer(1, draw)
# get things rolling
#timer.start()
#timer2.start()
#frame.start()
