import pygame
import math
import StateBulb
import Constants
class StateDisplay(pygame.sprite.Group):
    def __init__(self,pos,radius):
        super().__init__()
        self.pos = pos
        self.radius = radius
        for i in range(8):
            bPos = (pos[0] + radius*math.cos((2*math.pi/8)*i), pos[1] + radius*math.sin((2*math.pi/8)*i))
            bulb = StateBulb.StateBulb(Constants.MAX_REWARD,0)
            bulb.setPosition(bPos)
            self.add(bulb)
        
    def update(self,state):
        for i in range(3,11):
            self.sprites()[i - 3].setState(state[i])
