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

class Gem(GameElement):
    IMAGE = "GreenGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (2, 1),
            (1, 2),
            (3, 2),
            (2, 3)
        ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)
    
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
            exisiting_el.interact(PLAYER)

        if exisiting_el is None or not exisiting_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)




