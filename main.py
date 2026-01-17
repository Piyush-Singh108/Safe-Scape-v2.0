from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import connect_to_mongo, close_mongo_connection
import crime, routing

app = FastAPI(title="SafeScape v2.0")

# 🔑 FIXED CORS (ALLOW ALL DURING DEV)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(crime.router, prefix="/api/v1")
app.include_router(routing.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "SafeScape backend running"}
