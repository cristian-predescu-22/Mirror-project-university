from flask import Flask, render_template, request, jsonify, send_from_directory, Response
import os
import time
import logging
from logging.handlers import RotatingFileHandler

# Import project modules
import config
import emotion_detection
from utils.weather import WeatherService
from utils.news import NewsService

# Initialize services
weather_service = WeatherService(config.OPENCAGE_API_KEY, config.WEATHER_API_TIMEOUT)
news_service = NewsService(config.HAPPY_NEWS_FILE)

# Initialize Flask application
app = Flask(__name__)

# Setup logging
def setup_logging():
    if not os.path.exists(config.LOGS_DIR):
        os.makedirs(config.LOGS_DIR)
    
    file_handler = RotatingFileHandler(
        os.path.join(config.LOGS_DIR, 'smart_mirror.log'),
        maxBytes=config.LOG_FILE_MAX_BYTES,
        backupCount=config.LOG_FILE_BACKUP_COUNT
    )
    file_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
    file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, config.LOG_LEVEL))
    app.logger.info(f'Smart Mirror v{config.VERSION} startup')

# Ensure all required files exist
def ensure_files_exist():
    # Create data directory if it doesn't exist
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    # Touch files to ensure they exist
    if not os.path.exists(config.USER_SETTINGS_FILE):
        with open(config.USER_SETTINGS_FILE, "w") as f:
            f.write("{}")
    
    if not os.path.exists(config.EMOTION_FILE):
        with open(config.EMOTION_FILE, "w") as f:
            f.write("neutral")
    
    if not os.path.exists(config.SCREEN_OPERATION_FILE):
        with open(config.SCREEN_OPERATION_FILE, "w") as f:
            f.write("on")

# Helper function to load user settings
def load_user_settings():
    try:
        import json
        with open(config.USER_SETTINGS_FILE, "r") as data_file:
            return json.load(data_file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        app.logger.error(f"Error loading user settings: {e}")
        return {}

# Helper function to save user settings
def save_user_settings(data_dict):
    try:
        import json
        with open(config.USER_SETTINGS_FILE, "w") as data_file:
            json.dump(data_dict, data_file)
        return True
    except Exception as e:
        app.logger.error(f"Error saving user settings: {e}")
        return False

# Routes
@app.route('/')
def index():
    """Render the main application page."""
    app.logger.info('Main page accessed')
    return render_template('index.html')

@app.route("/setup", methods=["POST"])
def setup():
    """Handle setup data and store it in the user settings file."""
    data = request.get_json()
    
    if not data:
        app.logger.warning("Setup called with missing data")
        return jsonify({"status": "error", "message": "Data is missing"}), 400
    
    existing_data = load_user_settings()
    
    # Update only non-empty values
    for key, value in data.items():
        if value:
            existing_data[key] = value
    
    if save_user_settings(existing_data):
        app.logger.info(f"Settings updated: {', '.join(data.keys())}")
        return jsonify({'status': 'success'})
    else:
        return jsonify({"status": "error", "message": "Failed to save data"}), 500

@app.route('/data', methods=['GET'])
def get_data():
    """Serve the user settings file."""
    app.logger.info('User settings requested')
    return send_from_directory(config.DATA_DIR, os.path.basename(config.USER_SETTINGS_FILE))

@app.route('/weather', methods=['GET'])
def get_weather():
    """Fetch and return weather data based on location settings."""
    user_settings = load_user_settings()
    
    city = user_settings.get("city", config.DEFAULT_CITY)
    country = user_settings.get("country", config.DEFAULT_COUNTRY)
    open_weather_api_key = user_settings.get("openWeatherApiKey")
    
    if not open_weather_api_key:
        app.logger.warning("Weather request missing API key")
        return jsonify({"status": "error", "message": "OpenWeather API key is missing"}), 400
    
    try:
        # Get weather data from the service
        weather_data = weather_service.get_weather_for_location(
            city, 
            country, 
            open_weather_api_key,
            config.WEATHER_UNITS
        )
        
        return jsonify(weather_data)
    
    except Exception as e:
        app.logger.error(f"Unexpected error in weather request: {str(e)}")
        return jsonify({"status": "error", "message": "An unexpected error occurred"}), 500

@app.route('/events')
def events():
    """Server-sent events endpoint to notify about data changes."""
    def watch_for_changes():
        current_mtime = None
        current_location = None
        current_news_source = None
        
        while True:
            try:
                mtime = os.path.getmtime(config.USER_SETTINGS_FILE)
                
                if current_mtime != mtime:
                    current_mtime = mtime
                    user_settings = load_user_settings()
                    
                    location = (user_settings.get("city", ""), user_settings.get("country", ""))
                    news_source = user_settings.get("newsSource", "")
                    
                    if current_location != location or current_news_source != news_source:
                        current_location = location
                        current_news_source = news_source
                        app.logger.info("Data change detected, notifying clients")
                        yield "data: update\n\n"
            
            except FileNotFoundError:
                app.logger.warning(f"File not found: {config.USER_SETTINGS_FILE}")
                yield "data: error\n\n"
            except Exception as e:
                app.logger.error(f"Error in SSE: {str(e)}")
                yield "data: error\n\n"
                
            time.sleep(1)
    
    return Response(watch_for_changes(), content_type='text/event-stream')

@app.route('/emotion')
def emotion():
    """Get the current detected emotion."""
    try:
        emotion_detection.capture_and_predict_emotion()
        
        with open(config.EMOTION_FILE, "r") as f:
            detected_emotion = f.read().strip()
        
        app.logger.info(f"Emotion detected: {detected_emotion}")
        return jsonify(emotion=detected_emotion)
    except Exception as e:
        app.logger.error(f"Error detecting emotion: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/happy_news')
def happy_news():
    """Get happy news to display when the user is sad."""
    try:
        # Get a random happy news entry
        news_entry = news_service.get_random_happy_news()
        
        if not news_entry:
            app.logger.warning("No happy news available")
            return jsonify({"status": "error", "message": "No happy news available"}), 404
        
        app.logger.info("Happy news retrieved")
        return jsonify(news_entry)
    except Exception as e:
        app.logger.error(f"Error retrieving happy news: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "version": config.VERSION,
        "timestamp": time.time()
    })

# Application initialization
if __name__ == '__main__':
    setup_logging()
    ensure_files_exist()
    app.logger.info('Starting Smart Mirror application')
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)