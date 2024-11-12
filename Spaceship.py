from typing import Any
import pygame
import pygame.gfxdraw
import CircleSprite
import Constants
import pygame.math
import math
import Bullet
import Timer


class SpaceShip(CircleSprite.CircleSprite):

    def __init__(self,pos,group):
        self.action = (0,0)
        super().__init__(pos,16,Constants.PASTEL_BLUE)
        pygame.gfxdraw.aaellipse(self.image,16,16,12,4,(0,0,0))
        pygame.gfxdraw.filled_ellipse(self.image,16,16,13,5,(0,0,0))
        pygame.gfxdraw.aaellipse(self.image,16,16,4,12,(0,0,0))
        pygame.gfxdraw.filled_ellipse(self.image,16,16,5,13,(0,0,0))
        self.group = group

        self.energy = 0

        self.fps_clock = pygame.time.Clock()

        self.s_timer = Timer.timerLoop(0.1)
        self.fShoot = True
    
    def getAction(self,action):
        self.action = action

    
    def shoot(self):
        self.energy -= Constants.BULLET_ENERGY
        angle = self.action[1]
        vector = pygame.math.Vector2(Constants.BULLET_SPEED,0).rotate(angle)
        self.group.add(Bullet.Bullet(self.pos,vector))

    def outofBounderies(self,pos):
        return pos[0] < 0 or pos[0] > Constants.BOUNDERIES[0] or pos[1] < 0 or pos[1] > Constants.BOUNDERIES[1]

    def update(self) -> None:

        delta = self.fps_clock.tick()

        shootTime = self.s_timer.completed()

        if(self.energy > 0):
            if(self.action[0] != -1):
                if not self.fShoot:
                    self.fShoot = True
                    self.s_timer.reset()
                angle = self.action[1]
                speed = self.action[0] * Constants.SPACESHIP_SPEED * delta/10

                self.energy -= math.ceil(speed)
                
                vector = pygame.math.Vector2(speed,0).rotate(angle)


                nextPos = (round(self.pos[0] + vector[0]),round(self.pos[1] + vector[1]))
                if not self.outofBounderies(nextPos):
                    self.setPosition(nextPos)
                
            else:
                if self.fShoot:
                    self.shoot()
                    self.fShoot = False
                else:
                    if shootTime:
                        self.shoot()

