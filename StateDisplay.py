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
            bulb = StateBulb.StateBulb(Constants.MAX_REWARD,0,(30,30,30),(0,255,0))
            bulb.setPosition(bPos)
            self.add(bulb)

        for i in range(8):
            bPos = (pos[0] + 96 + radius*math.cos((2*math.pi/8)*i), pos[1] + radius*math.sin((2*math.pi/8)*i))
            bulb = StateBulb.StateBulb(0,Constants.MAX_PUNISH,(30,30,30),(255,0,0))
            bulb.setPosition(bPos)
            self.add(bulb)

        for i in range(8):
            bPos = (pos[0] +192 + radius*math.cos((2*math.pi/8)*i), pos[1] + radius*math.sin((2*math.pi/8)*i))
            bulb = StateBulb.StateBulb(0,Constants.MAX_REWARD/2,(30,30,30),(0,255,0))
            bulb.setPosition(bPos)
            self.add(bulb)
        
        for i in range(8):
            bPos = (pos[0] + 288 + radius*math.cos((2*math.pi/8)*i), pos[1] + radius*math.sin((2*math.pi/8)*i))
            bulb = StateBulb.StateBulb(0,Constants.MAX_REWARD,(30,30,30),(255,0,0))
            bulb.setPosition(bPos)
            self.add(bulb)


        
    def update(self,state):
        for i in range(3,Constants.STATE_LEN):
            self.sprites()[i - 3].setState(state[i])
