from shapely.geometry import Polygon, Point

poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0)))

print(poly.contains(Point(0.1, 0.1)))