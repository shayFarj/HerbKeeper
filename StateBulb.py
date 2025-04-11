import CircleSprite

class StateBulb(CircleSprite.CircleSprite):
    def __init__(self,maxNum, minNum):
        super.__init__(self,(0,0),16,(10,10,10))
        
        self.maxNum = maxNum
        self.minNum = minNum
    
    def self.minN