import numpy as np
import time
from utils.alert_system import play_alert_sound  # Import the fixed alert function

# Function to calculate Eye Aspect Ratio (EAR)
def calculate_ear(landmarks, eye_indices):
    A = np.linalg.norm(np.array(landmarks[eye_indices[1]]) - np.array(landmarks[eye_indices[5]]))
    B = np.linalg.norm(np.array(landmarks[eye_indices[2]]) - np.array(landmarks[eye_indices[4]]))
    C = np.linalg.norm(np.array(landmarks[eye_indices[0]]) - np.array(landmarks[eye_indices[3]]))
    return (A + B) / (2.0 * C)

# Function to calculate Mouth Aspect Ratio (MAR)
def calculate_mar(landmarks, mouth_indices):
    A = np.linalg.norm(np.array(landmarks[mouth_indices[1]]) - np.array(landmarks[mouth_indices[7]]))
    B = np.linalg.norm(np.array(landmarks[mouth_indices[2]]) - np.array(landmarks[mouth_indices[6]]))
    C = np.linalg.norm(np.array(landmarks[mouth_indices[3]]) - np.array(landmarks[mouth_indices[5]]))
    D = np.linalg.norm(np.array(landmarks[mouth_indices[0]]) - np.array(landmarks[mouth_indices[4]]))
    return (A + B + C) / (2.0 * D)

# Define Constants
EYE_AR_THRESH = 0.2  # Eye Aspect Ratio Threshold
MOUTH_AR_THRESH = 0.6  # Mouth Aspect Ratio Threshold
DROWSINESS_TIME_THRESHOLD = 2  # Time duration for drowsiness alert

start_time = None

def detect_drowsiness(landmarks):
    """Detects drowsiness based on eye and mouth aspect ratios."""
    global start_time

    # Define eye and mouth landmark indices
    left_eye = [33, 160, 158, 133, 153, 144]
    right_eye = [263, 387, 385, 362, 380, 373]
    mouth = [61, 40, 37, 0, 267, 270, 291, 321]

    ear_left = calculate_ear(landmarks, left_eye)
    ear_right = calculate_ear(landmarks, right_eye)
    mar = calculate_mar(landmarks, mouth)
    ear_avg = (ear_left + ear_right) / 2.0

    print(f"[DEBUG] EAR: {ear_avg:.3f}, MAR: {mar:.3f}")  # Debugging EAR & MAR values

    # Detect drowsiness (eye blink or yawning)
    if ear_avg < EYE_AR_THRESH or mar > MOUTH_AR_THRESH:
        if start_time is None:
            start_time = time.time()
        elif time.time() - start_time >= DROWSINESS_TIME_THRESHOLD:
            print("[ALERT] Drowsiness detected! Playing sound...")
            play_alert_sound()  # Plays alert sound if it is not already playing
            return True  # Drowsiness detected
    else:
        start_time = None  # Reset timer if no drowsiness detected
    
    return False  # No drowsiness detected
