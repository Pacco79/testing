import requests
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Events API"

@app.route('/events')
def get_events():
    try:
        # Fetch data from the external API
        response = requests.get('https://127.0.0.1/events')
        response.raise_for_status()
        data = response.json()

        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Convert the DataFrame to HTML
        html_table = df.to_html(classes='table table-striped', index=False)
        return render_template('index.html', table=html_table)

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
