import math


class Location:                                                             #Location struct
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

def calculate_distance(loc1: Location, loc2: Location) -> float:            #Euclidean Distance
    x = (loc1.x - loc2.x)**2
    y = (loc1.y - loc2.y)**2

    d = math.sqrt(x + y)
    return d

def nearest_neighbor(locations: list) -> list:                              #Calculating route using Nearest Neighbour algorithm
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

