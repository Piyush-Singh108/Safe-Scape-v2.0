# models.py
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Callable
from datetime import datetime
from bson import ObjectId
from pydantic_core import CoreSchema, core_schema


# --- Custom Pydantic Type for MongoDB ObjectId ---
class PyObjectId(ObjectId):
    """
    Custom type to handle MongoDB ObjectIds in Pydantic v2.
    Uses __get_pydantic_core_schema__ for correct schema generation.
    """

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        """The core validation logic: converts strings/bytes to ObjectId."""
        if isinstance(v, bytes):
            v = v.decode('utf-8')
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    # Pydantic v2 CORE SCHEMA METHOD: Defines validation and schema representation
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        
        # 1. Define the validator using the 'validate' class method
        validator = core_schema.no_info_plain_validator_function(cls.validate)
        
        # 2. Return a schema that accepts the Python type but represents it as a string in JSON
        return core_schema.json_or_python_schema(
            # Schema for Python input (handles validation)
            python_schema=core_schema.with_default_schema(validator),
            # Schema for JSON output (FastAPI docs/response will show string)
            json_schema=core_schema.str_schema(),
            # Serialization: ensures MongoDB's ObjectId is converted to string on response
            serialization=core_schema.to_string_ser_schema(),
        )

# --- Database Models (Crime Data) ---
class CrimeDataModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    crime_type: str = Field(..., description="e.g., 'Theft', 'Assault'")
    severity_score: int = Field(..., ge=1, le=10)
    incident_time: datetime = Field(...)
    
    # GeoJSON format for MongoDB 2dsphere index
    # Note: Coordinates are [longitude, latitude]
    location: dict = Field(..., example={"type": "Point", "coordinates": [-74.0060, 40.7128]}) 
    
    class Config:
        # Allows Pydantic to work with MongoDB's custom types and field names
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


# --- API Request/Response Models (Routing) ---
class RouteRequest(BaseModel):
    """Model for requesting a safe route"""
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    time_of_travel: Optional[datetime] = Field(default_factory=datetime.now)

class ScoredRouteResponse(BaseModel):
    """Model for the returned safe route"""
    safety_score: float = Field(..., description="Lower is safer")
    duration_minutes: float
    distance_km: float
    route_polyline: str = Field(..., description="Encoded polyline string for map display")