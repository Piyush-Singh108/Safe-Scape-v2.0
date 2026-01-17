# models.py
from pydantic import BaseModel, Field
from typing import Optional, Any, Callable
from datetime import datetime
from bson import ObjectId
from pydantic_core import CoreSchema, core_schema
from pydantic import BaseModel
from datetime import datetime
from typing import Optional



# ======================================================
# 🔑 Custom ObjectId for Pydantic v2
# ======================================================
class PyObjectId(ObjectId):

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        validator = core_schema.no_info_plain_validator_function(cls.validate)
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_default_schema(validator),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )


# ======================================================
# 🗄️ INTERNAL DB MODEL
# ======================================================
class CrimeDataModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    crime_type: str
    severity_score: Optional[int] = None   # ✅ FIXED
    incident_time: Optional[datetime] = None
    location: dict

    area_name: Optional[str] = None
    police_station: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ======================================================
# 🌐 API RESPONSE MODEL (FIXED)
# ======================================================
class CrimeOut(BaseModel):
    id: str
    crime_type: str
    severity_score: Optional[int] = None   # ✅ FIXED
    incident_time: Optional[datetime] = None
    location: dict

    area_name: Optional[str] = None
    police_station: Optional[str] = None


# ======================================================
# 🚦 ROUTING MODELS
# ======================================================
class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    time_of_travel: Optional[datetime] = Field(default_factory=datetime.now)


class ScoredRouteResponse(BaseModel):
    safety_score: float = Field(..., description="Lower is safer")
    duration_minutes: float
    distance_km: float
    route_polyline: str

# ======================================================
# 🏠 Address-based routing request (NEW)
# ======================================================
class AddressRouteRequest(BaseModel):
    start_address: str
    end_address: str
    time_of_travel: Optional[datetime] = Field(default_factory=datetime.now)

