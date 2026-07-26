import math


class Location:                                                             #Location struct
    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

def calculate_distance(loc1: Location, loc2: Location) -> float:            #Euclidean Distance
    x = (loc1.lat - loc2.lat)**2
    y = (loc1.lng - loc2.lng)**2

    d = math.sqrt(x + y)
    return d

def nearest_neighbor(locations: list) -> list:                              #Calculating route using Nearest Neighbor algorithm
    unvisited = locations[1:]
    visited = [locations[0]]

    while unvisited:
        current = visited[-1]
        distances = []
        for l in unvisited:
            d = calculate_distance(current, l)
            distances.append(d)
        nearest_index = distances.index(min(distances))
        visited.append(unvisited[nearest_index])
        unvisited.remove(unvisited[nearest_index])

    return visited

