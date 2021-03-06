from ZoomMapCoordinate import ZoomMapCoordinate

c1 = ZoomMapCoordinate(128.0, 128.0, 1)
print("c1: " + c1.toString())

c2 = c1.toMapCoordinate()
print("c2: " + c2.toString())

c3 = ZoomMapCoordinate(128.0, 128.0, 2)
print("c3: " + c3.toString())

c4 = c3.toMapCoordinate()
print("c4: " + c4.toString())

c5 = c1.toWGS84Coordinate()
print("c5: " + c5.toString())

c6 = c2.toWGS84Coordinate()
print("c6: " + c6.toString())



