import pygame
import pygame.gfxdraw
from pygame.locals import *
import math
import torch


BULLET_SPEED = 8
BULLET_DIR_ERROR = 1
BULLET_SIZE = 5
PASTEL_RED = (255,127,127)
PASTEL_BLUE = (127,127,255)
PASTEL_BLUE_LIGHT = (127,191,255)
PASTEL_PURPLE = (255,127 + 32,255)
PASTEL_PURPLE_LIGHT = (255,191,191)
PASTEL_GREEN = (127,255,127)
GREEN_DARK = (0,64,0,127 + 64)

AGENT_GAMMA = 0.95
SCHEDULER_GAMMA = 0.8

FPS = 60

CROP_RADIUS = 100
BULLET_ENERGY = 50
BOUNCER_DAMAGE = 400
BULLET_NUMBER = 15
HERB_ENERGY = 500
# BOUNCER_NUMBER = 40
BOUNCER_NUMBER = 0 # 15
# HERB_NUMBER = 7
HERB_NUMBER = 1
CROP_TIME = 30
HERB_RADIUS = 14
BOUNCER_RADIUS = 12

INIT_ENERGY = 4

SPACESHIP_SPEED = 300

STATE_LEN = HERB_NUMBER * 2 + BOUNCER_NUMBER * 4 + 3  #herb position, bouncer position&velocity, spaceship's position&energy 

#STATE_LEN = 3 + 8 #spaceship's position&energy, directions

P_DIRECTIONS = [1,2,3,4,5,6,7,8]
P_GEARS = [-1,0,1,2,3]


MAX_REWARD = 1
MAX_PUNISH = MAX_REWARD
SPACESHIP_RADIUS = 16
# CROP_HP = 60
CROP_HP = 30

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

REWARD_ALPHA = 0.6

def reward_diff_herb(distance,speed):
    if speed == 0:
        return 0 * distance
    else:
        if distance <= 0:
            return (MAX_REWARD/2) * (1 - torch.tanh((speed + distance)/REWARD_ALPHA))
        else:
            return (MAX_REWARD/2) * (-1 - torch.tanh((distance - speed)/REWARD_ALPHA))

def outofBounderies(sprite):
        if sprite is pygame.sprite:
            return sprite.pos[0] < 0 or sprite.pos[0] > BOUNDERIES[0] or sprite.pos[1] < 0 or sprite.pos[1] > BOUNDERIES[1]
        else:
            return sprite[0] < 0 or sprite[0] > BOUNDERIES[0] or sprite[1] < 0 or sprite[1] > BOUNDERIES[1]


def dir_status_herb(distance):
    return MAX_REWARD * (1 - math.tanh(((distance - HERB_RADIUS - SPACESHIP_RADIUS)/REWARD_GAMMA)))

def reward_diff_boun(distance,speed):
    if speed == 0:
        return 0 * distance
    else:
        if distance <= 0:
            return -MAX_PUNISH * (1 - torch.tanh((speed + distance)/0.6))
        else:
            return -MAX_PUNISH * (-1 - torch.tanh((distance - speed)/0.6))

def dir_status_boun(distance):
    return MAX_PUNISH * (-(1 - math.tanh(((distance - HERB_RADIUS - SPACESHIP_RADIUS)/PUNISH_GAMMA))))

def reward_herb(distance,cosines):
    return torch.sum(cosines / (REWARD_ALPHA * ((distance - HERB_RADIUS - SPACESHIP_RADIUS) + 1 / (MAX_REWARD * REWARD_ALPHA))))

def reward_herb2(distance,speed):
    if distance == 0 or speed == 0:
        return torch.zeros(1)
    offset = 1 / ((MAX_REWARD / 2) * REWARD_ALPHA)

    return torch.sum(1 / (REWARD_ALPHA * (distance - torch.sign(distance)*(offset + speed))))