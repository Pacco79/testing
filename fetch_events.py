import requests
import pandas as pd
from flask import Flask, render_template

# Fetch data from the API
response = requests.get('https://api.yourservice.com/events')
data = response.json()

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Create the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    # Convert the DataFrame to HTML
    html_table = df.to_html(classes='table table-striped', index=False)
    return render_template('index.html', table=html_table)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
