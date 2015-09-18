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
    ca = Vector(c.x - a.x, c.y - a.y)
    ab = Vector(b.x - a.x, b.y - a.y)
    cd = Vector(d.x - c.x, d.y - c.y)
    caXcd = ca.crossProduct(cd)
    abXcd = ab.crossProduct(cd)
    if abs(abXcd) - 0.00000000001 < 0:
        return None 
    t = caXcd / abXcd
    if t > 0 and t < 1:
        return Vector(a.x + t * ab.x, a.y + t * ab.y)
    else:
        return None
