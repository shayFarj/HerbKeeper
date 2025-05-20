import CircleSprite
import math
import Constants

class StateBulb(CircleSprite.CircleSprite):
    def __init__(self,maxNum, minNum,min_color,max_color,mid_color = None):
        super().__init__((0,0),16,(10,10,10))
        
        self.maxNum = max(maxNum,minNum)
        self.minNum = min(minNum,maxNum)

        self.min_color=min_color
        self.max_color = max_color
        self.mid_color = mid_color


    
    def setState(self,num):

        if self.mid_color == None:
            c_diff = (self.max_color[0] - self.min_color[0],self.max_color[1] - self.min_color[1],self.max_color[2] - self.min_color[2])

            num = min(max(num,self.minNum),self.maxNum)

            interpol = (num - self.minNum) / (self.maxNum - self.minNum)

            self.setColor(colorInterpol(self.min_color,self.max_color,interpol))
        else:
            midNum = self.minNum + (self.maxNum - self.minNum) / 2

            if num > midNum:
                num = min(num,self.maxNum)
                interpol = (num - midNum) / (self.maxNum - midNum)

                self.setColor(colorInterpol(self.mid_color,self.max_color,interpol))

            else:
                num = max(self.minNum,num)
                interpol = (midNum - num) / (midNum - self.minNum)

                self.setColor(colorInterpol(self.mid_color,self.min_color,interpol))
            

def colorInterpol(color1,color2,t):
    return color1[0] + (color2[0] - color1[0]) * t, color1[1] + (color2[1] - color1[1]) * t, color1[2] + (color2[2] - color1[2]) * t