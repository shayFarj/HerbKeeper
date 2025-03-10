import CircleSprite
import Constants
import pygame


HERB_IMAGE = pygame.Surface((Constants.HERB_RADIUS*2,Constants.HERB_RADIUS*2),pygame.SRCALPHA)
pygame.gfxdraw.aacircle(HERB_IMAGE,Constants.HERB_RADIUS,Constants.HERB_RADIUS,Constants.HERB_RADIUS - 1,Constants.PASTEL_GREEN)
pygame.gfxdraw.filled_circle(HERB_IMAGE, Constants.HERB_RADIUS, Constants.HERB_RADIUS, Constants.HERB_RADIUS - 1,Constants.PASTEL_GREEN)

class Herb(pygame.sprite.Sprite):
    def __init__(self,pos):
        pos2 =  (pos[0] - Constants.HERB_RADIUS, pos[1] - Constants.HERB_RADIUS)

        self.rect = pygame.rect.Rect(pos2,(2*Constants.HERB_RADIUS,2*Constants.HERB_RADIUS))
        self.radius = Constants.HERB_RADIUS
        self.pos = pos

        self.image = HERB_IMAGE

    def setPosition(self, pos):
        self.rect.move_ip(-self.pos[0] + pos[0],-self.pos[1] + pos[1])
        self.pos = pos