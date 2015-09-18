import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    def normalize(self):
        l = self.length()
        self.x /= l
        self.y /= l
    def toString(self):
        return "Vector(x:" + str(self.x) + ",y:" + str(self.y) + ")"
    def crossProduct(self, v):
        return self.x * v.y - self.y * v.x
    def dotProduct(self, v):
        return  self.x * v.x + self.y * v.y
