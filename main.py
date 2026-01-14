# main.py
from fastapi import FastAPI
from db import connect_to_mongo, close_mongo_connection # FLAT IMPORT
import health, crime, routing # FLAT IMPORT

app = FastAPI(
    title="SafeScape v2.0 Backend",
    description="FastAPI application for crime mapping and safety routing."
)

# Event Handlers
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Router Inclusion
app.include_router(health.router)
app.include_router(crime.router, prefix="/api/v1")
app.include_router(routing.router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to SafeScape v2.0 API. Check /docs for documentation."}