
import pygame
import Constants
import Enviroment
import HumanAgent
import Bouncer
import RectSprite

from timeit import default_timer as timer

def text_to_screen(screen, text, x, y, size = 50,
            color = (200, 000, 000), font_type = 'basis33.ttf'):
    try:

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception:
        print('Font Error, saw it coming')

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(Constants.BOUNDERIES)
main_surf = pygame.Surface(Constants.BOUNDERIES)
main_surf.fill((0,0,0))

pygame.display.set_caption("Herb's keeper")


entering = True
failing = False

human = HumanAgent.humanAgent()

env = Enviroment.Enviroment(main_surf)

pygame.mixer.music.load("opening.wav")
pygame.mixer.music.play(-1)


def main():
    run = True
    while run:
        main_surf.fill((0,0,0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        
        action = human.getAction(events)
        
        env.getInput(events,action)
        env.collisions()
        env.update()
        env.draw()
        env.sustain()

        screen.blit(main_surf,(0,0))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()