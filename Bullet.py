from typing import Any
import pygame
import Constants
import CircleSprite
import random
class Bullet(CircleSprite.CircleSprite):

    def __init__(self,pos,dir) -> None:
        super().__init__(pos,Constants.BULLET_SIZE,Constants.PASTEL_PURPLE)
        self.pos = pos
        self.dir = dir
    
    def update(self) -> None:
        self.setPosition((self.pos[0] + self.dir[0] + random.randint(-10,10), self.pos[1] + self.dir[1] + random.randint(-10,10)))
        


        
        