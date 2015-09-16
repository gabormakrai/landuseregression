from MathTools import MathTools, radianToDegree
import math

class MapCoordinate:
    
    """
    This class represents a coordinate in the Web Marcator projection system
    x and y are between 0.0 and 512.0 
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def toString(self):
        return "MapCoordinate(x:" + str(self.x) + ",y:" + str(self.y) + ")"

    def toWGS84Coorinate(self):
        from WGS84Coordinate import WGS84Coordinate
        lng = (self.x / 2.0 - MathTools.ORIGIN_X) / MathTools.PIXELS_PER_LONGITUDE_DEGREE
        latRadians = (self.y / 2.0 - MathTools.ORIGIN_Y) / - MathTools.PIXELS_PER_LONGITUDE_RADIAN
        lat = radianToDegree(2.0 * math.atan(math.exp(latRadians)) - math.pi / 2.0)
        return WGS84Coordinate(lat, lng)
    
    def toMapCoordinate(self):
        return self
    
    def toZoomMapCoordinate(self):
        from ZoomMapCoordinate import ZoomMapCoordinate
        return ZoomMapCoordinate(self.x, self.y, 1)
    
    def distance(self, otherCoordinate):
        return self.toWGS84Coorinate().distance(otherCoordinate)
