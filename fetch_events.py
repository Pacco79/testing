import requests
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Update the API endpoint if needed
        response = requests.get('http://webserver-service-events.infra.svc.cluster.local/events')
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

