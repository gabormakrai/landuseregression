from Geometry import linelineIntersection
from Vector import Vector
from MapCoordinate import MapCoordinate
        
t1 = linelineIntersection(Vector(0, 0), Vector(1,1), Vector(0, 1), Vector(1, 0))
print(t1.toString())
t2 = linelineIntersection(Vector(0, 0), Vector(1,1), Vector(0, 1), Vector(1, 2))
if t2 == None:
    print("None")
else:
    print(t2.toString())

t3 = linelineIntersection(MapCoordinate(0, 0), MapCoordinate(1,1), MapCoordinate(0, 1), MapCoordinate(1, 0))
print(t3.toString())
