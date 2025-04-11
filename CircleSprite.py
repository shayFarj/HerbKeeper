import ShapeSprite
import pygame
import pygame.gfxdraw



class CircleSprite (ShapeSprite.shapeSprite):
    def __init__(self,pos,radius,color) -> None:
        super().__init__(pos)
        pos2 =  (pos[0] - radius, pos[1] - radius)

        self.rect = pygame.rect.Rect(pos2,(2*radius,2*radius))
        self.radius = radius
        self.image = pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(self.image,radius,radius,radius - 1,color)
        pygame.gfxdraw.filled_circle(self.image, radius, radius, radius - 1,color)

    def setPosition(self, pos):
        self.rect.move_ip(-self.pos[0] + pos[0],-self.pos[1] + pos[1])
        self.pos = pos

    def setColor(self, color):
        pygame.gfxdraw.aacircle(self.image,self.radius,self.radius,self.radius - 1,color)
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, self.radius - 1,color)