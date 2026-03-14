from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('GOOGLE_API_KEY')

@app.route('/')
def home():
    return 'The server works'

@app.route('/places')
def get_places():
    location = request.args.get('location', '37.9838,23.7275')
    radius = request.args.get('radius', 1500)
    cuisine = request.args.get('cuisine', 'restaurant')
    budget = request.args.get('budget', None)

    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': location,
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


