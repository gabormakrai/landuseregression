from MapCoordinate import MapCoordinate
from MathTools import MathTools, radianToDegree
from WGS84Coordinate import WGS84Coordinate
import math

class InvalidCoordinateDataException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ZoomMapCoordinate:
    """
    Coordinate for Web Marcator projection
    
    0 <= x < 2.0^zoom and 0 <= y < 2.0^zoom 
 
    NorthWest coordinate: 0.0, 0.0 NW
    SouthEast coordinate: 2.0^zoom, 2.0^zoom
    """
    def __init__(self, x, y, zoom):
        tileNumberLimit = 1 << (zoom + 8)
        if x < 0.0 or x > tileNumberLimit:
            raise InvalidCoordinateDataException("Invalid x: " + str(x))
        elif y < 0.0 or y > tileNumberLimit:
            raise InvalidCoordinateDataException("Invalid y: " + str(y))
                
        self.x = x
        self.y = y
        self.zoom = zoom

    def toMapCoordinate(self):
        tileNumber = 1 << (self.zoom - 1)
        return MapCoordinate(self.x / tileNumber, self.y / tileNumber)
    
    def toWGS84Coorindate(self):
        tileNumber = 1 << (self.zoom - 1)
        lng = (self.x / (tileNumber) - MathTools.ORIGIN_X) / MathTools.PIXELS_PER_LONGITUDE_DEGREE
        latRadians = (self.y / (tileNumber) - MathTools.ORIGIN_Y) / - MathTools.PIXELS_PER_LONGITUDE_RADIAN
        lat = radianToDegree(2.0 * math.atan(math.exp(latRadians)) - math.pi / 2.0);
        return WGS84Coordinate(lat, lng)
            
    def toZoomMapCoordinate(self):
        return self

    def toString(self):
        return "ZoomMapCoordinate(x:" + str(self.x) + ",y:" + str(self.y) + ",zoom:" + str(self.zoom) + ")"
