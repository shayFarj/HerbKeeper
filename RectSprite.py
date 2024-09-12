import ShapeSprite
import pygame
import pygame.gfxdraw
import RectCollision

class RectSprite(ShapeSprite.shapeSprite):
    def __init__(self,pos,size,color) -> None:
        super().__init__(pos)
        self.size2 = (size[0]/2,size[1]/2)
        self.rect = pygame.rect.Rect((pos[0] - self.size2[0],pos[1] - self.size2[1]),size)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.cShape = RectCollision.rectCollision(pos,size)
