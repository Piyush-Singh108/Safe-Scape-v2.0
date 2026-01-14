# seed_db.py - MODIFIED FOR JSON FILE LOADING
import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings # FLAT IMPORT from config.py

# --- Configuration ---
COLLECTION_NAME = "crime_collection"
JSON_FILE_NAME = "transformed_crime_data.json"

async def seed_database():
    """Connects to MongoDB, clears existing data, and inserts data from JSON file."""
    
    print(f"Connecting to MongoDB at: {settings.MONGO_URI}")
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]
    collection = db[COLLECTION_NAME]
    
    try:
        # 1. Load data from the JSON file
        print(f"Loading data from {JSON_FILE_NAME}...")
        with open(JSON_FILE_NAME, 'r') as f:
            records_to_insert = json.load(f)

        # 2. Clear existing data
        print(f"Dropping existing collection: {COLLECTION_NAME}")
        await collection.drop()
        
        # 3. Ensure 2dsphere index (Crucial for fast geospatial queries)
        print("Ensuring 2dsphere index on 'location' field...")
        await collection.create_index([("location", "2dsphere")], background=True)
        
        # 4. Insert records
        print(f"Inserting {len(records_to_insert)} records into MongoDB...")
        
        # NOTE: If your MongoDB version is very old, you might need to use 
        # collection.insert_many(records_to_insert, ordered=False)
        result = await collection.insert_many(records_to_insert)
        
        print(f"✅ Successfully inserted {len(result.inserted_ids)} records.")
        print("Seeding complete! Data is ready for API access.")

    except FileNotFoundError:
        print(f"🚨 Error: JSON file '{JSON_FILE_NAME}' not found in the project root.")
    except Exception as e:
        print(f"🚨 An error occurred during seeding (Is MongoDB running locally?): {e}")
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())