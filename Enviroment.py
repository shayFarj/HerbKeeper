import Herb
import Spaceship
import Bouncer
import pygame
import Constants
import random
import Timer
import torch
import math
import numpy

class scene_flags:
    game = 1
    game_over = 2
    start_menu = 0

def text_to_screen(screen, text, x, y, size = 50,
            color = (200, 000, 000), font_type = 'basis33.ttf'):
    try:

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception:
        print('Font Error, saw it coming')

class Enviroment:
    def __init__(self,surface,agent,training = False):
        self.training = training
        self.agent = agent
        self.bouncer_group = pygame.sprite.Group()
        self.herb_group = pygame.sprite.Group()
        self.spaceship = Spaceship.SpaceShip((200,200))
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(self.spaceship)
        self.graze_group = pygame.sprite.GroupSingle()
        self.graze_group.add(self.spaceship.graze)
        self.fps_clock = pygame.time.Clock()

        self.scene_status = scene_flags.start_menu

        self.delta_avg = []
        
        self.actions = []
        for i in range(1,9):
            for j in range(0,2):
                self.actions.append((j,i))

        self.surface = surface

        if not training:
            pygame.mixer.music.load("opening.wav")
            pygame.mixer.music.play(-1)
        
        self.dmg_timer = 0

    def getInput(self,events,action):
        self.spaceship.getAction(action)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.scene_status == scene_flags.start_menu or self.scene_status == scene_flags.game_over:
                    self.restart()

        text_to_screen(self.surface,str(self.spaceship.action),128,64,size=20,color=Constants.PASTEL_RED,font_type="basss.ttf")
     

    def restart(self):
        self.clear()
        if not self.training:
            pygame.mixer.music.stop()

        self.scene_status = scene_flags.game
        
        self.spaceship.energy = Constants.INIT_ENERGY
        self.spaceship.setPosition(self.randomPosition())

        self.agent.active = True

        for i in range(Constants.BOUNCER_NUMBER):
            self.bouncer_group.add(Bouncer.Bouncer(self.randomPosition()))

        for i in range(Constants.HERB_NUMBER):
            self.herb_group.add(Herb.Herb(self.randomPosition()))

    
    def gameOver(self):
        return self.spaceship.energy <= 0

    def legal_actions(self,state):
        return self.actions

    def move(self,action,events,or_delta = None,render = True):
        reward = 0
        if self.dmg_timer >= 5000:
            self.dmg_timer = 0
            self.spaceship.energy -= 1
            reward -= 1
        

        herb_p1 = torch.zeros((Constants.HERB_NUMBER,2))

        j = 0
        for i in self.herb_group.sprites():
            herb_p1[j][0] = (i.pos[0] - self.spaceship.pos[0])
            herb_p1[j][1] = (i.pos[1] - self.spaceship.pos[1])
            j += 1

        h_dist1 = torch.sqrt(torch.sum((herb_p1**2),axis=1)) - 110
        dh_reward1 = 2*torch.sum(1 - torch.tanh(0.06*h_dist1))

        self.getInput(events,action)
        self.sustain()
        delta = self.update(or_delta=or_delta)

        hc_count, bc_count = self.collisions()

        if render:
            self.draw()


        if self.scene_status == scene_flags.game:
            self.dmg_timer += delta
        else:
            self.dmg_timer = 0

        
        herb_p2 = torch.zeros((Constants.HERB_NUMBER,2))
        #bounce_p = numpy.zeros((Constants.BOUNCER_NUMBER,2))

        j = 0
        for i in self.herb_group.sprites():
            herb_p2[j][0] = (i.pos[0] - self.spaceship.pos[0])
            herb_p2[j][1] = (i.pos[1] - self.spaceship.pos[1])
            j += 1
        
        # k = 0
        # for i in self.bouncer_group.sprites():
        #     bounce_p[k][0] == (i.pos[0] - self.spaceship.pos[0])/Constants.BOUNDERIES[0]
        #     bounce_p[k][1] == (i.pos[1] - self.spaceship.pos[1])/Constants.BOUNDERIES[1]
        
        h_dist2 = torch.sqrt(torch.sum((herb_p2**2),axis=1)) - 110
        dh_reward2 = 2* torch.sum(1 - torch.tanh(0.06*h_dist2))#0.5 - 0.5* torch.tanh(0.015*h_dist)

        if hc_count > 0:
            reward = hc_count * 3
        else:
            reward = (dh_reward2 - dh_reward1)*2 - 0.05
        

        # text_to_screen(self.surface,"Graze : (" + str(grazeB) + "," + str(grazeH) + ")",196,64,size=20,color=Constants.PASTEL_PURPLE_LIGHT,font_type="basss.ttf")
        text_to_screen(self.surface,"Reward : " + str(reward),256+ 64,64,size=20,color=Constants.PASTEL_GREEN,font_type="basss.ttf")
        

        done = self.gameOver()
        if or_delta:
            return reward,done, or_delta
        else:
            return reward,done, delta
        


    def randomPosition(self):
        return (random.randint(0,Constants.BOUNDERIES[0]),random.randint(0,Constants.BOUNDERIES[1]))

    def clear(self):
        self.scene_status = scene_flags.game_over
        self.bouncer_group.empty()
        self.herb_group.empty()
        self.agent.active = False

        if not self.training:
            pygame.mixer.music.load("ending.wav")
            pygame.mixer.music.play(-1)

    def update(self,or_delta=None):
        if self.gameOver() and self.scene_status != scene_flags.game_over:
            self.clear()
            return

        if or_delta:
            delta = or_delta*1000
        else:
            delta = self.fps_clock.tick()
            self.delta_avg.append(delta)



        self.bouncer_group.update(delta)
        self.spaceship_group.update(delta)


        # text_to_screen(self.surface,"state : " +str(len(str_state)),64,128+64,size=20,color=Constants.PASTEL_BLUE_LIGHT,font_type='pixelated-papyrus.ttf')
        if not or_delta:
            if len(self.delta_avg) < 20:
                text_to_screen(self.surface,"fps : " + str(round(1000/delta)),64,64,size=20,color=Constants.PASTEL_BLUE_LIGHT,font_type='pixelated-papyrus.ttf')
                return delta
            else:
                self.delta_avg.pop(0)
                avg = 0
                for i in self.delta_avg:
                    avg += i
                avg /= len(self.delta_avg)
                text_to_screen(self.surface,"fps : " + str(round(1000/avg)),64,64,size=20,color=Constants.PASTEL_BLUE_LIGHT,font_type='pixelated-papyrus.ttf')
                return avg
        else:
            return delta
        
        






    def draw(self):
        match(self.scene_status):
            case scene_flags.game:
                self.graze_group.draw(self.surface)
                self.bouncer_group.draw(self.surface)
                self.spaceship_group.draw(self.surface)
                self.herb_group.draw(self.surface)
                text_to_screen(self.surface,str(self.spaceship.energy),512-32,64,color=Constants.PASTEL_BLUE_LIGHT)
            case scene_flags.game_over:
                text_to_screen(self.surface,'FALIURE',128,128,size=100,color=Constants.PASTEL_RED,font_type='pixelated-papyrus.ttf')
                text_to_screen(self.surface,'Click to restart',128,128+96,size=30,color=Constants.PASTEL_BLUE,font_type='pixelated-papyrus.ttf')
            case scene_flags.start_menu:
                text_to_screen(self.surface,'Herb\'s Keeper',128,128,size=100,color=Constants.PASTEL_GREEN,font_type='pixelated-papyrus.ttf')
                text_to_screen(self.surface,'Click to start',128,128+96,size=30,color=Constants.PASTEL_BLUE,font_type='pixelated-papyrus.ttf')


    def state(self, delta):
        state = []
        state.append(self.spaceship.energy / 3)

        state.append(self.spaceship.pos[0] / Constants.BOUNDERIES[0])
        state.append(self.spaceship.pos[1] / Constants.BOUNDERIES[1])


        for i in self.herb_group.sprites():
            state.append(i.pos[0] / Constants.BOUNDERIES[0])
            state.append(i.pos[1] / Constants.BOUNDERIES[1])



        for i in range(Constants.HERB_NUMBER - len(self.herb_group.sprites())):
            state.append(0)
            state.append(0)

        for i in self.bouncer_group.sprites():
            state.append(i.pos[0] / Constants.BOUNDERIES[0])
            state.append(i.pos[1] / Constants.BOUNDERIES[1])

            state.append(i.dir[0] / math.ceil(delta/10))
            state.append(i.dir[1] / math.ceil(delta/10))
        for i in range(Constants.BOUNCER_NUMBER - len(self.bouncer_group.sprites())):
            state.append(0)
            state.append(0)
            state.append(0)
            state.append(0)



        # print(f"\r length : "+ str(len(state)) + "///",end ="")
        state = torch.tensor(state,dtype=torch.float32)
        #print(f"\r"+str(state),end ="")
        return state


    def collisions(self):
        herb_c = pygame.sprite.spritecollide(self.spaceship,self.herb_group,True)
        hc_count = len(herb_c)

        for i in herb_c:
             self.spaceship.energy += 1#Constants.HERB_ENERGY

        bounce_c = pygame.sprite.spritecollide(self.spaceship,self.bouncer_group,True)
        bc_count = len(bounce_c)

        for i in bounce_c:
            self.spaceship.energy -= 1#Constants.BOUNCER_DAMAGE
        
        return (hc_count,bc_count)




    def outofBounderies(self,sprite):
        return sprite.pos[0] < 0 or sprite.pos[0] > Constants.BOUNDERIES[0] or sprite.pos[1] < 0 or sprite.pos[1] > Constants.BOUNDERIES[1]


    def sustain(self):
        if self.scene_status == scene_flags.game:
            if len(self.herb_group.sprites()) < Constants.HERB_NUMBER:
                self.herb_group.add(Herb.Herb(self.randomPosition()))

            if len(self.bouncer_group.sprites()) < Constants.BOUNCER_NUMBER:
                x, y = self.randomPosition()
                bouncer = Bouncer.Bouncer((x,y))

                self.bouncer_group.add(bouncer)




