import cv2
import time
import sqlite3
import pygame
import os
import mediapipe as mp
import numpy as np
from utils.Drowsiness_Detection import detect_drowsiness
from utils.Distraction_Detection import detect_distraction
from utils.Emotion_Recognition import estimate_emotion
from utils.Gaze_Estimation import estimate_gaze

# Suppress TensorFlow logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize Pygame for sound alerts
pygame.init()
pygame.mixer.init()

# Ensure database directory exists
os.makedirs("database", exist_ok=True)

# Initialize database
conn = sqlite3.connect("database/driver_logs.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS driver_logs (timestamp TEXT, event_type TEXT)")
conn.commit()
conn.close()

def log_event(event_type):
    """Logs events into SQLite database"""
    conn = sqlite3.connect("database/driver_logs.db")
    cursor = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO driver_logs (timestamp, event_type) VALUES (?, ?)", (timestamp, event_type))
    conn.commit()
    conn.close()

# Initialize Mediapipe Face Mesh and Hands Detection
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize Video Capture
cap = cv2.VideoCapture(0)

# Face loss tracking
face_lost_time = None
police_alert_played = False  # Ensure police sound plays only once per event

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip frame for correct orientation
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    hand_results = hands.process(rgb_frame)  # Process hands for phone usage detection

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = [(int(l.x * w), int(l.y * h)) for l in face_landmarks.landmark]

            # Run detection modules only if valid landmarks exist
            if len(landmarks) > 0:
                drowsy_detected = detect_drowsiness(landmarks)
                print(f"[DEBUG] Drowsiness detected: {drowsy_detected}")
                if drowsy_detected:
                    log_event("Drowsiness Detected")
                    cv2.putText(frame, "DROWSINESS ALERT!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

                distracted_detected = detect_distraction(landmarks, hand_results.multi_hand_landmarks, w, h)
                print(f"[DEBUG] Distraction detected: {distracted_detected}")
                if distracted_detected:
                    log_event("Distraction Detected")
                    cv2.putText(frame, "DISTRACTION ALERT!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

                emotion = estimate_emotion(landmarks, w, h)
                print(f"[DEBUG] Emotion detected: {emotion}")
                if emotion != "Neutral":
                    log_event(f"Emotion: {emotion}")
                    cv2.putText(frame, f"Emotion: {emotion}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

                gaze_direction = estimate_gaze(landmarks, w, h)
                print(f"[DEBUG] Gaze direction: {gaze_direction}")
                if gaze_direction in ["Looking Left", "Looking Right"]:
                    log_event(f"Gaze: {gaze_direction}")
                    cv2.putText(frame, f"Gaze: {gaze_direction}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Reset face loss timer if face is detected again
            face_lost_time = None  
            police_alert_played = False  
            
    else:
        # If face is lost, start the timer
        if face_lost_time is None:
            face_lost_time = time.time()
        elif time.time() - face_lost_time > 10 and not police_alert_played:
            pygame.mixer.music.load("police.ogg")
            pygame.mixer.music.play()
            police_alert_played = True

    # Display real-time feed
    cv2.imshow("Driver State Monitoring System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
