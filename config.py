import os
from pathlib import Path

# Application version
VERSION = "1.0.0"

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# File paths
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# File paths
USER_SETTINGS_FILE = os.path.join(DATA_DIR, "user_settings.json")
EMOTION_FILE = os.path.join(DATA_DIR, "emotion.txt")
HAPPY_NEWS_FILE = os.path.join(DATA_DIR, "happy_news.txt")
SCREEN_OPERATION_FILE = os.path.join(DATA_DIR, "screen_operation.txt")
CAPTURED_IMAGE_FILE = os.path.join(DATA_DIR, "captured_image.jpg")

# API Keys - For production, load these from environment variables
OPENCAGE_API_KEY = os.environ.get("OPENCAGE_API_KEY", "7edad7fb766d4888b829859f0ade0b70")

# Default values
DEFAULT_CITY = "London"
DEFAULT_COUNTRY = "UK"
DEFAULT_NEWS_SOURCE = "BBC News"

# Emotion detection settings
SAD_THRESHOLD = 40  # Threshold for "sad" emotion probability
EMOTION_DETECTION_INTERVAL = 30  # Seconds between emotion detection runs
QUESTION_TIMEOUT = 10  # Seconds to display question before hiding
HAPPY_NEWS_DISPLAY_TIME = 120  # Seconds to display happy news
NEWS_COOLDOWN_PERIOD = 600  # Seconds (10 minutes) before asking again

# Flask settings
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8000))

# Logging configuration
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_MAX_BYTES = 10485760  # 10MB
LOG_FILE_BACKUP_COUNT = 5

# Weather API settings
WEATHER_UNITS = "metric"  # Options: metric, imperial
WEATHER_REFRESH_INTERVAL = 600  # Seconds (10 minutes)
WEATHER_API_TIMEOUT = 10  # Seconds