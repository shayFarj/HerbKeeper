import Herb
import Spaceship
import Bouncer
import pygame
import Constants
import random
import Timer
import torch
import math
import StateDisplay
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
        # self.graze_group = pygame.sprite.GroupSingle()
        # self.graze_group.add(self.spaceship.graze)
        self.fps_clock = pygame.time.Clock()
        # self.sDisplay = StateDisplay.StateDisplay((64,64),32)

        self.scene_status = scene_flags.start_menu

        self.delta_avg = []
        
        self.actions = []
            
        for i in range(1,9):
            self.actions.append((1,i))
        
        self.actions.append((0,0))


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

        #text_to_screen(self.surface,str(self.spaceship.action),128,64,size=20,color=Constants.PASTEL_RED,font_type="basss.ttf")
     

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
        if self.dmg_timer >= 2000:
            self.dmg_timer = 0
            self.spaceship.energy -= 1
            # reward -= Constants.MAX_PUNISH
        

        herb_p1 = torch.zeros((Constants.HERB_NUMBER,2))

        j = 0
        for i in self.herb_group.sprites():
            herb_p1[j][0] = (i.pos[0] - self.spaceship.pos[0])
            herb_p1[j][1] = (i.pos[1] - self.spaceship.pos[1])
            j += 1

        h_dist1 = torch.sqrt(torch.sum((herb_p1**2),axis=1))

        # if not 0 in h_dist1:
        #     h1_cosines = torch.matmul(herb_p1,self.act_vectors[action[1]]) / h_dist1
        # else:
        #     h1_cosines = torch.tensor([0],dtype=torch.float16)

        self.getInput(events,action)
        delta = self.update(or_delta=or_delta)

        hc_count, bc_count = self.collisions()

        if render:
            self.draw()


        if self.scene_status == scene_flags.game:
            self.dmg_timer += delta
        else:
            self.dmg_timer = 0

        
        herb_p2 = torch.zeros((Constants.HERB_NUMBER,2))

        j = 0
        for i in self.herb_group.sprites():
            herb_p2[j][0] = (i.pos[0] - self.spaceship.pos[0])
            herb_p2[j][1] = (i.pos[1] - self.spaceship.pos[1])
            j += 1
        
        h_dist2 = torch.sqrt(torch.sum((herb_p2**2),axis=1)) 
        
        h_diff = torch.clamp(h_dist2 - h_dist1,max = self.spaceship.speed,min = -self.spaceship.speed)

        

        if hc_count > 0 or bc_count > 0:
            reward = hc_count * Constants.MAX_REWARD - bc_count*Constants.MAX_PUNISH
        else:
            if self.spaceship.speed == 0 or self.spaceship.stuck:
                reward = -Constants.MAX_PUNISH / 2
            else:
                reward = torch.sum(Constants.reward_herb2(h_diff,self.spaceship.speed)).item()#Constants.reward_diff_herb(h_diff,self.spaceship.speed).item() #
        

        # text_to_screen(self.surface,"Graze : (" + str(grazeB) + "," + str(grazeH) + ")",196,64,size=20,color=Constants.PASTEL_PURPLE_LIGHT,font_type="basss.ttf")
        text_to_screen(self.surface,"Reward : " + str(reward),256+ 64,64,size=20,color=Constants.PASTEL_GREEN,font_type="basss.ttf")
        # text_to_screen(self.surface,"dIst : " + str(h_diff),256+ 64,128,size=20,color=Constants.PASTEL_GREEN,font_type="basss.ttf")
        # text_to_screen(self.surface,"speed : " + str(self.spaceship.speed),256+ 64,64 + 32,size=20,color=Constants.PASTEL_GREEN,font_type="basss.ttf")

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
        # self.sDisplay.update(self.state(delta))
        if not or_delta:
            if not self.training:
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
        
        

    def prox(self,num1,num2,mnum):
        diff = abs(num1 - num2)
        diff1 = abs(num1 - mnum) / diff
        diff2 = abs(num2 - mnum) / diff
        return (diff1,diff2)

    def polar(self,x, y):
        angle = math.atan2(y,x)
        radius = math.sqrt(y**2 + x**2)
        return (radius,angle)
        

    

    def draw(self):
        match(self.scene_status):
            case scene_flags.game:
                # self.graze_group.draw(self.surface)
                self.bouncer_group.draw(self.surface)
                self.spaceship_group.draw(self.surface)
                self.herb_group.draw(self.surface)
                # self.sDisplay.draw(self.surface)
                if not self.training:
                    
                    text_to_screen(self.surface,str(self.spaceship.energy),512-32,64,color=Constants.PASTEL_BLUE_LIGHT)
            case scene_flags.game_over:
                text_to_screen(self.surface,'FALIURE',128,128,size=100,color=Constants.PASTEL_RED,font_type='pixelated-papyrus.ttf')
                text_to_screen(self.surface,'Click to restart',128,128+96,size=30,color=Constants.PASTEL_BLUE,font_type='pixelated-papyrus.ttf')
            case scene_flags.start_menu:
                text_to_screen(self.surface,'Herb\'s Keeper',128,128,size=100,color=Constants.PASTEL_GREEN,font_type='pixelated-papyrus.ttf')
                text_to_screen(self.surface,'Click to start',128,128+96,size=30,color=Constants.PASTEL_BLUE,font_type='pixelated-papyrus.ttf')


    def state(self, delta):
        state = torch.zeros(Constants.STATE_LEN,dtype=torch.float32)

        state[0] = self.spaceship.energy / Constants.INIT_ENERGY

        state[1] = self.spaceship.pos[0] / Constants.BOUNDERIES[0]
        state[2] = self.spaceship.pos[1] / Constants.BOUNDERIES[1]

        i_iter = 3
        for i in self.herb_group.sprites():
            state[i_iter] = (i.pos[0] - self.spaceship.pos[0]) / Constants.BOUNDERIES[0]
            i_iter += 1
            state[i_iter] = (i.pos[1] - self.spaceship.pos[1]) / Constants.BOUNDERIES[1]
            i_iter += 1

        for i in self.bouncer_group.sprites():
            state[i_iter] = (i.pos[0] - self.spaceship.pos[0]) / Constants.BOUNDERIES[0]
            i_iter += 1
            state[i_iter] = (i.pos[1] - self.spaceship.pos[1]) / Constants.BOUNDERIES[1]
            i_iter += 1
            state[i_iter] =  i.dir[0] / math.ceil(delta/10)
            i_iter += 1
            state[i_iter] = i.dir[1] / math.ceil(delta/10)
            i_iter += 1
        
        return state

    def state_sorted(self, delta):
        state = torch.zeros(Constants.STATE_LEN,dtype=torch.float32)

        state[0] = self.spaceship.energy / Constants.INIT_ENERGY

        state[1] = self.spaceship.pos[0] / Constants.BOUNDERIES[0]
        state[2] = self.spaceship.pos[1] / Constants.BOUNDERIES[1]

        i_iter = 3

        herbs_arr = []

        for i in self.herb_group.sprites():
            herbs_arr.append((i.pos[0] - self.spaceship.pos[0]) / Constants.BOUNDERIES[0], (i.pos[1] - self.spaceship.pos[1]) / Constants.BOUNDERIES[1])

        herbs_arr = sorted(herbs_arr,key=lambda x: x[0]**2 + x[1]**2)

        for i in herbs_arr:
            state[i_iter] = i[0]
            i_iter += 1
            state[i_iter] = i[1]
            i_iter += 1

        boun_arr = []

        for i in self.bouncer_group.sprites():
            boun_arr.append((i.pos[0] - self.spaceship.pos[0]) / Constants.BOUNDERIES[0],
                             (i.pos[1] - self.spaceship.pos[1]) / Constants.BOUNDERIES[1],
                             i.dir[0] / math.ceil(delta/10),
                             i.dir[1] / math.ceil(delta/10))

        boun_arr = sorted(boun_arr,key=lambda x: x[0]**2 + x[1]**2)

        for i in boun_arr:
            state[i_iter] = i[0]
            i_iter += 1
            state[i_iter] = i[1]
            i_iter += 1
            state[i_iter] =  i[2]
            i_iter += 1
            state[i_iter] = i[3]
            i_iter += 1
        
        return state

    # def state(self, delta):
    #     state = torch.zeros(Constants.STATE_LEN,dtype=torch.float32)

    #     state[0] = self.spaceship.energy / Constants.INIT_ENERGY

    #     state[1] = self.spaceship.pos[0] / Constants.BOUNDERIES[0]
    #     state[2] = self.spaceship.pos[1] / Constants.BOUNDERIES[1]

    #     i_iter = 3
    #     for i in self.herb_group.sprites():
    #         x  = (i.pos[0] - self.spaceship.pos[0]) 
    #         y = (i.pos[1] - self.spaceship.pos[1])
    #         radius, angle = self.polar(x,y)

    #         if angle < 0:
    #             angle = 2*math.pi + angle
            
    #         count = int(angle // (math.pi/4))

    #         if angle < (2*math.pi) * (7/8):
    #             diff1, diff2 = self.prox(count*(math.pi/4),(count + 1)*(math.pi/4),angle)
    #             state[3 + count] = diff2 * Constants.dir_status_herb(radius)
    #             state[3 + count + 1] = diff1 * Constants.dir_status_herb(radius)
    #         else:
    #             diff1, diff2 = self.prox(count*(math.pi/4),(count + 1)*(math.pi/4),angle)
    #             state[3 + count] = diff2 * Constants.dir_status_herb(radius)
    #             state[3] = diff1 * Constants.dir_status_herb(radius)
                
    
    #     for i in self.bouncer_group.sprites():
    #         x  = (i.pos[0] - self.spaceship.pos[0]) 
    #         y = (i.pos[1] - self.spaceship.pos[1])
    #         radius, angle = self.polar(x,y)

    #         if angle < 0:
    #             angle = 2*math.pi - angle
            
    #         count = int(angle // (math.pi/4))

    #         if angle < (2*math.pi) * (7/8):
    #             diff1, diff2 = self.prox(count*(math.pi/4),(count + 1)*(math.pi/4),angle)
    #             state[3 + count] = diff2 * Constants.dir_status_boun(radius)
    #             state[3 + count + 1] = diff1 * Constants.dir_status_boun(radius)
    #         else:
    #             diff1, diff2 = self.prox(count*(math.pi/4),0,angle)
    #             state[3 + count] = diff2 * Constants.dir_status_boun(radius)
    #             state[3] = diff1 * Constants.dir_status_boun(radius)
            
    #     return state

    def collisions(self):
        herb_c = pygame.sprite.spritecollide(self.spaceship,self.herb_group,dokill=False)
        hc_count = len(herb_c)

        for i in herb_c:
             self.spaceship.energy += 1#Constants.HERB_ENERGY
             i.setPosition(self.randomPosition())

        bounce_c = pygame.sprite.spritecollide(self.spaceship,self.bouncer_group,dokill=False)
        bc_count = len(bounce_c)

        for i in bounce_c:
            self.spaceship.energy -= 1#Constants.BOUNCER_DAMAGE
            i.setPosition(self.randomPosition())
        
        return (hc_count,bc_count)




    def outofBounderies(self,sprite):
        return sprite.pos[0] < 0 or sprite.pos[0] > Constants.BOUNDERIES[0] or sprite.pos[1] < 0 or sprite.pos[1] > Constants.BOUNDERIES[1]
