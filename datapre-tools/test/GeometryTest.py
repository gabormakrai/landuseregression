from Geometry import linelineIntersection
from Vector import Vector
        
t1 = linelineIntersection(Vector(0, 0), Vector(1,1), Vector(0, 1), Vector(1, 0))
print(t1.toString())
t2 = linelineIntersection(Vector(0, 0), Vector(1,1), Vector(0, 1), Vector(1, 2))
if t2 == None:
    print("None")
else:
    print(t2.toString())
