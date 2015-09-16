from geopy.distance import vincenty
from WGS84Coordinate import WGS84Coordinate

newport_ri = (41.49008, -71.312796)
cleveland_oh = (41.499498, -81.695391)
print("distance(newport,cleveland).miles = " +  str(vincenty(newport_ri, cleveland_oh).miles))

np = WGS84Coordinate(41.49008, -71.312796)
cl = WGS84Coordinate(41.499498, -81.695391)

print("distance(newport,cleveland) = " + str(np.distance(cl)))

barcelona = WGS84Coordinate(41.3879169, 2.16991870)
madrid = WGS84Coordinate(40.4167413, -3.7032498)

print("distance(barcelona, madrid) = " + str(barcelona.distance(madrid)))


c1 = WGS84Coordinate(66.51326044311185,-90.0)
c2 = c1.toMapCoordinate()
c3 = c1.toZoomMapCoordinate()
c4 = c1.toWGS84Coordinate()

print("c1: " + c1.toString())
print("c2: " + c2.toString())
print("c3: " + c3.toString())
print("c4: " + c4.toString())

