# routes_crime.py
from fastapi import APIRouter, Depends
from db import get_database # FLAT IMPORT
from crud import get_crimes_in_bbox # FLAT IMPORT
from models import CrimeDataModel # FLAT IMPORT
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter(tags=["Crime Data"], prefix="/crimes")
@router.get("/", response_model=List[CrimeDataModel])
async def list_crimes(
    min_lat: float, max_lat: float, min_lon: float, max_lon: float,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    crimes = await get_crimes_in_bbox(db, min_lon, max_lon, min_lat, max_lat)
    return crimes