from fastapi import FastAPI
from pydantic import BaseModel
from src.algorithm import Location, nearest_neighbor, ortools_route, total_route_distance

app = FastAPI()

class LocationInput(BaseModel):
    name: str
    lat: float
    lng: float

class RouteRequest(BaseModel):
    locations: list[LocationInput]

@app.post("/optimize-route")
def optimize_route(request: RouteRequest):
    locations = [Location(l.name, l.lat, l.lng) for l in request.locations]
    
    nn_route = nearest_neighbor(locations)
    nn_distance = total_route_distance(nn_route)
    
    or_route = ortools_route(locations)
    or_distance = total_route_distance(or_route)
    
    if nn_distance == 0:
        improvement = 0.0
    else:
        improvement = round(((nn_distance - or_distance) / nn_distance) * 100, 2)

    return {
        "nearest_neighbor": {
            "route": [{"name": s.name, "lat": s.lat, "lng": s.lng} for s in nn_route],
            "total_distance": round(nn_distance, 4)
        },
        "ortools": {
            "route": [{"name": s.name, "lat": s.lat, "lng": s.lng} for s in or_route],
            "total_distance": round(or_distance, 4)
        },
        "improvement_percent": improvement
    }