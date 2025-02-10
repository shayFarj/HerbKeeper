import pygame

class shapeSprite (pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        #https://www.reddit.com/r/pygame/comments/6v9os5/how_to_draw_a_sprite_with_a_circular_shape/
        self.rect = pygame.rect.Rect(pos,(0,0))
        self.pos = pos

    def setPosition(self,pos):
        self.rect.move_ip(-self.pos[0] + pos[0],-self.pos[1] + pos[1])
        self.pos = pos