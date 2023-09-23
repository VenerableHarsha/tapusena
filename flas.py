from flask import Flask, request
from ScrapeData import place_lst, search_field
from lat_long import json_object
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)

@app.route('/')
def hello():
    return '<p>Hello World</p>'

@app.route('/get-between/start-place/end-place', methods=['GET', 'POST'])
def get_json():
    start_place = request.args.get('start_pt')
    end_place = request.args.get('end_pt')
    search_field.send_keys(f'restaurants on {start_place} {end_place} highway')
    return json_object

if __name__ == '__main__':
    app.run()