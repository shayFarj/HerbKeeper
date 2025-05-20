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
            bulb = StateBulb.StateBulb(Constants.MAX_REWARD,0,(10,10,10),(0,255,0))
            bulb.setPosition(bPos)
            self.add(bulb)

        for i in range(8):
            bPos = (pos[0] + 96 + radius*math.cos((2*math.pi/8)*i), pos[1] + radius*math.sin((2*math.pi/8)*i))
            bulb = StateBulb.StateBulb(0,-Constants.MAX_PUNISH,(255,0,0),(10,10,10))
            bulb.setPosition(bPos)
            self.add(bulb)

        for i in range(8):
            bPos = (pos[0] +192 + radius*math.cos((2*math.pi/8)*i), pos[1] + radius*math.sin((2*math.pi/8)*i))
            bulb = StateBulb.StateBulb(-Constants.MAX_PUNISH/10,Constants.MAX_PUNISH/10,(255,0,0),(0,255,0),mid_color=(10,10,10))
            bulb.setPosition(bPos)
            self.add(bulb)


        
    def update(self,state):
        for i in range(3,Constants.STATE_LEN):
            self.sprites()[i - 3].setState(state[i])
