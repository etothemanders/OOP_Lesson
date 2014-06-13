import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
from random import choice, randint

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
CURRENT_LEVEL = None
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#####################

#### Put class definitions here ####
class Level(object):
    current_level = 1
    new_level= {}
    chest_location = None

    def make_next_level(self):
        #recreate the level_dict with empty values
        for x in range(GAME_WIDTH):
            for y in range(GAME_HEIGHT):
                if GAME_BOARD.get_el(x, y) == PLAYER:
                    pass
                else:
                    self.new_level[(x,y)] = ''

        # add the chest
        chest = choice(self.new_level.keys())
        self.chest_location = chest

        self.new_level[chest] = 'Chest'
        #add the green gem not on the chest or the edge

        while True:
            rand_x = randint(1, GAME_WIDTH - 2)
            rand_y = randint(1, GAME_HEIGHT - 2)

            if chest != (rand_x, rand_y):
                self.new_level[(rand_x, rand_y)] = 'Gem'
                gem_location = (rand_x, rand_y)
                break
            else:
                pass

        print chest, gem_location        
        #add random trees and rocks                
        num_objects = 0
        while num_objects < 4:
            extra_object = choice(['Rock','Tree'])
            rand_x = randint(0, GAME_WIDTH - 1)
            rand_y = randint(0, GAME_HEIGHT - 1)
            if chest != (rand_x, rand_y) and gem_location != (rand_x, rand_y):
                self.new_level[(rand_x, rand_y)] = extra_object
                num_objects += 1
            else:
                pass    

        return self.new_level        

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

    def move_forward(self, direction):
        return (self.x, self.y)

class Character(GameElement):
    IMAGE = "Horns"

class GreenGem(GameElement):
    IMAGE = "OrangeGem"
    SOLID = True
    level_portal = 'Chest'

    def level_up(self, x, y):
        portal_location = CURRENT_LEVEL.chest_location

        if (x, y) == portal_location:
            Level.current_level += 1
            GAME_BOARD.draw_msg("You made it to level %d!" % Level.current_level)
            next_level = CURRENT_LEVEL.make_next_level()
            draw_board(next_level)


class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def move_forward(self, direction):
        return (self.x, self.y)

class Person(GameElement):
    IMAGE = "Boy"
    SOLID = True

    def interact(self, direction):
        GAME_BOARD.draw_msg("Push the gem into the chest.")
        return(self.x, self.y)

    def move_forward(self, direction):
        return (self.x, self.y)

class Tree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

    def move_forward(self, direction):
        return (self.x, self.y)

CHARACTERS = {
    "Boy": Person,
    "Gem": GreenGem,
    "Chest": Chest,
    "Tree": Tree,
    "Rock": Rock,
}
####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    global PLAYER
    PLAYER = Character()
    global CURRENT_LEVEL
    CURRENT_LEVEL = Level()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 0, PLAYER)

    level_one = CURRENT_LEVEL.make_next_level()
    draw_board(level_one)

 
def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg() 

    if direction:
        next_player = PLAYER.move_forward(direction)
        next_x = next_player[0]
        next_y = next_player[1]      

        exisiting_el = GAME_BOARD.get_el(next_x, next_y)

        if exisiting_el:
            next_existing_el = exisiting_el.move_forward(direction)
            GAME_BOARD.del_el(exisiting_el.x, exisiting_el.y)
            GAME_BOARD.set_el(next_existing_el[0], next_existing_el[1], exisiting_el)

        if GAME_BOARD.get_el(next_x, next_y) is None or not exisiting_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

        if exisiting_el:
            exisiting_el.level_up(next_existing_el[0], next_existing_el[1])

def draw_board(level_description):
    # clear the existing board
    for x in range(GAME_WIDTH):
            for y in range(GAME_HEIGHT):
                if GAME_BOARD.get_el(x, y) == PLAYER:
                    pass
                else:
                    GAME_BOARD.del_el(x,y)

    # use the correct level dictionary to draw the new board
    for k, v in level_description.iteritems():
        if GAME_BOARD.get_el(k[0], k[1]) == PLAYER:
            pass
        elif v == '':
            pass
        else:
            item = CHARACTERS[v]()
            GAME_BOARD.register(item)
            GAME_BOARD.set_el(k[0], k[1], item)

