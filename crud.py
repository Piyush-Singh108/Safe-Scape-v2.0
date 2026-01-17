# crud.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import CrimeDataModel
from typing import List
from datetime import datetime

async def get_crimes_near_segment(
    db: AsyncIOMotorDatabase,
    longitude: float,
    latitude: float,
    radius_meters: int,
    time_of_travel: datetime
):
    query = {
        "location": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": radius_meters
            }
        }
    }

    crime_docs = await db["crime_collection"].find(query).limit(100).to_list(100)

    return crime_docs


    docs = await (
        db["crime_collection"]
        .find(query)
        .limit(200)
        .to_list(length=200)
    )

    crimes = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        crimes.append(CrimeDataModel(**doc))

    return crimes
