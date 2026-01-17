from fastapi import APIRouter, Query, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime, time
from typing import List

from db import get_crime_collection
from models import CrimeOut

router = APIRouter(tags=["Crimes"])

SEVERITY_MAP = {
    "Theft": 2,
    "Cheating": 2,
    "Fraud": 3,
    "Vandalism": 3,
    "Assault": 4,
    "Robbery": 5,
    "Kidnapping": 5,
    "Sexual Assault": 6,
    "Shooting": 7,
    "Murder": 10,
}

MAX_RESULTS = 500

@router.get("/crimes/", response_model=List[CrimeOut])
async def list_crimes(
    min_lat: float = Query(...),
    max_lat: float = Query(...),
    min_lon: float = Query(...),
    max_lon: float = Query(...),
    collection: AsyncIOMotorCollection = Depends(get_crime_collection),
):
    # ⚠️ NO GEO QUERY — YOUR DATA IS NOT GEOJSON
    query = {
        "Latitude": {"$gte": min_lat, "$lte": max_lat},
        "Longitude": {"$gte": min_lon, "$lte": max_lon},
    }

    crimes = []

    cursor = (
        collection
        .find(query)
        .sort("Crime_Date", -1)
        .limit(MAX_RESULTS)
    )

    async for doc in cursor:
        try:
            lat = float(doc.get("Latitude"))
            lon = float(doc.get("Longitude"))
        except:
            continue

        crime_type = doc.get("Crime_Type", "Unknown")
        severity_score = SEVERITY_MAP.get(crime_type, 1)

        crime_date = doc.get("Crime_Date")
        crime_time = doc.get("Crime_Time")

        if isinstance(crime_date, str):
            crime_date = datetime.fromisoformat(crime_date.replace("Z", ""))

        if isinstance(crime_time, str):
            crime_time = datetime.strptime(crime_time, "%H:%M:%S").time()
        else:
            crime_time = time(0, 0)

        incident_time = datetime.combine(crime_date.date(), crime_time)

        crimes.append({
            "id": str(doc["_id"]),
            "crime_type": crime_type,
            "severity_score": severity_score,
            "incident_time": incident_time,
            "location": {
                "type": "Point",
                "coordinates": [lon, lat],  # ✅ LEAFLET READY
            },
            "area_name": doc.get("Area_Name"),
            "police_station": doc.get("Police_Station"),
        })

    return crimes
