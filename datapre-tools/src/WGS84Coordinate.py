from geopy.distance import vincenty

class WGS84Coordinate:
    
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
    def toString(self):
        return "WGS84Coordinate(latitude:" + str(self.latitude) + ",longitude:" + str(self.longitude) + ")"

    def distance(self, otherCoordinate):
        return vincenty((self.latitude, self.longitude), (otherCoordinate.latitude, otherCoordinate.longitude)).meters
    