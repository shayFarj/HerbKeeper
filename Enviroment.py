import Herb
import Bullet
import Spaceship
import Bouncer
import pygame
import Constants
import random
import Timer
import torch
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
    def __init__(self,surface,agent):
        self.agent = agent
        self.bouncer_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.herb_group = pygame.sprite.Group()
        self.spaceship = Spaceship.SpaceShip((200,200),self.bullet_group)
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(self.spaceship)

        self.fps_clock = pygame.time.Clock()
        self.survive_clock = pygame.time.Clock()

        self.survive_time = 0

        self.scene_status = scene_flags.start_menu

        self.delta_avg = []
        
        self.actions = []
        for i in range(1,9):
            for j in range(-1,4):
                self.actions.append((i,j))

        self.surface = surface

        pygame.mixer.music.load("opening.wav")
        pygame.mixer.music.play(-1)

    def getInput(self,events,action):
        self.spaceship.getAction(action)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.scene_status == scene_flags.start_menu or self.scene_status == scene_flags.game_over:
                    self.restart()

        # text_to_screen(self.surface,str(self.spaceship.action),128,64,size=20,color=Constants.PASTEL_RED,font_type='pixelated-papyrus.ttf')
     

    def restart(self):
        pygame.mixer.music.stop()
        self.scene_status = scene_flags.
        
        self.survive_time = 0

        self.spaceship.energy = 1000

        self.agent.active = True

        for i in range(Constants.BOUNCER_NUMBER):
            self.bouncer_group.add(Bouncer.Bouncer(self.randomPosition()))

        for i in range(Constants.HERB_NUMBER):
            self.herb_group.add(Herb.Herb(self.randomPosition()))

    
    def gameOver(self):
        return self.spaceship.energy <= 0

    def legal_actions(self,state):
        return self.actions

    def move(self,action,events):
        self.survive_time += self.survive_clock.tick()
        prev_eng = self.spaceship.energy
        self.getInput(events,action)
        self.sustain()
        delta = self.update()
        self.collisions()
        #self.draw()
        reward = self.spaceship.energy - prev_eng + self.survive_time/10
        done = self.gameOver()

        return reward,done, delta


    def randomPosition(self):
        return (random.randint(0,Constants.BOUNDERIES[0]),random.randint(0,Constants.BOUNDERIES[1]))

    def clear(self):
        self.scene_status = scene_flags.game_over
        self.bouncer_group.empty()
        self.bullet_group.empty()
        self.herb_group.empty()
        self.agent.active = False

        pygame.mixer.music.load("ending.wav")
        pygame.mixer.music.play(-1)

    def update(self):
        if self.gameOver() and self.scene_status != scene_flags.game_over:
            self.clear()
            return


        delta = self.fps_clock.tick()
        self.delta_avg.append(delta)



        self.bouncer_group.update(delta)
        self.bullet_group.update(delta)
        self.spaceship_group.update(delta)

        str_state = self.state()



        text_to_screen(self.surface,"state : " +str(len(str_state)),64,128+64,size=20,color=Constants.PASTEL_BLUE_LIGHT,font_type='pixelated-papyrus.ttf')

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
        
        






    def draw(self):
        match(self.scene_status):
            case scene_flags.game:
                self.bouncer_group.draw(self.surface)
                self.bullet_group.draw(self.surface)
                self.spaceship_group.draw(self.surface)
                self.herb_group.draw(self.surface)
                text_to_screen(self.surface,str(self.spaceship.energy),512-32,64,color=Constants.PASTEL_BLUE_LIGHT)
            case scene_flags.game_over:
                text_to_screen(self.surface,'FALIURE',128,128,size=100,color=Constants.PASTEL_RED,font_type='pixelated-papyrus.ttf')
            case scene_flags.start_menu:
                text_to_screen(self.surface,'Herb\'s Keeper',128,128,size=100,color=Constants.PASTEL_GREEN,font_type='pixelated-papyrus.ttf')


    def state(self):
        state = []
        state.append(self.spaceship.energy)

        state.append(self.spaceship.pos[0])
        state.append(self.spaceship.pos[1])


        for i in self.herb_group.sprites():
            state.append(i.pos[0])
            state.append(i.pos[1])



        for i in range(Constants.HERB_NUMBER - len(self.herb_group.sprites())):
            state.append(0)
            state.append(0)

        for i in self.bouncer_group.sprites():
            state.append(i.pos[0])
            state.append(i.pos[1])

            state.append(i.dir[0])
            state.append(i.dir[1])
        for i in range(Constants.BOUNCER_NUMBER - len(self.bouncer_group.sprites())):
            state.append(0)
            state.append(0)
            state.append(0)
            state.append(0)


        for i in self.bullet_group.sprites():
            state.append(i.pos[0])
            state.append(i.pos[1])

            state.append(i.f_dir[0])
            state.append(i.f_dir[1])
        for i in range(Constants.BULLET_NUMBER - len(self.bullet_group.sprites())):
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
        for i in herb_c:
            self.spaceship.energy += Constants.HERB_ENERGY
                
        for i in self.bouncer_group.sprites():
            herb_bounce_c = pygame.sprite.spritecollide(i,self.herb_group,True)



        for i in self.bullet_group.sprites():
            bullet_bounce_c = pygame.sprite.spritecollide(i,self.bouncer_group,True)
            if len(bullet_bounce_c) != 0:
                self.bullet_group.remove(i)

        for i in self.bouncer_group.sprites():
            ship_bounce_c = pygame.sprite.spritecollide(self.spaceship,self.bouncer_group,True)
            for i in ship_bounce_c:
                self.spaceship.energy -= Constants.BOUNCER_DAMAGE

        for i in self.bullet_group.sprites():
            if self.outofBounderies(i):
                self.bullet_group.remove(i)


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




