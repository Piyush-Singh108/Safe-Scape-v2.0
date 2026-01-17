import requests

def geocode_address(address: str):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "SafeScape/1.0"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if not data:
        raise ValueError("Address not found")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    return lat, lon
