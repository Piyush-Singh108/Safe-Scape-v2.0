# services_scoring.py
from typing import List
from datetime import datetime
from models import CrimeDataModel # FLAT IMPORT

def calculate_temporal_factor(incident_time: datetime, travel_time: datetime) -> float:
    time_diff_hours = abs((incident_time - travel_time).total_seconds()) / 3600
    if time_diff_hours < 4: return 1.5
    elif time_diff_hours < 12: return 1.0
    else: return 0.5 

def calculate_segment_risk(
    crimes_near_segment: List[CrimeDataModel], travel_time: datetime
) -> float:
    total_risk = 0.0
    for crime in crimes_near_segment:
        temporal_factor = calculate_temporal_factor(crime.incident_time, travel_time)
        weighted_risk = crime.severity_score * temporal_factor
        total_risk += weighted_risk
    return total_risk