import pygame
import pygame.gfxdraw
from pygame.locals import *
import math
import torch


PASTEL_RED = (255,127,127)
PASTEL_BLUE = (127,127,255)
PASTEL_BLUE_LIGHT = (127,191,255)
PASTEL_PURPLE = (255,127 + 32,255)
PASTEL_PURPLE_LIGHT = (255,191,191)
PASTEL_GREEN = (127,255,127)
GREEN_DARK = (0,64,0,127 + 64)


ACT_CARTEZ = torch.zeros(9,2,dtype = torch.float32)

AGENT_GAMMA = 0.95
SCHEDULER_GAMMA = 0.8

FPS = 60

DEBUG = False

BOUNCER_DAMAGE = 2
HERB_ENERGY = 1
# BOUNCER_NUMBER = 40
BOUNCER_NUMBER = 8# 15
# HERB_NUMBER = 7
HERB_NUMBER = 1
HERB_RADIUS = 14
BOUNCER_RADIUS = 12

INIT_ENERGY = 4

TIME_UNIT = 2000

SPACESHIP_SPEED = 300
BOUNCER_SPEED = 150
SPACESHIP_RADIUS = 16


#STATE_LEN = HERB_NUMBER * 2 + BOUNCER_NUMBER * 4 + 3   #herb position, bouncer position&velocity, spaceship's position&energy 

STATE_LEN = 3 + 8 + 8 + 16 #spaceship's position&energy, herb eyes, bouncer_eyes, bouncer_move_change(16 eyes)

MAX_REWARD = 7
MAX_PUNISH = 10

MAX_DIFF_PUNISH = MAX_PUNISH
MAX_DIFF_REWARD = MAX_REWARD

MAX_STATUS_PUNISH = MAX_PUNISH
MAX_STATUS_REWARD = MAX_REWARD



for i in range(8):
    ACT_CARTEZ[i][0] = math.cos(math.radians((225 + 45*i) % 360)) * MAX_REWARD
    ACT_CARTEZ[i][1] = math.sin(math.radians((225 + 45*i) % 360)) * MAX_REWARD

ACT_EYES = torch.zeros(9,8,dtype=torch.float32)

for i in range(8):
    ACT_EYES[i][((225 + 45*i) % 360) // 45] = MAX_REWARD

BOUNDERIES = (512,512)

flags = DOUBLEBUF
screen = pygame.display.set_mode(BOUNDERIES, flags=flags)

HERB_IMAGE = pygame.Surface((HERB_RADIUS*2,HERB_RADIUS*2))
pygame.gfxdraw.aacircle(HERB_IMAGE,HERB_RADIUS,HERB_RADIUS,HERB_RADIUS - 1,PASTEL_GREEN)
pygame.gfxdraw.filled_circle(HERB_IMAGE, HERB_RADIUS, HERB_RADIUS, HERB_RADIUS - 1,PASTEL_GREEN)
HERB_IMAGE = HERB_IMAGE.convert_alpha()

BOUNCER_IMAGE = pygame.Surface((BOUNCER_RADIUS*2,BOUNCER_RADIUS*2))

pygame.gfxdraw.aacircle(BOUNCER_IMAGE,BOUNCER_RADIUS,BOUNCER_RADIUS,BOUNCER_RADIUS - 1,PASTEL_RED)
pygame.gfxdraw.filled_circle(BOUNCER_IMAGE, BOUNCER_RADIUS, BOUNCER_RADIUS, BOUNCER_RADIUS - 1,PASTEL_RED)

pygame.gfxdraw.aapolygon(BOUNCER_IMAGE,[(2,8),(22,8),(12,23)],(0,0,0))
pygame.gfxdraw.filled_polygon(BOUNCER_IMAGE,[(2,8),(22,8),(12,23)],(0,0,0))

BOUNCER_IMAGE = BOUNCER_IMAGE.convert_alpha()

REWARD_GAMMA = (BOUNDERIES[0]/2) * HERB_NUMBER 
PUNISH_GAMMA = (BOUNDERIES[0]/2) * BOUNCER_NUMBER

REWARD_ALPHA = 1.6
PUNISH_ALPHA = 1.4

MIN_STATUS_HERB = 1 
MIN_STATUS_BOUN = 2

MAX_D = math.sqrt(BOUNDERIES[0]**2 + BOUNDERIES[1]**2)

GREEN_SCOPE = MAX_D
RED_SCOPE = 33

STATUS_ALPHA_REWARD = (1/MIN_STATUS_HERB - 1/MAX_STATUS_REWARD) / (GREEN_SCOPE- HERB_RADIUS - SPACESHIP_RADIUS)
STATUS_ALPHA_PUNISH = (1/MIN_STATUS_BOUN - 1/MAX_STATUS_PUNISH) / (RED_SCOPE- BOUNCER_RADIUS - SPACESHIP_RADIUS)


RELEV_ALPHA = 95
RELEV_TRANS = (-RELEV_ALPHA+math.sqrt(RELEV_ALPHA**2+4*RELEV_ALPHA)) / (2*RELEV_ALPHA)


def d_relev(distance):
    d_norm = torch.abs(distance / (MAX_D - SPACESHIP_RADIUS -BOUNCER_RADIUS))
    return 1 /(RELEV_ALPHA*(d_norm + RELEV_TRANS)) - RELEV_TRANS


RELEV_ALPHA2 = (1 - MIN_STATUS_BOUN/MAX_STATUS_PUNISH) / (RED_SCOPE - HERB_RADIUS - SPACESHIP_RADIUS)
def d_relev2(distance):
    offset = 1 / RELEV_ALPHA2
    return 1 / (RELEV_ALPHA2 * (distance - BOUNCER_RADIUS - SPACESHIP_RADIUS + offset))

def outofBounderies(sprite):
        if sprite is pygame.sprite:
            return sprite.pos[0] < 0 or sprite.pos[0] > BOUNDERIES[0] or sprite.pos[1] < 0 or sprite.pos[1] > BOUNDERIES[1]
        else:
            return sprite[0] < 0 or sprite[0] > BOUNDERIES[0] or sprite[1] < 0 or sprite[1] > BOUNDERIES[1]


def dir_status_herb(distance):
    offset = 1 / (MAX_STATUS_REWARD * STATUS_ALPHA_REWARD)
    return 1 / (STATUS_ALPHA_REWARD * (distance- HERB_RADIUS - SPACESHIP_RADIUS + offset))


def dir_status_boun(distance):
    offset = 1 / (MAX_STATUS_PUNISH * STATUS_ALPHA_PUNISH)
    return 1 / (STATUS_ALPHA_PUNISH * (distance- BOUNCER_RADIUS - SPACESHIP_RADIUS + offset))


def reward_herb2(distance,speed):
    if speed == 0:
        return torch.zeros(1,dtype=torch.float32)
    offset = 1 / ((MAX_DIFF_REWARD / 2) * REWARD_ALPHA)

    sum = torch.sum(1 / (REWARD_ALPHA * (distance - torch.sign(distance)*(offset + speed))))

    if math.isinf(sum):
        return torch.zeros(1,dtype=torch.float32)
    else:
        return sum 

def punish_boun(distance,speed,dis):
    if speed == 0:
        return torch.zeros(1,dtype=torch.float32)
    offset = 1 / ((MAX_DIFF_PUNISH / 2) * PUNISH_ALPHA)

    x = distance - torch.sign(distance)*(offset + speed)
    punishes = -1 / (PUNISH_ALPHA*x)
    p_relev = punishes * d_relev2(dis)

    sum = torch.sum(p_relev)

    if math.isinf(sum):
        return torch.zeros(1,dtype=torch.float32)
    else:
        return sum 

def actToCartez(action):
    return ACT_CARTEZ[action[1] - 1] * action[0]

def actToEyes(action):
    if action[0] == 0:
        return ACT_EYES[8]
    else:
        return ACT_EYES[action[1] - 1]
    
def outofBounderies_pos(pos):
        return pos[0] < 0 or pos[0] > BOUNDERIES[0] or pos[1] < 0 or pos[1] > BOUNDERIES[1]