import pygame

class humanAgent:
    def __init__(self) -> None:
        self.action = [0,0]
    
    def getAction(self,events) -> tuple:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.action[1] = -135
                if event.key == pygame.K_w:
                    self.action[1] = -90
                if event.key == pygame.K_e:
                    self.action[1] = -45
                if event.key == pygame.K_d:
                    self.action[1] = 0
                if event.key == pygame.K_c:
                    self.action[1] = 45
                if event.key == pygame.K_x:
                    self.action[1] = 90
                if event.key == pygame.K_z:
                    self.action[1] = 135
                if event.key == pygame.K_a:
                    self.action[1] = 180

                if event.key == pygame.K_v:
                    self.action[0] = 0
                if event.key == pygame.K_b:
                    self.action[0] = 1
                if event.key == pygame.K_n:
                    self.action[0] = 2
                if event.key == pygame.K_m:
                    self.action[0] = 3
                
                if event.key == pygame.K_h:
                    self.action[0] = -1

        return self.action