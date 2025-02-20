# Smart Mirror Web Interface

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green)

## Overview
This project is a smart mirror web interface built using Flask. The interface displays essential information such as time, weather, mood detection, and an RSS news feed. Additionally, it includes a mood-based interaction system that detects if the user is sad and offers uplifting news via voice interaction.

## Features
- **Real-Time Updates**: Displays the current time, weather, and news feed.
- **Mood Detection**: Uses DeepFace to analyze facial expressions and determine mood.
- **Voice Interaction**: If the user is detected as sad, the system asks whether they would like to see uplifting news.
- **Happy News Display**: Fetches and displays uplifting news based on user consent.
- **Automatic Hiding**: The question disappears after 10 seconds if unanswered and does not reappear for 10 minutes.
- **Timed News Display**: Happy news is displayed for 2 minutes before being hidden.

## Project Structure
