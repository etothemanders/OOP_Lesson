GAME_WIDTH = 5
GAME_HEIGHT = 5


class GameElement(object):
    IMAGE = "StoneBlock"
    SOLID = False
    
    def __init__(self):
        self.sprite = None
        self.board = None
        self.x = None
        self.y = None

    def interact(self, direction):
        return (self.x, self.y)

    def __str__(self):
        return "<%s located at %r, %r>"%(type(self).__name__, self.x, self.y)

    def update(self, dt):
        pass

    def level_up(self, x, y):
        pass

    def move_forward(self, direction):
        if direction == "up" and self.y-1 >= 0:
            return (self.x, self.y-1)
        elif direction == "down" and self.y+1 < GAME_HEIGHT:
            return (self.x, self.y+1)
        elif direction == "left" and self.x-1 >= 0:
            return (self.x-1, self.y) 
        elif direction == "right" and self.x+1 < GAME_WIDTH:
            return (self.x+1, self.y)
        return (self.x, self.y)
