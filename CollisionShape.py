
class CollisionShape:

    def __init__(self,pos) -> None:
        self.pos = pos
    
    def setPosition(self,pos):
       self.pos = pos



    def collides(self,shape) -> bool:
        pass

    def setPosition(self,pos) -> None:
        self.pos = pos


