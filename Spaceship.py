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

    def __init__(self,pos,group,shoot_hold=False):
        self.action = (0,0)
        super().__init__(pos,16,Constants.PASTEL_BLUE)
        pygame.gfxdraw.aaellipse(self.image,16,16,12,4,(0,0,0))
        pygame.gfxdraw.filled_ellipse(self.image,16,16,13,5,(0,0,0))
        pygame.gfxdraw.aaellipse(self.image,16,16,4,12,(0,0,0))
        pygame.gfxdraw.filled_ellipse(self.image,16,16,5,13,(0,0,0))
        self.group = group

        self.shoot_hold = shoot_hold

        self.energy = 1000

        self.speedVec = pygame.Vector2()
        

        self.s_timer = Timer.timerLoop(0.1)
        self.fShoot = True
    
    def getAction(self,action):
        self.action = action

    
    def shoot(self):
        if len(self.group.sprites()) >= Constants.BULLET_NUMBER:
            return
        self.energy -= Constants.BULLET_ENERGY
        match self.action[1]:
                    case 0:
                        angle = 0
                    case 1:
                        angle = -135
                    case 2:
                        angle = -90
                    case 3:
                        angle = -45
                    case 4:
                        angle = 0
                    case 5:
                        angle = 45
                    case 6:
                        angle = 90
                    case 7:
                        angle = 135
                    case 8:
                        angle = 180
        vector = pygame.math.Vector2(Constants.BULLET_SPEED,0).rotate(angle)
        self.group.add(Bullet.Bullet(self.pos,vector))

    def outofBounderies(self,pos):
        return pos[0] < 0 or pos[0] > Constants.BOUNDERIES[0] or pos[1] < 0 or pos[1] > Constants.BOUNDERIES[1]

    def update(self,delta) -> None:

        #delta = self.fps_clock.tick()

        if self.shoot_hold:
            shootTime = self.s_timer.completed()

        if(self.energy > 0):
            if(self.action[0] != -1):
                if not self.fShoot:
                    self.fShoot = True
                    self.s_timer.reset()
                
                match self.action[1]:
                    case 0:
                        angle = 0
                    case 1:
                        angle = -135
                    case 2:
                        angle = -90
                    case 3:
                        angle = -45
                    case 4:
                        angle = 0
                    case 5:
                        angle = 45
                    case 6:
                        angle = 90
                    case 7:
                        angle = 135
                    case 8:
                        angle = 180

                
                speed = self.action[0] * Constants.SPACESHIP_SPEED * delta/10

                self.energy -= math.ceil(speed)
                
                vector = pygame.math.Vector2(speed,0).rotate(angle)

                self.speedVec = vector

                nextPos = (round(self.pos[0] + vector[0]),round(self.pos[1] + vector[1]))
                if not self.outofBounderies(nextPos):
                    self.setPosition(nextPos)
                
            else:
                if self.shoot_hold:
                    if self.fShoot:
                        self.shoot()
                        self.fShoot = False
                    else:
                        if shootTime:
                            self.shoot()
                else:
                    self.shoot()

