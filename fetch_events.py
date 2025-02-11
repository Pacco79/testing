import requests
import json
import pandas as pd
from geopy.distance import geodesic

# API details
url = "https://api.predicthq.com/v1/events/"
headers = {
    "Authorization": "Bearer tMx4SwCE1w_YcZ3ESwBsi35L8n7fX_bLIfCBwkj6",
}

# Query parameters
params = {
    "q": "outdoor",
    "active.gte": "2025-01-01",
    "active.lte": "2025-12-31",
    "location.origin": "53.7676,-0.3274",  # Coordinates for Hull
    "location.scope": "200mi",             # Radius around Hull in miles
    "country": "GB",                       # Ensuring we specify United Kingdom
    "category": "community,concerts,expos,festivals,performing-arts",  # Comma-separated categories
    "status": "active"
}

# Initialize results list and page number
results = []
offset = 0

while True:
    # Update query parameters with current offset for pagination
    params['offset'] = offset
    response = requests.get(url, headers=headers, params=params)
    events = response.json()

    if response.status_code != 200:
        print(f"Error: {events.get('error', 'Failed to fetch data')} (status code: {response.status_code})")
        break

    # Fetch results and add to list
    new_results = events.get('results', [])
    if not new_results:
        break

    results.extend(new_results)
    offset += len(new_results)

# Convert to DataFrame if results are found
if results:
    df = pd.DataFrame(results)

    # Check for NaN values and handle them
    for col in df.columns:
        if df[col].dtype == 'float64':
            df[col].fillna(0, inplace=True)
        else:
            df[col].fillna('N/A', inplace=True)

    # Select only the required fields
    required_fields = [
        'title', 'description', 'category', 'phq_attendance', 'entities', 'duration',
        'start', 'start_local', 'end', 'end_local', 'updated', 'first_seen',
        'location', 'geo', 'place_hierarchies', 'state'
    ]
    df = df[required_fields]

    # Define a function to calculate distance from Hull
    def calculate_distance(row):
        hull_coords = (53.7676, -0.3274)
        try:
            event_coords = (row['geo']['geometry']['coordinates'][1], row['geo']['geometry']['coordinates'][0])
            return geodesic(hull_coords, event_coords).miles
        except KeyError:
            return float('inf')  # Assign a high value if coordinates are missing

    # Apply distance calculation and sort DataFrame
    df['distance_from_hull'] = df.apply(calculate_distance, axis=1)
    df = df.sort_values('distance_from_hull')

    # Save to CSV
    df.to_csv("outdoor_events_2025_hull_sorted.csv", index=False)
    print("Data saved to outdoor_events_2025_hull_sorted.csv")
else:
    print("No events found for the given criteria.")
