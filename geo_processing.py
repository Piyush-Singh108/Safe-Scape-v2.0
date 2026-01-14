# services_geo.py
from typing import List, Dict

def get_candidate_routes(start_coords: tuple, end_coords: tuple) -> List[Dict]:
    """Mocks an external API call to get multiple route options."""
    route_a = "fast_route_polyline_ABCDEFGHIJ"
    route_b = "safer_route_polyline_KLMNOPQRST" 
    
    return [
        {"polyline": route_a, "duration_minutes": 15.0, "distance_km": 5.2},
        {"polyline": route_b, "duration_minutes": 18.0, "distance_km": 5.8}
    ]

def segment_route_polyline(polyline: str) -> List[tuple]:
    """Mocks breaking a route polyline into evenly spaced points."""
    # Mocking: 6 points in Pune's general coordinates
    return [
        (73.70, 18.50), (73.73, 18.51), (73.76, 18.52), 
        (73.79, 18.53), (73.82, 18.54), (73.85, 18.55)
    ]