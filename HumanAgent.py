import pygame

class humanAgent:
    def __init__(self) -> None:
        self.action = [0,0]
        self.active = True


    def getAction(self,events) -> tuple:
        if not self.active:
            self.action = [0,0]
            return self.action
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.action[1] = 1#-135
                if event.key == pygame.K_w:
                    self.action[1] = 2#-90
                if event.key == pygame.K_e:
                    self.action[1] = 3#-45
                if event.key == pygame.K_d:
                    self.action[1] = 4#0
                if event.key == pygame.K_c:
                    self.action[1] = 5#45
                if event.key == pygame.K_x:
                    self.action[1] = 6#90
                if event.key == pygame.K_z:
                    self.action[1] = 7#135
                if event.key == pygame.K_a:
                    self.action[1] = 8#180

                if event.key == pygame.K_v:
                    self.action[0] = 0
                if event.key == pygame.K_b:
                    self.action[0] = 1
                if event.key == pygame.K_n:
                    self.action[0] = 2
                if event.key == pygame.K_m:
                    self.action[0] = 3

        return self.action