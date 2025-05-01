from typing import Any
import CircleSprite
import Constants
import pygame.gfxdraw
import random
import math

class Bouncer(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        pos2 =  (pos[0] - Constants.BOUNCER_RADIUS, pos[1] - Constants.BOUNCER_RADIUS)

        self.rect = pygame.rect.Rect(pos2,(2*Constants.BOUNCER_RADIUS,2*Constants.BOUNCER_RADIUS))
        self.radius = Constants.BOUNCER_RADIUS
        self.pos = pos

        self.image = Constants.BOUNCER_IMAGE

        self.dir = [random.randint(-2,2),random.randint(-1,1)]
        if self.dir[0] == 0:
            self.dir[0] = 1

        if self.dir[1] == 0:
            self.dir[1] = 1
    
    def setPosition(self, pos):
        self.rect.move_ip(-self.pos[0] + pos[0],-self.pos[1] + pos[1])
        self.pos = pos

    def update(self,delta) -> None:    
        if(self.pos[0] > Constants.BOUNDERIES[0] or self.pos[0] < 0):
            self.dir[0] *= -1
            self.dir[1] = random.randint(-1,1) * Constants.BOUNCER_SPEED * (delta / 1000)
        if(self.pos[1] > Constants.BOUNDERIES[1] or self.pos[1] < 0):
            self.dir[1] *= -1
            self.dir[0] = random.randint(-1,1) * Constants.BOUNCER_SPEED  * (delta / 1000)
        
        self.setPosition((self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]))
        