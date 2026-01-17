from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(settings.MONGO_URI)
    mongodb.database = mongodb.client[settings.DB_NAME]

    await mongodb.database[settings.COLLECTION_NAME].create_index(
        [("location", "2dsphere")],
        background=True
    )

    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()

def get_database():
    if mongodb.database is None:
        raise RuntimeError("MongoDB not initialized")
    return mongodb.database

def get_crime_collection():
    return mongodb.database[settings.COLLECTION_NAME]
