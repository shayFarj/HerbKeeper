import CircleSprite
import Constants
import pygame.gfxdraw
import Timer
import Constants
import RectSprite


def text_to_screen(screen, text, x, y, size = 50,
            color = (200, 000, 000), font_type = 'basis33.ttf'):
    try:

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception:
        print('Font Error, saw it coming')

class Crop(CircleSprite.CircleSprite):
    def __init__(self,pos,group,surface,spaceship):
        super().__init__(pos,100,Constants.GREEN_DARK)
        pygame.gfxdraw.aacircle(self.image,99,99,99,Constants.PASTEL_GREEN)
        self.group = group
        self.surface = surface
        self.hp = Constants.CROP_HP
        self.beat = Timer.timerLoop(1)   
        self.spaceship = spaceship

    def update(self) -> None:
        if self.beat.completed():
            if self.collides(self.spaceship):
                self.spaceship.energy += 100

        if self.hp <= 0:
            self.group.remove(self)
        
