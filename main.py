from fastapi import FastAPI
from pydantic import BaseModel
from src.algorithm import Location, nearest_neighbor

app = FastAPI()

class LocationInput(BaseModel):
    name: str
    x: float
    y: float

class RouteRequest(BaseModel):
    locations: list[LocationInput]

@app.post('/optimize-route')

def optimize_route(request: RouteRequest):
    locations = [Location(l.name, l.x, l.y) for l in request.locations]
    route = nearest_neighbor(locations)
    return {"route" : [{"name": stop.name, "x": stop.x, "y": stop.y} for stop in route]}