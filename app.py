from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Replace with your actual API Gateway URL
API_URL = "https://xso7ro9h82.execute-api.us-east-1.amazonaws.com/ReadBucket"

@app.route('/')
def index():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()  # This should be a list of records
        return render_template('index.html', records=data)
    except Exception as e:
        return f"Error fetching data: {e}", 500

@app.route('/api')
def api_data():
    """Optional JSON endpoint in Flask itself"""
    response = requests.get(API_URL)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
