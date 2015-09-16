from MapCoordinate import MapCoordinate

c = MapCoordinate(5.0, 12.0)
print("c: " + c.toString())

c1 = MapCoordinate(128.0, 128.0)
c2 = c1.toWGS84Coordinate()
print("c1: " + c1.toString())
print("c2: " + c2.toString())

c3 = MapCoordinate(256.0, 256.0)
c4 = c3.toWGS84Coordinate()
print("c3: " + c3.toString())
print("c4: " + c4.toString())

c5 = c1.toZoomMapCoordinate()
print("c5: " + c5.toString())

c6 = c1.toMapCoordinate()
print("c6: " + c6.toString())

