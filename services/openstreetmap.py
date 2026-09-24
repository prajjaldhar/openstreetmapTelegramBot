import requests
import math


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "BusinessFinderBot/1.0"
}


CATEGORY_MAP = {
    "restaurant": "restaurant",
    "cafe": "cafe",
    "hospital": "hospital",
    "pharmacy": "pharmacy",
    "school": "school",
    "college": "college",
    "bank": "bank",
    "hotel": "hotel",
    "gym": "gym",
    "supermarket": "supermarket",
    "bakery": "bakery",
    "dentist": "dentist",
    "clinic": "clinic",
    "police": "police",
    "fuel": "fuel",
}


def get_city_coordinates(city):

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return None

    return (
        float(data[0]["lat"]),
        float(data[0]["lon"])
    )


def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


def search_business(category, city, radius):

    if category not in CATEGORY_MAP:
        return []

    city_coordinates = get_city_coordinates(city)

    if not city_coordinates:
        return []

    city_lat, city_lon = city_coordinates

    osm_category = CATEGORY_MAP[category]

    search_query = f"{osm_category}, {city}"

    params = {
        "q": search_query,
        "format": "json",
        "addressdetails": 1,
        "limit": 50
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for place in data:

        if not place.get("lat") or not place.get("lon"):
            continue

        business_lat = float(place["lat"])
        business_lon = float(place["lon"])

        distance = calculate_distance(
            city_lat,
            city_lon,
            business_lat,
            business_lon
        )

        if distance <= radius:

            address = place.get("address", {})

            results.append({
                "name": place.get(
                    "name",
                    "Business name unavailable"
                ),

                "lat": place.get("lat"),

                "lon": place.get("lon"),

                "display_name": place.get(
                    "display_name",
                    "Address unavailable"
                ),

                "type": place.get(
                    "type",
                    category
                ),

                "address": address,

                "phone": place.get(
                    "phone",
                    address.get("phone", "Not available")
                ),

                "website": place.get(
                    "website",
                    "Not available"
                ),

                "distance": round(distance, 2)
            })

    results.sort(
        key=lambda x: x["distance"]
    )

    return results