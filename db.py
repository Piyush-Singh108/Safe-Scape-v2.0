# db.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import settings # FLAT IMPORT

class MongoDB:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(settings.MONGO_URI)
    mongodb.database = mongodb.client[settings.DB_NAME]
    print("✅ Connected to MongoDB successfully!")
    await mongodb.database["crime_collection"].create_index([("location", "2dsphere")], background=True)

async def close_mongo_connection():
    mongodb.client.close()
    print("❌ Disconnected from MongoDB.")

def get_database() -> AsyncIOMotorDatabase:
    return mongodb.database