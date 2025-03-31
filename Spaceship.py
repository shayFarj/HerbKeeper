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

    def __init__(self,pos):
        self.action = (0,0)
        super().__init__(pos,Constants.SPACESHIP_RADIUS,Constants.PASTEL_BLUE)
        pygame.gfxdraw.aaellipse(self.image,16,16,12,4,(0,0,0))
        pygame.gfxdraw.filled_ellipse(self.image,16,16,13,5,(0,0,0))
        pygame.gfxdraw.aaellipse(self.image,16,16,4,12,(0,0,0))
        pygame.gfxdraw.filled_ellipse(self.image,16,16,5,13,(0,0,0))

        # self.graze = CircleSprite.CircleSprite(pos,32,Constants.GREEN_DARK)

        self.energy = Constants.INIT_ENERGY #1000

        self.speedVec = pygame.Vector2()

        self.speed = 0
        self.stuck = False
        
    
    def getAction(self,action):
        self.action = action

    def setPosition(self, pos):
        super().setPosition(pos)
        # self.graze.setPosition(pos)

    def outofBounderies(self,pos):
        return pos[0] < 0 or pos[0] > Constants.BOUNDERIES[0] or pos[1] < 0 or pos[1] > Constants.BOUNDERIES[1]

    def update(self,delta) -> None:
        angle = 0

        if(self.energy > 0):
            if(self.action[0] != -1):
                
                match self.action[1]:
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

                
                self.speed = self.action[0] * 4 * Constants.SPACESHIP_SPEED * delta/10

                #TODO return this
                # self.energy -= math.ceil(speed) 
                
                vector = pygame.math.Vector2(self.speed,0).rotate(angle)

                self.speedVec = vector

                nextPos = (round(self.pos[0] + vector[0]),round(self.pos[1] + vector[1]))
                if not self.outofBounderies(nextPos):
                    self.stuck = False
                    self.setPosition(nextPos)
                else:
                    self.stuck = True
                

