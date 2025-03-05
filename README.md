# Smart Mirror Web Interface

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview
A professional-grade smart mirror web interface built with Flask that displays essential information such as time, weather, and news. The system includes a mood detection feature using DeepFace to analyze facial expressions and offer mood-based interactions.

## Features
- **Real-Time Updates**: Displays the current time, weather, and news feed
- **Mood Detection**: Analyzes facial expressions to determine the user's mood
- **Voice Interaction**: Offers uplifting news to users when they appear sad
- **Responsive Design**: Adapts to different screen sizes
- **Configuration Management**: Centralized settings for easy customization
- **Logging System**: Comprehensive logging for troubleshooting and monitoring
- **Error Handling**: Robust error recovery mechanisms

## Project Structure

```
smart-mirror/
│
├── app.py                # Main Flask application 
├── emotion_detection.py  # Facial emotion detection module
├── config.py             # Centralized configuration management
├── requirements.txt      # Project dependencies
│
├── data/                 # Data storage
│   ├── user_settings.json
│   ├── emotion.txt
│   ├── screen_operation.txt
│   └── happy_news.txt
│
├── logs/                 # Application logs
│   ├── smart_mirror.log
│   └── emotion_detection.log
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── images/
│   │   ├── cloud.png
│   │   ├── rain.png
│   │   ├── snow.png
│   │   └── sun.png
│   └── js/
│       └── scripts.js
│
├── templates/
│   ├── base.html
│   └── index.html
│
├── utils/                # Helper utilities
│   ├── __init__.py
│   ├── weather.py        # Weather API integration
│   └── news.py           # News processing functionality
│
└── README.md
```

## Installation

### Prerequisites
- Python 3.11 or higher
- Webcam (for emotion detection)
- Internet connection (for weather and news updates)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart-mirror.git
   cd smart-mirror
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your API keys:
   - Open `config.py` and update API keys or set them as environment variables
   - Get OpenWeather API key from: https://openweathermap.org/api

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the web interface:
   - Open your browser and navigate to: `http://localhost:8000`

## Configuration

The application can be configured through the `config.py` file or by setting environment variables. Key configurations include:

- `OPENCAGE_API_KEY`: API key for geocoding services
- `DEFAULT_CITY`, `DEFAULT_COUNTRY`: Default location for weather
- `EMOTION_DETECTION_INTERVAL`: Time between emotion detection runs (seconds)
- `DEBUG`: Enable/disable debug mode
- `PORT`: Server port number

## Usage

1. **Initial Setup**:
   - On first launch, the system will prompt for your location and API keys
   - Configure your news source preference

2. **Emotion Detection**:
   - Position yourself in front of the webcam
   - The system will periodically analyze your facial expressions
   - If sadness is detected, uplifting news will be offered

3. **Weather Updates**:
   - Current weather conditions are displayed on the main screen
   - Weather refreshes automatically at configured intervals

## Development

### Adding New Features

To add new features to the Smart Mirror:

1. Create a new module in the appropriate directory
2. Update `app.py` to include the new functionality
3. Add any new routes or services as needed
4. Update templates or static files as required

### Running Tests

Run the test suite with:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- DeepFace for emotion detection capabilities
- OpenWeather for weather data API
- OpenCage for geocoding services