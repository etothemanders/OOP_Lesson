import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

######################
LEVEL1 = {
    (0, 0): '',
    (0, 1): '',
    (0, 2): '',
    (0, 3): '',
    (0, 4): '',
    (1, 0): '',
    (1, 1): '',
    (1, 2): 'Gem',
    (1, 3): '',
    (1, 4): '',
    (2, 0): '',
    (2, 1): '',
    (2, 2): '',
    (2, 3): 'Gem',
    (2, 4): '',
    (4, 0): 'Chest'
}

LEVEL2 = {
    (0, 0): 'BlueGem',
    (0, 1): 'BlueGem',
    (0, 2): 'Gem',
    (1, 0): '',
    (1, 1): '',
    (1, 2): 'BlueGem',
    (2, 0): 'BlueGem',
    (2, 1): '',
    (2, 2): 'BlueGem'
}

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Horns"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up" and self.y-1 >= 0:
            return (self.x, self.y-1)
        elif direction == "down" and self.y+1 < GAME_HEIGHT:
            return (self.x, self.y+1)
        elif direction == "left" and self.x-1 >= 0:
            return (self.x-1, self.y) 
        elif direction == "right" and self.x+1 < GAME_WIDTH:
            return (self.x+1, self.y)
        return (self.x, self.y)

    def get_inventory(self):
        return self.inventory

class Gem(GameElement):
    IMAGE = "GreenGem"
    SOLID = True

    def interact(self, player, direction):
        if direction == "up" and self.y-1 >= 0:
            return (self.x, self.y-1)
        elif direction == "down" and self.y+1 < GAME_HEIGHT:
            return (self.x, self.y+1)
        elif direction == "left" and self.x-1 >= 0:
            return (self.x-1, self.y) 
        elif direction == "right" and self.x+1 < GAME_WIDTH:
            return (self.x+1, self.y)
        return (self.x, self.y)

class BlueGem(Gem):
    IMAGE = "BlueGem"

    def interact(self):
        draw_board(LEVEL2)

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self, player):
        pass

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 0, PLAYER)

    draw_board(LEVEL1)

 
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
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]      

        exisiting_el = GAME_BOARD.get_el(next_x, next_y)

        if exisiting_el:
            next_direction = exisiting_el.interact(PLAYER, direction)
            GAME_BOARD.del_el(exisiting_el.x, exisiting_el.y)
            GAME_BOARD.set_el(next_direction[0], next_direction[1], exisiting_el)

        if GAME_BOARD.get_el(next_x, next_y) is None or not exisiting_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)


def draw_board(level):
    # clear the existing board
    for x in range(GAME_WIDTH):
            for y in range(GAME_HEIGHT):
                if GAME_BOARD.get_el(x, y) == PLAYER:
                    pass
                else:
                    GAME_BOARD.del_el(x,y)
    # use the correct level dictionary to draw the new board
    for k, v in level.iteritems():
        if GAME_BOARD.get_el(k[0], k[1]) == PLAYER:
            print k[0], k[1]
            pass
        elif v == '':
            pass
        else:
            if v == 'BlueGem':
                item = BlueGem()
            elif v == 'Gem':
                item = Gem()
            elif v == 'Chest':
                item = Chest()
            GAME_BOARD.register(item)
            GAME_BOARD.set_el(k[0], k[1], item)


