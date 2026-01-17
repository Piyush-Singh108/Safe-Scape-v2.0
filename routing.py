# routing.py
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
import random

from db import get_database
from crud import get_crimes_near_segment
from models import AddressRouteRequest
from geo_processing import get_candidate_routes, segment_route_polyline
from scoring import calculate_segment_risk
from config import settings
from geo.geocoding import geocode_address

router = APIRouter(tags=["Routing"], prefix="/route")


@router.post("/safe_route_by_address")
async def get_safest_route_by_address(
    request: AddressRouteRequest,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # -----------------------------
    # STEP 1: GEOCODE ADDRESSES
    # -----------------------------
    start_lat, start_lon = geocode_address(request.start_address)
    end_lat, end_lon = geocode_address(request.end_address)

    # -----------------------------
    # STEP 2: FETCH BASE ROUTE
    # -----------------------------
    base_routes = get_candidate_routes(
        (start_lat, start_lon),
        (end_lat, end_lon)
    )

    # Fallback safety
    if not base_routes:
        return {"error": "No route found"}

    base_route = base_routes[0]

    # -----------------------------
    # STEP 3: SIMULATE ALTERNATIVES
    # -----------------------------
    simulated_routes = []
    profiles = ["fastest", "balanced", "safe"]

    for profile in profiles:
        risk_multiplier = {
            "fastest": random.uniform(1.2, 1.4),
            "balanced": random.uniform(0.9, 1.1),
            "safe": random.uniform(0.6, 0.8),
        }[profile]

        distance_multiplier = {
            "fastest": random.uniform(0.9, 1.0),
            "balanced": random.uniform(1.0, 1.1),
            "safe": random.uniform(1.1, 1.25),
        }[profile]

        duration_multiplier = {
            "fastest": random.uniform(0.85, 0.95),
            "balanced": random.uniform(1.0, 1.1),
            "safe": random.uniform(1.15, 1.3),
        }[profile]

        # -----------------------------
        # STEP 4: CALCULATE RISK
        # -----------------------------
        segments = segment_route_polyline(base_route["polyline"])
        base_risk = 0.0

        for lon, lat in segments:
            crimes = await get_crimes_near_segment(
                db=db,
                longitude=lon,
                latitude=lat,
                radius_meters=settings.ROUTE_BUFFER_METERS,
                time_of_travel=request.time_of_travel,
            )
            base_risk += calculate_segment_risk(
                crimes, request.time_of_travel
            )

        simulated_routes.append({
            "route_polyline": base_route["polyline"],
            "distance_km": round(base_route["distance_km"] * distance_multiplier, 2),
            "duration_minutes": round(base_route["duration_minutes"] * duration_multiplier, 1),
            "safety_score": round(base_risk * risk_multiplier, 2),
            "profile": profile
        })

    # -----------------------------
    # STEP 5: PICK SAFEST
    # -----------------------------
    safest_route = min(simulated_routes, key=lambda r: r["safety_score"])

    return {
        "safest_route": safest_route,
        "all_routes": simulated_routes
    }
