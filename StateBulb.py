import CircleSprite
import math

class StateBulb(CircleSprite.CircleSprite):
    def __init__(self,maxNum, minNum):
        super().__init__((0,0),16,(10,10,10))
        
        self.maxNum = maxNum
        self.minNum = minNum
    
    
    def setState(self,num):
        num = max(min(num,self.maxNum),self.minNum)
        self.setColor((10,255 * (num / (self.maxNum - self.minNum)),10))