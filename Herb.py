import CircleSprite
import Constants

class Herb(CircleSprite.CircleSprite):
    def __init__(self,pos):
        super().__init__(pos,14,Constants.PASTEL_GREEN)