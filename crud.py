# crud.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import CrimeDataModel # FLAT IMPORT
from config import settings # FLAT IMPORT
from typing import List
from datetime import datetime

COLLECTION_NAME = "crime_collection"

async def get_crimes_in_bbox(
    db: AsyncIOMotorDatabase, min_lon: float, max_lon: float, min_lat: float, max_lat: float
) -> List[CrimeDataModel]:
    bbox = [[min_lon, min_lat], [max_lon, max_lat]]
    query = {"location": {"$geoWithin": {"$box": bbox}}}
    crime_docs = await db[COLLECTION_NAME].find(query).to_list(settings.MAX_CRIME_FETCH)
    return [CrimeDataModel(**doc) for doc in crime_docs]

async def get_crimes_near_segment(
    db: AsyncIOMotorDatabase, longitude: float, latitude: float, radius_meters: int, time_of_travel: datetime
) -> List[CrimeDataModel]:
    query = {
        "location": {
            "$nearSphere": {
                "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                "$maxDistance": radius_meters
            }
        },
        "incident_time": {"$gte": datetime(time_of_travel.year, time_of_travel.month, 1)}
    }
    crime_docs = await db[COLLECTION_NAME].find(query).to_list(500)
    return [CrimeDataModel(**doc) for doc in crime_docs]