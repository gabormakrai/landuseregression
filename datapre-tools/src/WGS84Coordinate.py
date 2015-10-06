#from geopy.distance import vincenty
from MathTools import MathTools, bound, degreeToRadian
import math

class WGS84Coordinate:
    """
    This class represents a coordinate in the WGS84 Projection system
    latitude is between -90.0 and 90.0
    longitude is between -180.0 and 180.0
    """
    
    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        
    def toString(self):
        return "WGS84Coordinate(latitude:" + str(self.latitude) + ",longitude:" + str(self.longitude) + ")"

    def distance(self, otherCoordinate):
#        otherWgs = otherCoordinate.toWGS84Coordinate()
#        return vincenty((self.latitude, self.longitude), (otherWgs.latitude, otherWgs.longitude)).meters
        c1 = otherCoordinate.toWGS84Coordinate()
        
        dLat = degreeToRadian(self.latitude - c1.latitude)
        dLong = degreeToRadian(self.longitude - c1.longitude)
        R = 6371000.0
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(degreeToRadian(self.latitude)) * math.cos(degreeToRadian(c1.latitude)) * math.sin(dLong/2) * math.sin(dLong/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        
        return d;
    
    def toZoomMapCoordinate(self):
        from ZoomMapCoordinate import ZoomMapCoordinate
        x = MathTools.ORIGIN_X + self.longitude * MathTools.PIXELS_PER_LONGITUDE_DEGREE
        siny = bound(math.sin(degreeToRadian(self.latitude)), -0.9999, 0.9999)
        y = MathTools.ORIGIN_Y + 0.5 * math.log((1 + siny) / (1 - siny)) * - MathTools.PIXELS_PER_LONGITUDE_RADIAN
        return ZoomMapCoordinate(x * 2.0, y * 2.0, 1)
    
    # Truncating to 0.9999 effectively limits latitude to 89.189. This is
    # about a third of a tile past the edge of the world tile.
    def toMapCoordinate(self):
        from MapCoordinate import MapCoordinate
        x = MathTools.ORIGIN_X + self.longitude * MathTools.PIXELS_PER_LONGITUDE_DEGREE
        siny = bound(math.sin(degreeToRadian(self.latitude)), -0.9999, 0.9999)
        y = MathTools.ORIGIN_Y + 0.5 * math.log((1 + siny) / (1 - siny)) * - MathTools.PIXELS_PER_LONGITUDE_RADIAN
        return MapCoordinate(x * 2.0, y * 2.0)
    
    def toWGS84Coordinate(self):
        return self
