from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["SafeScapeDB"]
collection = db["crime_collection"]

updated = 0

for doc in collection.find({
    "Latitude": {"$exists": True},
    "Longitude": {"$exists": True}
}):
    lat = doc.get("Latitude")
    lon = doc.get("Longitude")

    if lat is None or lon is None:
        continue

    collection.update_one(
        {"_id": doc["_id"]},
        {
            "$set": {
                "location": {
                    "type": "Point",
                    "coordinates": [lon, lat]  # 🔑 lon, lat order
                }
            }
        }
    )
    updated += 1

print(f"✅ Updated {updated} documents with GeoJSON location")
