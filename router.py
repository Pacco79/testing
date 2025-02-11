# routes.py

import requests
import pandas as pd
from flask import Flask, render_template
from geopy.distance import geodesic
from config import API_URL, API_HEADERS, API_PARAMS

def init_routes(app):
    @app.route('/')
    def index():
        return "Welcome to the Events API"

    @app.route('/events')
    def get_events():
        try:
            params = API_PARAMS.copy()
            results = []
            offset = 0

            while True:
                # Update query parameters with current offset for pagination
                params['offset'] = offset
                response = requests.get(API_URL, headers=API_HEADERS, params=params)
                events = response.json()

                if response.status_code != 200:
                    return f"Error fetching data: {events.get('error', 'Failed to fetch data')} (status code: {response.status_code})", 500

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

                # Convert the DataFrame to HTML
                html_table = df.to_html(classes='table table-striped', index=False)
                return render_template('index.html', table=html_table)

            else:
                return "No events found for the given criteria."

        except requests.exceptions.RequestException as e:
            return f"Error fetching data: {e}", 500
