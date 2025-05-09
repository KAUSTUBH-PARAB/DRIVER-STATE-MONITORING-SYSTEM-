import numpy as np
import sqlite3
import time

# Connect to SQLite Database
def log_emotion(event_type):
    """Logs detected emotion in the database"""
    conn = sqlite3.connect("database/driver_logs.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS events (timestamp TEXT, event_type TEXT)")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO events (timestamp, event_type) VALUES (?, ?)", (timestamp, event_type))
    conn.commit()
    conn.close()

def estimate_emotion(landmarks, w, h):
    """Estimates emotion based on facial landmarks"""
    brow_left = np.array([landmarks[70][0], landmarks[70][1]])
    brow_right = np.array([landmarks[300][0], landmarks[300][1]])
    mouth_left = np.array([landmarks[61][0], landmarks[61][1]])
    mouth_right = np.array([landmarks[291][0], landmarks[291][1]])
    mouth_center = np.array([landmarks[13][0], landmarks[13][1]])

    # Distance Metrics
    brow_distance = np.linalg.norm(brow_left - brow_right) / w  # Normalize by width
    mouth_width = np.linalg.norm(mouth_left - mouth_right) / w
    mouth_openness = np.linalg.norm(mouth_center - ((mouth_left + mouth_right) / 2.0)) / h

    # Emotion Conditions (Using normalized values)
    if brow_distance < 0.1 and mouth_openness > 0.03:
        return "Stress/Anger"
    elif mouth_openness > 0.04:
        return "Fatigue/Yawning"
    else:
        return "Neutral"
