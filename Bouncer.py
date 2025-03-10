from typing import Any
import CircleSprite
import Constants
import pygame.gfxdraw
import random
import math

BOUNCER_IMAGE = pygame.Surface((Constants.BOUNCER_RADIUS*2,Constants.BOUNCER_RADIUS*2),pygame.SRCALPHA)

pygame.gfxdraw.aacircle(BOUNCER_IMAGE,Constants.BOUNCER_RADIUS,Constants.BOUNCER_RADIUS,Constants.BOUNCER_RADIUS - 1,Constants.PASTEL_RED)
pygame.gfxdraw.filled_circle(BOUNCER_IMAGE, Constants.BOUNCER_RADIUS, Constants.BOUNCER_RADIUS, Constants.BOUNCER_RADIUS - 1,Constants.PASTEL_RED)

pygame.gfxdraw.aapolygon(BOUNCER_IMAGE,[(2,8),(22,8),(12,23)],(0,0,0))
pygame.gfxdraw.filled_polygon(BOUNCER_IMAGE,[(2,8),(22,8),(12,23)],(0,0,0))

class Bouncer(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        pos2 =  (pos[0] - Constants.HERB_RADIUS, pos[1] - Constants.HERB_RADIUS)

        self.rect = pygame.rect.Rect(pos2,(2*Constants.HERB_RADIUS,2*Constants.HERB_RADIUS))
        self.radius = Constants.HERB_RADIUS
        self.pos = pos

        self.dir = [random.randint(-2,2),random.randint(-1,1)]
        if self.dir[0] == 0:
            self.dir[0] = 1

        if self.dir[1] == 0:
            self.dir[1] = 1
    
    def update(self,delta) -> None:    
        if(self.pos[0] > Constants.BOUNDERIES[0] or self.pos[0] < 0):
            self.dir[0] *= -1
            self.dir[1] = random.randint(-1,1)
        if(self.pos[1] > Constants.BOUNDERIES[1] or self.pos[1] < 0):
            self.dir[1] *= -1
            self.dir[0] = random.randint(-1,1)
        self.setPosition((self.pos[0] + self.dir[0] * math.ceil(delta/10), self.pos[1] + self.dir[1]* math.ceil(delta/10)))
        