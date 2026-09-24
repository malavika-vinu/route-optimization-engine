from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from src.algorithm import Location, nearest_neighbor, ortools_route

app = FastAPI()

ALGORITHMS = {
    "nearest_neighbor": nearest_neighbor,
    "ortools": ortools_route,
}

class LocationInput(BaseModel):
    name: str
    lat: float
    lng: float

class RouteRequest(BaseModel):
    locations: list[LocationInput]
    algorithm: Literal["nearest_neighbor", "ortools"] = "nearest_neighbor"

@app.post('/optimize-route')
def optimize_route(request: RouteRequest):
    locations = [Location(l.name, l.lat, l.lng) for l in request.locations]
    algorithm_func = ALGORITHMS[request.algorithm]
    route = algorithm_func(locations)
    return {"route": [{"name": stop.name, "lat": stop.lat, "lng": stop.lng} for stop in route]}