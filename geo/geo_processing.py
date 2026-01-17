# geo_processing.py
import requests
import polyline
from typing import List, Tuple
from config import settings

ORS_BASE = "https://api.openrouteservice.org/v2/directions"

# 🚗 Multiple routing profiles → REAL variation
PROFILES = [
    "driving-car",
    "cycling-regular",
    "foot-walking"
]

def get_candidate_routes(
    start_coords: Tuple[float, float],
    end_coords: Tuple[float, float]
):
    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json"
    }

    all_routes = []

    for profile in PROFILES:
        url = f"{ORS_BASE}/{profile}"

        body = {
            "coordinates": [
                [start_coords[1], start_coords[0]],
                [end_coords[1], end_coords[0]]
            ],
            "alternative_routes": {
                "target_count": 2,
                "share_factor": 0.3,
                "weight_factor": 1.8
            }
        }

        response = requests.post(url, json=body, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        for route in data.get("routes", []):
            all_routes.append({
                "polyline": route["geometry"],
                "distance_km": route["summary"]["distance"] / 1000,
                "duration_minutes": route["summary"]["duration"] / 60,
                "profile": profile
            })

    return all_routes


def segment_route_polyline(
    encoded_polyline: str,
    step: int = 8
) -> List[Tuple[float, float]]:
    decoded = polyline.decode(encoded_polyline)

    segments = []
    for i in range(0, len(decoded), step):
        lat, lon = decoded[i]
        segments.append((lon, lat))  # MongoDB expects lon, lat

    return segments
