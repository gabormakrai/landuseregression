
class MapTile:

    def __init__(self, x, y, zoom):
        
        limit = 1 << zoom
        
        if x < 0:
            while x < 0:
                x += limit
        elif x >= limit:
            while x >= limit:
                x -= limit
        
        if y < 0:
            while y < 0:
                y += limit
        elif y >= limit:
            while y >= limit:
                y -= limit
                
        self.x = x
        self.y = y
        self.zoom = zoom
        
    def getNorthWestCorner(self):
        from ZoomMapCoordinate import ZoomMapCoordinate
        return ZoomMapCoordinate(self.x * 256.0, self.y * 256.0, self.zoom)
    def getNorthEastCorner(self):
        from ZoomMapCoordinate import ZoomMapCoordinate
        return ZoomMapCoordinate((self.x + 1) * 256.0, self.y * 256.0, self.zoom)
    def getSouthEastCorner(self):
        from ZoomMapCoordinate import ZoomMapCoordinate
        return ZoomMapCoordinate((self.x + 1) * 256.0, (self.y + 1) * 256.0, self.zoom)
    def getSouthWestCorner(self):
        from ZoomMapCoordinate import ZoomMapCoordinate
        return ZoomMapCoordinate(self.x * 256.0, (self.y + 1) * 256.0, self.zoom)
    
    def toString(self):
        return  "GoogleMapsTile(x:" + self.x + ",y:" + self.y + ",zoom:" + self.zoom + ")"
    
