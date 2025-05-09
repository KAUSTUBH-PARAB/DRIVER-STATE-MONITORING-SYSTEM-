import cv2
import sqlite3
import time
import mediapipe as mp
import numpy as np
from utils.Drowsiness_Detection import detect_drowsiness
from utils.Distraction_Detection import detect_distraction

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("database/driver_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS driver_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT
        )
    """)
    conn.commit()
    conn.close()

# Log event into SQLite database
def log_event(event_type):
    conn = sqlite3.connect("database/driver_logs.db")
    cursor = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO driver_logs (timestamp, event_type) VALUES (?, ?)", (timestamp, event_type))
    conn.commit()
    conn.close()

# Initialize Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize Video Capture
cap = cv2.VideoCapture(0)
init_db()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract face landmarks
            landmarks = [(int(l.x * w), int(l.y * h)) for l in face_landmarks.landmark]

            # Check for drowsiness
            drowsy_detected = detect_drowsiness(landmarks)
            if drowsy_detected:
                log_event("Drowsiness Detected")

            # Check for distraction
            distracted_detected = detect_distraction(landmarks)
            if distracted_detected:
                log_event("Distraction Detected")

    # Display frame
    cv2.imshow("Real-Time Monitoring", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
