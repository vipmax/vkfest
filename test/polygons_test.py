import re

node_re = re.compile('id="(\w+)"')
lat_re = re.compile('lat="(\w+.\w+)"')
lon_re = re.compile('lon="(\w+.\w+)"')
nodes_and_points = {}
with open("/home/maxpetrov/PycharmProjects/vkfest1/data/vkfest_final_zones.osm", "r") as f:
    for line in f.readlines():
        # print(line)
        try:
            node_id = node_re.findall(line)[0]
            lat = lat_re.findall(line)[0]
            lon = lon_re.findall(line)[0]
            # print(node_id, lat, lon)
            nodes_and_points[int(node_id)] = (lat, lon)
        except:
            pass



fnode_re = re.compile('ref="(\w+)"')
fest_re = re.compile('v="vkfest (\w+)"')
with open("/home/maxpetrov/PycharmProjects/vkfest1/data/vkfest_final_zones.osm", "r") as f:
    for line in f.readlines():
        # print(line)
        try:
            fnode_id = fnode_re.findall(line)[0]
            point = nodes_and_points.get(int(fnode_id))
            print(' \t \t ({}, {}),'.format(point[0], point[1]))
        except:
            pass

        try:
            zone_id = fest_re.findall(line)[0]
            print(" \t]), \n \t \'zone\': \'" + zone_id + "\' \n }, \n {  \n 'polygon': Polygon([")
        except:
            pass



