Smart Mirror Web Interface

Overview

This project is a smart mirror web interface built using Flask. The interface displays essential information such as time, weather, mood detection, and an RSS news feed. Additionally, it includes a mood-based interaction system that detects if the user is sad and offers uplifting news via voice interaction.

Features

Real-Time Updates: Displays the current time, weather, and news feed.

Mood Detection: Uses DeepFace to analyze facial expressions and determine mood.

Voice Interaction: If the user is detected as sad, the system asks whether they would like to see uplifting news.

Happy News Display: Fetches and displays uplifting news based on user consent.

Automatic Hiding: The question disappears after 10 seconds if unanswered and does not reappear for 10 minutes.

Timed News Display: Happy news is displayed for 2 minutes before being hidden.

Project Structure

ScrachNew - Copy (3) - Copy
├── app.py
├── captured_image.jpg
├── data.txt
├── emotion.txt
├── emotion_detection.py
├── screen_operation.txt
├── static
│   ├── css
│   │   └── styles.css
│   ├── images
│   │   ├── cloud.png
│   │   ├── rain.png
│   │   ├── snow.png
│   │   └── sun.png
│   └── js
│       └── scripts.js
├── templates
│   ├── base.html
│   └── index.html
├── happy_news.txt

Installation

Prerequisites

Python 3.11+

Flask

DeepFace

Steps

Clone the repository:

git clone <repository_url>
cd smart-mirror-web-interface

Install dependencies:

pip install flask deepface

Run the Flask application:

python app.py

Open the interface in a web browser:

http://127.0.0.1:8000/

Usage

The smart mirror continuously monitors the user's mood every 60 seconds.

If sadness is detected, it prompts the user with the question: "Would you like to see some uplifting news?"

If the user responds with any variation of "yes," happy news is fetched and displayed.

If no response is detected within 10 seconds, the question disappears.

The happy news is hidden after 2 minutes of display.

Configuration

Modify happy_news.txt to include uplifting news articles. The format should follow:

Title: Your Happy News Title
Description: Brief description of the news
Date: Day, DD Month YYYY HH:MM:SS +0000

Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
