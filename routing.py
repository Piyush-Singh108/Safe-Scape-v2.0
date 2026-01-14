# routes_routing.py
from fastapi import APIRouter, Depends
from db import get_database # FLAT IMPORT
from crud import get_crimes_near_segment # FLAT IMPORT
from models import RouteRequest, ScoredRouteResponse # FLAT IMPORT
from geo_processing import get_candidate_routes, segment_route_polyline # FLAT IMPORT
from scoring import calculate_segment_risk # FLAT IMPORT
from config import settings # FLAT IMPORT
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(tags=["Routing"], prefix="/route")

@router.post("/safe_route", response_model=ScoredRouteResponse)
async def get_safest_route(
    request: RouteRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    start_coords = (request.start_lat, request.start_lon)
    end_coords = (request.end_lat, request.end_lon)
    candidate_routes = get_candidate_routes(start_coords, end_coords) 
    
    scored_routes = []
    
    for route in candidate_routes:
        segments = segment_route_polyline(route["polyline"])
        route_risk_score = 0.0
        
        for lon, lat in segments:
            crimes_near = await get_crimes_near_segment(
                db, longitude=lon, latitude=lat,
                radius_meters=settings.ROUTE_BUFFER_METERS,
                time_of_travel=request.time_of_travel
            )
            segment_risk = calculate_segment_risk(crimes_near, request.time_of_travel)
            route_risk_score += segment_risk
            
        scored_routes.append({
            "safety_score": route_risk_score,
            "duration_minutes": route["duration_minutes"],
            "distance_km": route["distance_km"],
            "route_polyline": route["polyline"]
        })
        
    safest_route_data = sorted(scored_routes, key=lambda x: x["safety_score"])[0]
    
    return ScoredRouteResponse(**safest_route_data)