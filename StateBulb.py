import CircleSprite
import math
import Constants

class StateBulb(CircleSprite.CircleSprite):
    def __init__(self,maxNum, minNum,color):
        super().__init__((0,0),16,(10,10,10))
        
        self.maxNum = maxNum
        self.minNum = minNum
        self.color=color
    
    def setState(self,num):
        num = max(min(num,self.maxNum),self.minNum)
        interpol= (num / (self.maxNum - self.minNum))

        if self.color == "red":
            self.setColor((10+245*interpol,10,10))
        
        if self.color == "green":
            self.setColor((10,10+245*interpol,10))