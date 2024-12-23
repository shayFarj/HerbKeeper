
import pygame
import Constants
import Enviroment
import HumanAgent
import Bouncer

from timeit import default_timer as timer

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(Constants.BOUNDERIES)
main_surf = pygame.Surface(Constants.BOUNDERIES)
main_surf.fill((0,0,0))

pygame.display.set_caption("Herb's keeper")

human = HumanAgent.humanAgent()

env = Enviroment.Enviroment(main_surf,human)

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
        env.sustain()
        env.update()
        env.collisions()
        env.draw()
        
        

        screen.blit(main_surf,(0,0))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()