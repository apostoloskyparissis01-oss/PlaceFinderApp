from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('GOOGLE_API_KEY')

def get_coordinates(location):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': location,
            'key': API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data['results']:
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            return f'{lat},{lng}'
        
        return None

@app.route('/')
def home():
    return 'The server works'

@app.route('/places')
def get_places():
    location = request.args.get('location', 'Athens')
    radius = request.args.get('radius', 1500)
    cuisine = request.args.get('cuisine', 'restaurant')
    budget = request.args.get('budget', None)

    coordinates = get_coordinates(location)

    if not coordinates:
        return jsonify({'error': 'Location not found'}), 404

    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': coordinates,
        'radius': radius,
        'type': 'restaurant',
        'keyword': cuisine,
        'key': API_KEY

    }

    

    response = requests.get(url,params=params)
    data = response.json()

    results = data.get('results',[])
    if budget:
        results = [place for place in results
                   if place.get('price_level') == int(budget)]

    return jsonify({'results': results})



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)


