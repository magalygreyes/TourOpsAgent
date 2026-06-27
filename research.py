import requests
from planner import build_plan

# Turn a city name into map coordinates.
def geocode(city):
    city = city.split(",")[0].strip()
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1})
    results = r.json().get("results")
    if not results:
        return None
    top = results[0]
    return top["latitude"], top["longitude"]

# Get current weather for those coordinates.
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    r = requests.get(url, params={
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "temperature_unit": "fahrenheit",
    })
    return r.json()["current"]["temperature_2m"]

# Find real venues in a city using free OpenStreetMap data.
def find_venues(city, limit=3):
    coords = geocode(city)
    if not coords:
        return []
    lat, lon = coords
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"~"nightclub|bar|theatre|community_centre"](around:12000,{lat},{lon});
      node["leisure"="dance"](around:12000,{lat},{lon});
    );
    out body 15;
    """
    try:
        r = requests.get("https://overpass-api.de/api/interpreter", params={"data": query}, timeout=30)
        elements = r.json().get("elements", [])
    except Exception:
        return ["venue lookup busy, try again"]
    venues = []
    for el in elements:
        name = el.get("tags", {}).get("name")
        if name:
            venues.append(name)
        if len(venues) >= limit:
            break
    return venues

# Turn the Planner's vehicle hint into a transport note.
def transport_note(vehicle_hint):
    return f"{vehicle_hint}. Confirm rental availability per city."

# Gather all research for a tour and return it as data.
def run_research(tour_description):
    plan = build_plan(tour_description)
    stops = []
    for stop in plan["stops"]:
        city = stop["city"]
        coords = geocode(city)
        if coords:
            temp = get_weather(coords[0], coords[1])
            weather = f"{temp}F (current reading)"
        else:
            weather = "weather unavailable"
        venues = find_venues(city)
        venue_line = ", ".join(venues) if venues else "no venues found"
        stops.append({
            "city": city,
            "date": stop.get("date", ""),
            "weather": weather,
            "transport": transport_note(plan["vehicle_hint"]),
            "venues": venue_line,
        })
    return {
        "band_name": plan["band_name"],
        "party_size": plan["party_size"],
        "vehicle_hint": plan["vehicle_hint"],
        "stops": stops,
    }


if __name__ == "__main__":
    sample = """
    The band is Las Cafeteras, 6 people plus gear.
    We play Austin on August 10, Houston on August 12, San Antonio on August 14.
    Mostly driving between cities. Mid-size budget.
    """
    data = run_research(sample)
    print("Researching tour for:", data["band_name"])
    print()
    for s in data["stops"]:
        print(s["city"], s["date"])
        print("  weather:", s["weather"])
        print("  transport:", s["transport"])
        print("  venues:", s["venues"])
        print()