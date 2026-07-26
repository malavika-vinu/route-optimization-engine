from fastapi import FastAPI
from pydantic import BaseModel
from src.algorithm import Location, nearest_neighbor

app = FastAPI()

class LocationInput(BaseModel):
    name: str
    lat: float
    lng: float

class RouteRequest(BaseModel):
    locations: list[LocationInput]

@app.post('/optimize-route')

def optimize_route(request: RouteRequest):
    locations = [Location(l.name, l.lat, l.lng) for l in request.locations]
    route = nearest_neighbor(locations)
    return {"route" : [{"name": stop.name, "lat": stop.lat, "lng": stop.lng} for stop in route]}