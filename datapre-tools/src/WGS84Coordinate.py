from geopy.distance import vincenty

class WGS84Coordinate:
    """
    This class represents a coordinate in the WGS84 Projection system
    latitude is between -90.0 and 90.0
    longitude is between -180.0 and 180.0
    """
    
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
    def toString(self):
        return "WGS84Coordinate(latitude:" + str(self.latitude) + ",longitude:" + str(self.longitude) + ")"

    def distance(self, otherCoordinate):
        return vincenty((self.latitude, self.longitude), (otherCoordinate.latitude, otherCoordinate.longitude)).meters
    