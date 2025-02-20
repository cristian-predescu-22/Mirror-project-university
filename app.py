from flask import Flask, render_template, request, jsonify, send_from_directory, Response
import requests
import json
import os
import time
import emotion_detection


opencage_api_key = "7edad7fb766d4888b829859f0ade0b70"


app = Flask(__name__)


# After initializing the Flask app



@app.route('/')
def index():
    return render_template('index.html')


# New /setup route to accept data and store it in a .txt file
@app.route("/setup", methods=["POST"])
def setup():

    # Get JSON data from the incoming request
    data = request.get_json()

    if data is not None:
        existing_data = {}

        if os.path.exists("data.txt"):
            with open("data.txt", "r") as data_file:
                # Load the JSON data from the file into the existing_data dictionary
                existing_data = json.load(data_file)

        for key, value in data.items():
            # If the value is not empty (or not None), add/update the key-value pair in the existing_data dictionary
            if value:
                existing_data[key] = value

        with open("data.txt", "w") as data_file:
            json.dump(existing_data, data_file)

        return jsonify({'result': 'success'})
    # If data is missing, return an error
    else:
        return jsonify({"status": "error", "message": "Data is missing"}), 400


# Add a new route to serve the data.txt file
@app.route('/data', methods=['GET'])
def get_data():
    return send_from_directory('.', 'data.txt')


@app.route('/weather', methods=['GET'])
def get_weather():
    with open("data.txt", "r") as data_file:
        data = json.load(data_file)

    city = data.get("city")
    country = data.get("country")
    open_weather_api_key = data.get("openWeatherApiKey")

    if not city or not country or not open_weather_api_key:
        return jsonify({"status": "error", "message": "Required data is missing"}), 400

    # Fetch latitude and longitude from OpenCage Geocoder API
    geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={city},+{country}&key={opencage_api_key}"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()

    if geocode_data.get("results"):
        latitude = geocode_data["results"][0]["geometry"]["lat"]
        longitude = geocode_data["results"][0]["geometry"]["lng"]

        # Fetch weather data from OpenWeather One Call API 3.0
        weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&exclude=minutely,hourly,daily,alerts&appid={open_weather_api_key}"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        return jsonify(weather_data)

    return jsonify({"status": "error", "message": "Location not found"}), 400


@app.route('/events')
def events():
    def watch_for_changes():
        current_mtime = None
        current_location = None
        current_news_source = None
        while True:
            try:
                mtime = os.path.getmtime("data.txt")
                if current_mtime != mtime:
                    current_mtime = mtime
                    with open("data.txt", "r") as data_file:
                        data = json.load(data_file)

                    location = (data.get("city", ""), data.get("country", ""))
                    news_source = data.get("newsSource", "")

                    if current_location != location or current_news_source != news_source:
                        current_location = location
                        current_news_source = news_source
                        yield "data: update\n\n"

            except FileNotFoundError:
                pass
            time.sleep(1)

    return Response(watch_for_changes(), content_type='text/event-stream')


@app.route('/emotion')
def emotion():
    emotion_detection.capture_and_predict_emotion()  # Call the new function
    with open("emotion.txt", "r") as f:
        detected_emotion = f.read()
    return jsonify(emotion=detected_emotion)



import re

@app.route('/happy_news')
def happy_news():
    with open("happy_news.txt", "r", encoding="utf-8") as file:
        data = file.read()

    title = re.search("Title: (.*)", data).group(1)
    description = re.search("Description: (.*)", data).group(1)
    date = re.search("Date: (.*)", data).group(1)

    return jsonify(title=title, description=description, date=date)




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
