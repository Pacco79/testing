# config.py

# API Configuration
API_URL = "https://api.predicthq.com/v1/events/"
API_HEADERS = {
    "Authorization": "Bearer tMx4SwCE1w_YcZ3ESwBsi35L8n7fX_bLIfCBwkj6",
}
API_PARAMS = {
    "q": "outdoor",
    "active.gte": "2025-01-01",
    "active.lte": "2025-12-31",
    "location.origin": "53.7676,-0.3274",  # Coordinates for Hull
    "location.scope": "200mi",             # Radius around Hull in miles
    "country": "GB",                       # Ensuring we specify United Kingdom
    "category": "community,concerts,expos,festivals,performing-arts",  # Comma-separated categories
    "status": "active"
}
