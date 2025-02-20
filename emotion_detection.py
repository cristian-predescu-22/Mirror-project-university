import cv2
from deepface import DeepFace

def capture_image():
    cap = cv2.VideoCapture(0)
    cv2.waitKey(1000)  # Wait for 1000 ms (1 second) to let the camera start

    ret, frame = cap.read()

    cap.release()
    return frame

def capture_and_predict_emotion():
    with open("screen_operation.txt", "r") as f:
        screen_operation = f.read().strip()

    if screen_operation == "on":
        # Capture the image using webcam
        captured_image = capture_image()

        # Save the captured image
        cv2.imwrite('captured_image.jpg', captured_image)

        img_path = "captured_image.jpg"

        # Analyze only the emotion
        face_analysis_list = DeepFace.analyze(img_path=img_path, actions=['emotion'])

        # Select the first dictionary in the list
        face_analysis = face_analysis_list[0]
        # Extract the dominant emotion
        dominant_emotion = face_analysis['dominant_emotion']
        # Extract the emotion probabilities
        emotion_probabilities = face_analysis['emotion']
        print(emotion_probabilities)
        # Define a threshold for the "Sad" emotion
        sad_threshold = 40

        # Check if the "Sad" emotion probability is below the threshold
        if dominant_emotion == 'sad' and emotion_probabilities['sad'] < sad_threshold:
            # Replace "Sad" with "Neutral" if the probability is below the threshold
            dominant_emotion = 'neutral'

        # Save the dominant emotion to the "emotion.txt" file
        with open("emotion.txt", "w") as f:
            f.write(dominant_emotion)
    else:
        with open("emotion.txt", "w") as f:
            f.write("Screen operation is off")


if __name__ == "__main__":
    capture_and_predict_emotion()
