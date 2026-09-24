import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


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

def build_distance_matrix(locations: list) -> list[list[float]]:
    distance_matrix = [[0] * (len(locations)) for _ in range(len(locations))]
    for i in range(len(locations)):
        for j in range(len(locations)):
            if i == j:
                distance_matrix[i][j] = 0.0
            else:
                distance_matrix[i][j] = calculate_distance(locations[i], locations[j])
    return distance_matrix

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


def total_route_distance(route: list) -> float:
    total = 0.0
    for i in range(len(route) - 1):
        total += calculate_distance(route[i], route[i + 1])
    total += calculate_distance(route[-1], route[0])
    return total

def ortools_route(locations: list) -> list:
    distance_matrix = build_distance_matrix(locations)
    num_locations = len(locations)

    manager = pywrapcp.RoutingIndexManager(num_locations, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node] * 1000)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(5)

    solution = routing.SolveWithParameters(search_parameters)

    route = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(locations[node])
        index = solution.Value(routing.NextVar(index))

    return route


