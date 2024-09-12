import CollisionShape
import CircleCollision

class rectCollision(CollisionShape.CollisionShape):
    def __init__(self,pos,size):
        self.size = size
        self.pos = pos
        self.size2 = (size[0]/2,size[1]/2)
        self.corners = [[pos[0] - self.size2[0],pos[1] - self.size2[1]],
                            [pos[0] + self.size2[0],pos[1] + self.size2[1]]]
    
    def setPosition(self,pos):
        vector = (self.pos[0] - pos[0],self.pos[1] - pos[1])
        self.pos = pos
        for i in self.corners:
            i[0] += vector[0]
            i[1] += vector[1]

    def collides(self,shape):
        if type(shape) is rectCollision:
            return self.corners[0][0] < shape.corners[1][0] and self.corners[1][0] > shape.corners[0][0] and self.corners[0][1] < shape.corners[1][1] and self.corners[1][1] > shape.corners[0][1]
        
        if type(shape) is CircleCollision.CircleCollision:
            
            distance = (abs(shape.pos[0] - self.pos[0]),abs(shape.pos[1] - self.pos[1]))

            if distance[0] > (self.size2[0] + shape.radius):
                return False
            if distance[1] > (self.size2[1] + shape.radius):
                return False
            
            if distance[0] <= self.size2[0]:
                return True
            if distance[1] <= self.size2[1]:
                return True
            
            cornerDistance_sq = (distance[0] - self.size2[0])**2 + (distance[1] - self.size2[1])**2
            return cornerDistance_sq <= shape.radius**2
