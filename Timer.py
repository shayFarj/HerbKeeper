import pygame

class timerLoop:
    def __init__(self,seconds) -> None:
        self.seconds = seconds
        self.time = 0
        self.pTicks = 0
        self.gain = True
    
    def completed(self):
        if self.gain:
            cTicks = pygame.time.get_ticks()
            self.time += cTicks - self.pTicks
            flag = self.time >= self.seconds * 1000
            if flag:
                self.reset()
            self.pTicks = pygame.time.get_ticks()
            return flag
    
    def reset(self):
        self.time = 0
    
    def pause(self,pause):
        self.gain = not pause
    
