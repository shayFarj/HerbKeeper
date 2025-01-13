import ShapeSprite
import pygame
import pygame.gfxdraw

class CircleSprite (ShapeSprite.shapeSprite):
    def __init__(self,pos,radius,color) -> None:
        super().__init__(pos)
        self.rect = pygame.rect.Rect(pos,(2*radius,2*radius))
        self.radius = radius
        self.image = pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(self.image,radius,radius,radius - 1,color)
        pygame.gfxdraw.filled_circle(self.image, radius, radius, radius - 1,color)

    def setPosition(self, pos):
        self.rect.x = pos[0] - self.radius
        self.rect.y = pos[1] - self.radius
        self.pos = pos