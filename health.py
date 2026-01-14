# routes_health.py
from fastapi import APIRouter
router = APIRouter(tags=["Health"])
@router.get("/health")
async def get_health_status():
    return {"status": "ok", "service": "SafeScape Backend v2.0"}