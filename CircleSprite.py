import ShapeSprite
import pygame
import pygame.gfxdraw
import CircleCollision

class CircleSprite (ShapeSprite.shapeSprite):
    def __init__(self,pos,radius,color) -> None:
        super().__init__(pos)
        self.rect = pygame.rect.Rect((pos[0] - radius,pos[1] - radius),(radius,radius))
        self.image = pygame.Surface((radius*2,radius*2),pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(self.image,radius,radius,radius - 1,color)
        pygame.gfxdraw.filled_circle(self.image, radius, radius, radius - 1,color)
        self.cShape = CircleCollision.CircleCollision(pos,radius)
