import CircleSprite
import math
import Constants

class StateBulb(CircleSprite.CircleSprite):
    def __init__(self,maxNum, minNum,color,reverse):
        super().__init__((0,0),16,(10,10,10))
        
        self.maxNum = max(maxNum,minNum)
        self.minNum = min(minNum,maxNum)
        self.color=color
        self.reverse=reverse
    
    def setState(self,num):
        num = max(min(num,self.maxNum),self.minNum)
        if not self.reverse:
            interpol= (num / (self.maxNum - self.minNum))
        else:
            interpol=(abs(num)/(self.maxNum -self.minNum))

        if self.color == "red":
            self.setColor((10+245*interpol,10,10))
        
        if self.color == "green":
            self.setColor((10,10+245*interpol,10))