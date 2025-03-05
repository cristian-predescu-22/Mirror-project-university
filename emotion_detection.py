import cv2
import os
import logging
from deepface import DeepFace
from pathlib import Path

# Configuration
SCREEN_OPERATION_FILE = "screen_operation.txt"
EMOTION_FILE = "emotion.txt"
CAPTURED_IMAGE_FILE = "captured_image.jpg"
SAD_THRESHOLD = 40  # Threshold for "sad" emotion probability

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Add handler to the logger
handler = logging.FileHandler('logs/emotion_detection.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def capture_image():
    """
    Capture an image from the webcam.
    
    Returns:
        numpy.ndarray: The captured image frame, or None if capture failed
    """
    try:
        cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            logger.error("Error: Could not open webcam")
            return None
        
        # Wait for camera to initialize
        cv2.waitKey(1000)
        
        # Capture frame
        ret, frame = cap.read()
        
        # Release the camera
        cap.release()
        
        if not ret:
            logger.error("Failed to capture image from webcam")
            return None
            
        logger.info("Image captured successfully")
        return frame
        
    except Exception as e:
        logger.error(f"Error capturing image: {str(e)}")
        return None

def analyze_emotion(img_path):
    """
    Analyze the emotion in an image using DeepFace.
    
    Args:
        img_path (str): Path to the image file
        
    Returns:
        str: The dominant emotion detected
    """
    try:
        # Analyze only the emotion
        face_analysis_list = DeepFace.analyze(img_path=img_path, actions=['emotion'])
        
        # If no faces detected or empty result
        if not face_analysis_list:
            logger.warning("No faces detected in the image")
            return "neutral"
            
        # Select the first face analysis
        face_analysis = face_analysis_list[0]
        
        # Extract the dominant emotion and probabilities
        dominant_emotion = face_analysis['dominant_emotion']
        emotion_probabilities = face_analysis['emotion']
        
        logger.info(f"Emotion analysis complete: {dominant_emotion} ({emotion_probabilities[dominant_emotion]:.2f}%)")
        logger.debug(f"All emotion probabilities: {emotion_probabilities}")
        
        # Apply threshold for the "sad" emotion
        if dominant_emotion == 'sad' and emotion_probabilities['sad'] < SAD_THRESHOLD:
            logger.info(f"Sad emotion below threshold ({emotion_probabilities['sad']} < {SAD_THRESHOLD}), changing to neutral")
            return 'neutral'
            
        return dominant_emotion
        
    except Exception as e:
        logger.error(f"Error analyzing emotion: {str(e)}")
        return "error"

def is_screen_on():
    """
    Check if the screen operation is set to 'on'.
    
    Returns:
        bool: True if screen is on, False otherwise
    """
    try:
        # Ensure the file exists
        Path(SCREEN_OPERATION_FILE).touch(exist_ok=True)
        
        with open(SCREEN_OPERATION_FILE, "r") as f:
            screen_operation = f.read().strip().lower()
            
        return screen_operation == "on"
        
    except Exception as e:
        logger.error(f"Error checking screen operation: {str(e)}")
        return False

def save_emotion(emotion):
    """
    Save the detected emotion to the emotion file.
    
    Args:
        emotion (str): The emotion to save
    """
    try:
        with open(EMOTION_FILE, "w") as f:
            f.write(emotion)
        logger.info(f"Emotion saved: {emotion}")
    except Exception as e:
        logger.error(f"Error saving emotion: {str(e)}")

def capture_and_predict_emotion():
    """
    Capture an image from the webcam and predict the emotion.
    """
    try:
        # Check if screen is on
        if not is_screen_on():
            logger.info("Screen operation is off, skipping emotion detection")
            save_emotion("Screen operation is off")
            return
            
        # Capture image
        captured_image = capture_image()
        
        if captured_image is None:
            logger.error("Failed to capture image")
            save_emotion("error")
            return
            
        # Save the captured image
        cv2.imwrite(CAPTURED_IMAGE_FILE, captured_image)
        logger.info(f"Image saved to {CAPTURED_IMAGE_FILE}")
        
        # Analyze emotion
        dominant_emotion = analyze_emotion(CAPTURED_IMAGE_FILE)
        
        # Save the detected emotion
        save_emotion(dominant_emotion)
        
    except Exception as e:
        logger.error(f"Unexpected error in emotion detection: {str(e)}")
        save_emotion("error")

if __name__ == "__main__":
    capture_and_predict_emotion()