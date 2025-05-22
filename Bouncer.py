from typing import Any
import CircleSprite
import Constants
import pygame.gfxdraw
import random
import math

class Bouncer(pygame.sprite.Sprite):
    def __init__(self,pos,debug = False):
        super().__init__()

        self.rect = pygame.rect.Rect(pos,(2*Constants.BOUNCER_RADIUS,2*Constants.BOUNCER_RADIUS))
        self.radius = Constants.BOUNCER_RADIUS
        self.pos = pos

        self.image = Constants.BOUNCER_IMAGE
        
        r_ang = random.random() * 2 * math.pi

        self.dir = [Constants.BOUNCER_SPEED* math.cos(r_ang) * (1 / Constants.FPS),Constants.BOUNCER_SPEED * math.sin(r_ang) * (1 / Constants.FPS)]
        self.debug = debug
    
    def setPosition(self, pos):
        self.rect.move_ip(-self.pos[0] + pos[0],-self.pos[1] + pos[1])
        self.pos = pos

    def update(self,delta) -> None:
        nPos = (round(self.pos[0] + self.dir[0]), round(self.pos[1] + self.dir[1]))
        if(nPos[0] > Constants.BOUNDERIES[0]):
            r_ang = random.uniform(math.pi / 2 + math.pi / 12, (math.pi * 3) / 2 - math.pi / 12)
            self.dir = [Constants.BOUNCER_SPEED* math.cos(r_ang) * (delta / 1000),Constants.BOUNCER_SPEED * math.sin(r_ang) * (delta / 1000)]
        
        if(nPos[0] < 0):
            r_ang = random.uniform(math.pi / 2 - math.pi / 12, -math.pi / 2 / 2 + math.pi / 12)
            self.dir = [Constants.BOUNCER_SPEED* math.cos(r_ang) * (delta / 1000),Constants.BOUNCER_SPEED * math.sin(r_ang) * (delta / 1000)]
        
        if(nPos[1] > Constants.BOUNDERIES[1]):
            r_ang = random.uniform(- math.pi / 12,-math.pi + math.pi / 12)
            self.dir = [Constants.BOUNCER_SPEED* math.cos(r_ang) * (delta / 1000),Constants.BOUNCER_SPEED * math.sin(r_ang) * (delta / 1000)]
        
        if(nPos[1] < 0):
            r_ang = -random.uniform(- math.pi / 12,-math.pi + math.pi / 12)
            self.dir = [Constants.BOUNCER_SPEED* math.cos(r_ang) * (delta / 1000),Constants.BOUNCER_SPEED * math.sin(r_ang) * (delta / 1000)]
        
        if not self.debug:
            self.setPosition((round(self.pos[0] + self.dir[0]), round(self.pos[1] + self.dir[1])))
        