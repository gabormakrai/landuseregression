"""
This files contains useful functions for calculating several
important geometry features
"""
from Vector import Vector

"""
Function which calculates the intersection point of two lines
return: None if there is no intersection
        otherwise a Vector contains the intersection point  
"""        
def linelineIntersection(a, b, c, d):
    if a is Vector:
        vectorA = a
        vectorB = b
        vectorC = c
        vectorD = d
    else:
        vectorA = Vector(a.x, a.y)
        vectorB = Vector(b.x, b.y)
        vectorC = Vector(c.x, c.y)
        vectorD = Vector(d.x, d.y)
        
    ca = Vector(vectorC.x - vectorA.x, vectorC.y - vectorA.y)
    ab = Vector(vectorB.x - vectorA.x, vectorB.y - vectorA.y)
    cd = Vector(vectorD.x - vectorC.x, vectorD.y - vectorC.y)
    caXcd = ca.crossProduct(cd)
    abXcd = ab.crossProduct(cd)
    if abs(abXcd) - 0.00000000001 < 0:
        return None 
    t = caXcd / abXcd
    if t > 0 and t < 1:
        return Vector(vectorA.x + t * ab.x, vectorA.y + t * ab.y)
    else:
        return None
