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
    ac = Vector(vectorA.x - vectorC.x, vectorA.y - vectorC.y)
    caXcd = ca.crossProduct(cd)
    abXcd = ab.crossProduct(cd)
    acXab = ac.crossProduct(ab)
    cdXab = cd.crossProduct(ab)
    if abs(abXcd) - 0.0000000000001 < 0:
        return None 
    t = caXcd / abXcd
    u = acXab / cdXab
    if t > 0 and t < 1 and u > 0 and u < 1:
#        print("t: " + str(t))
        return Vector(vectorA.x + t * ab.x, vectorA.y + t * ab.y)
    else:
        return None
    
def sign(p1x, p1y, p2x, p2y, p3x, p3y):
    return ((p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y)) < 0.0

def pointInTriangle(a, b, c, p):
    
        x1 = a.x
        x2 = b.x
        x3 = c.x
        y1 = a.y
        y2 = b.y
        y3 = c.y
        x = p.x
        y = p.y
        
        b1 = sign(x, y, x1, y1, x2, y2)
        b2 = sign(x, y, x2, y2, x3, y3)
        
        if b1 != b2:
            return False
        
        b3 = sign(x, y, x3, y3, x1, y1)
        
        if b2 != b3:
            return False
        
        return True
    