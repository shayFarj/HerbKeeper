
import pygame
import Constants
import Enviroment
import HumanAgent
from DQN_Agent import DQN_Agent
import Bouncer
import torch

from timeit import default_timer as timer

# checkpoint = torch.load("Data\checkpoint13.pth")
# print("loading checkpoint")


pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(Constants.BOUNDERIES)
main_surf = pygame.Surface(Constants.BOUNDERIES)
main_surf.fill((0,0,0))

pygame.display.set_caption("Herb's keeper")

human =  HumanAgent.humanAgent()#DQN_Agent(train=False)#
#human.DQN.load_state_dict(checkpoint['model_state_dict'])

env = Enviroment.Enviroment(main_surf,human)

human.env = env

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
        
        action = human.getAction(events=events)
        
        # action = human.get_action(state=env.state((1/Constants.FPS)*1000),train=False)

        test1 = env.state(1000*(1/Constants.FPS))
        env.move(action,events)
        test2 = env.state(1000*(1/Constants.FPS))
        # env.getInput(events,action)
        # env.sustain()
        # env.update()
        # env.collisions()
        # env.draw()        

        screen.blit(main_surf,(0,0))
        pygame.display.update()
        clock.tick(Constants.FPS)

if __name__ == "__main__":
    main()