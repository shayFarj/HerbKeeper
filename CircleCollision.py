import CollisionShape
import RectCollision

class CircleCollision(CollisionShape.CollisionShape):
    def __init__(self,pos,radius):
        super().__init__(pos)
        self.radius = radius

    def collides(self,shape):
        if type(shape) is CircleCollision:
            distance_x = self.pos[0] - shape.pos[0]
            distance_y = self.pos[1] - shape.pos[1]
            return (distance_x**2 + distance_y**2) <= ((self.radius + shape.radius)**2)
        
        if type(shape) is RectCollision.rectCollision:
            distance = (abs(shape.pos[0] - self.pos[0]),abs(shape.pos[1] - self.pos[1]))

            if distance[0] > (shape.size2[0] + self.radius):
                return False
            if distance[1] > (shape.size2[1] + self.radius):
                return False
            
            if distance[0] <= shape.size2[0]:
                return True
            if distance[1] <= shape.size2[1]:
                return True
            
            cornerDistance_sq = (distance[0] - shape.size2[0])**2 + (distance[1] - shape.size2[1])**2
            return cornerDistance_sq <= self.radius**2