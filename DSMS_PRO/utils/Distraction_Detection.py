import numpy as np
import time
from utils.alert_system import play_alert_sound  # Import the alert system

DISTRACTION_TIME_THRESHOLD = 2  # Time before triggering an alert
HAND_NEAR_FACE_TIME_THRESHOLD = 1  # Time before detecting phone usage
start_time = None
hand_near_face_time = None

def detect_distraction(landmarks, hand_landmarks, w, h):
    """Detects if the driver is distracted based on face orientation or phone usage."""
    global start_time, hand_near_face_time

    distraction_detected = False

    # Define face landmark indices
    nose = np.array([landmarks[1][0], landmarks[1][1]])
    left_eye = np.array([landmarks[33][0], landmarks[33][1]])
    right_eye = np.array([landmarks[263][0], landmarks[263][1]])

    # Calculate face orientation
    eye_center = (left_eye + right_eye) / 2.0
    face_vector = nose - eye_center
    angle = np.arctan2(face_vector[1], face_vector[0]) * 180 / np.pi

    # Check if looking away
    if angle < -15 or angle > 15:
        distraction_detected = True

    # Detect hand near face for phone usage detection
    if hand_landmarks:
        for hand in hand_landmarks:
            for landmark in hand.landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                if y < h // 3:  # Hand near face region
                    if hand_near_face_time is None:
                        hand_near_face_time = time.time()
                    elif time.time() - hand_near_face_time > HAND_NEAR_FACE_TIME_THRESHOLD:
                        distraction_detected = True
                        print("[ALERT] Phone usage detected!")  # Debugging message
                        break
                else:
                    hand_near_face_time = None  # Reset timer if hand moves away

    # Trigger alert if distraction is detected
    if distraction_detected:
        if start_time is None:
            start_time = time.time()
        elif time.time() - start_time >= DISTRACTION_TIME_THRESHOLD:
            play_alert_sound()
            return True  # Distraction detected
    else:
        start_time = None

    return False  # No distraction detected
