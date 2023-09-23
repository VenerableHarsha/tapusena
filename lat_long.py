# Import the required library
import socket
import json
from flask import Flask, request
import os

import geopy.exc
import requests.exceptions
import urllib3.exceptions
from geopy.geocoders import Nominatim
from ScrapeData import retrieve_data

app = Flask(__name__)

# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")
latlong_dict = {}


# print(latlong_dict)
# print("The latitude of the location is: ", location.latitude)
# print("The longitude of the location is: ", location.longitude)

@app.route('/')
def home():
    return "<p>Hello, World!</p>"

@app.route('/get-between/<start_place>/<end_place>', methods=['GET', 'POST'])
def get_json(start_place, end_place):
    # start_pt = request.args.get('start_place')
    # end_pt = request.args.get('end_place')
    for i in retrieve_data(start_place, end_place):
        try:
            location = geolocator.geocode(i)
            if location is not None:
                latlong_dict[i] = [location.latitude, location.longitude]
        except geopy.exc.GeocoderUnavailable or requests.exceptions.ConnectTimeout or urllib3.exceptions.MaxRetryError or urllib3.exceptions.ConnectTimeoutError or socket.timeout \
               or AttributeError:
            pass
    json_object = json.dumps(latlong_dict, indent=4)
    return json_object

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
