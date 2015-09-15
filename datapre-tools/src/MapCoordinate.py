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

