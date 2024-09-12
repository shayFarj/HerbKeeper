from typing import Any
import CircleSprite
import Constants
import pygame.gfxdraw
import random

class Bouncer(CircleSprite.CircleSprite):
    def __init__(self,pos):
        super().__init__(pos,12,Constants.PASTEL_RED)
        pygame.gfxdraw.aapolygon(self.image,[(2,8),(22,8),(12,23)],(0,0,0))
        pygame.gfxdraw.filled_polygon(self.image,[(2,8),(22,8),(12,23)],(0,0,0))

        self.dir = [random.randint(-2,2),random.randint(-2,2)]
        if self.dir[0] == 0:
            self.dir[0] = 1

        if self.dir[1] == 0:
            self.dir[1] = 1
    
    def update(self) -> None:
        if(self.pos[0] > Constants.BOUNDERIES[0] or self.pos[0] < 0):
            self.dir[0] *= -1
            self.dir[1] = random.randint(-2,2)
        if(self.pos[1] > Constants.BOUNDERIES[1] or self.pos[1] < 0):
            self.dir[1] *= -1
            self.dir[0] = random.randint(-2,2)
        
        self.setPosition((self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]))
        