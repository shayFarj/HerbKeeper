import Herb
import Bullet
import Spaceship
import Bouncer
import pygame
import Constants
import random
import Timer
import RectSprite


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
    def __init__(self,surface):
        self.bouncer_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.herb_group = pygame.sprite.Group()
        self.spaceship = Spaceship.SpaceShip((200,200),self.bullet_group)
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(self.spaceship)

        self.scene_status = scene_flags.start_menu

        self.surface = surface


    def getInput(self,events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.scene_status == scene_flags.start_menu or self.scene_status == scene_flags.game_over:
                    print("Aaa")
                    self.scene_status = scene_flags.game

                    for i in range(Constants.BOUNCER_NUMBER):
                        self.bouncer_group.add(Bouncer.Bouncer(self.randomPosition()))
        
                    for i in range(Constants.HERB_NUMBER):
                        self.herb_group.add(Herb.Herb(self.randomPosition()))
                    print(self.bouncer_group)

    def gameOver(self):
        return self.spaceship.energy <= 0

    def isLegal(self,action):
        if(action[0] != -1):
            return self.spaceship.energy - Constants.SPACESHIP_SPEED * action[0] > 0
        else:
            return self.spaceship.energy - 2 > 0


    def randomPosition(self):
        return (random.randint(0,Constants.BOUNDERIES[0]),random.randint(0,Constants.BOUNDERIES[1]))
    
    def getAction(self, action):
        self.spaceship.getAction(action)

    def update(self):
        if self.gameOver() and self.scene_status != scene_flags.game_over:
            self.scene_status = scene_flags.game_over
            self.bouncer_group.empty()
            self.bullet_group.empty()
            self.herb_group.empty()
            return

        self.bouncer_group.update()
        self.bullet_group.update()
        self.spaceship_group.update()
        
        
    
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
            
        status = self.status()
        status[0] = 0
        
    
    def status(self):
        status = []
        status.append(self.spaceship.energy)

        for i in self.herb_group.sprites():
            vector = (i.pos[0] - self.spaceship.pos[0],i.pos[1] - self.spaceship.pos[1])
            status.append(pygame.Vector2(vector[0],vector[1]).as_polar())
        for i in self.bouncer_group.sprites():
            vector = (i.pos[0] - self.spaceship.pos[0],i.pos[1] - self.spaceship.pos[1])
            status.append(pygame.Vector2(vector[0],vector[1]).as_polar())
        
        return status


    def collisions(self):
        for i in self.herb_group.sprites():
            if i.collides(self.spaceship):
                self.spaceship.energy += Constants.HERB_ENERGY
                self.herb_group.remove(i)
        
        for i in self.bouncer_group.sprites():
            for j in self.herb_group.sprites():
                if i.collides(j):
                    self.herb_group.remove(j)
        
        for i in self.bullet_group.sprites():
            for j in self.bouncer_group.sprites():
                if i.collides(j):
                    self.bullet_group.remove(i)
                    self.bouncer_group.remove(j)

        for i in self.bouncer_group.sprites():
            if i.collides(self.spaceship):
                # print(i)
                # print(i.cShape.pos)
                # print(self.spaceship.cShape.pos)
                # if(type(i) is Spaceship.SpaceShip):
                #     print(i.cShape.corners)
                # print(self.spaceship.cShape.corners)
                self.spaceship.energy -= Constants.BOUNCER_DAMAGE
                self.bouncer_group.remove(i)
        
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

        
        
            
