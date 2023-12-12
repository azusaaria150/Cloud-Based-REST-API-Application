from flask import Flask, jsonify, request, Response
from google.cloud import firestore

app = Flask(__name__)

# Example of a simple in-memory 'database' for demonstration
fake_db = {
    'items': [{'id': 1, 'name': 'Sample item'}]
}

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(fake_db['items']), 200

@app.route('/items', methods=['POST'])
def create_item():
    item = request.json
    fake_db['items'].append(item)
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in fake_db['items'] if item['id'] == item_id), None)
    if not item:
        return Response(status=404)
    item_update = request.json
    item.update(item_update)
    return jsonify(item), 200

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((item for item in fake_db['items'] if item['id'] == item_id), None)
    if not item:
        return Response(status=404)
    fake_db['items'].remove(item)
    return Response(status=204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

import requests

app = Flask(__name__)
@app.route('/weather', methods=['GET'])
def get_weather():
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    city = request.args.get('city', default='', type=str)
    if not city:
        return jsonify({'error': 'No city provided'}), 400

    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
        return jsonify(weather_data), 200
    else:
        return jsonify({'error': 'Failed to retrieve weather data'}), response.status_code


db = firestore.Client()

app = Flask(__name__)