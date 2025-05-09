import numpy as np
import sqlite3
import time

# Connect to SQLite Database
def log_gaze(event_type):
    """Logs detected gaze direction in the database"""
    conn = sqlite3.connect("database/driver_logs.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS events (timestamp TEXT, event_type TEXT)")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO events (timestamp, event_type) VALUES (?, ?)", (timestamp, event_type))
    conn.commit()
    conn.close()

def estimate_gaze(landmarks, w, h):
    """Estimates gaze direction based on eye position"""
    left_eye_indices = [33, 160, 158, 133, 153, 144]  # Left eye
    right_eye_indices = [263, 387, 385, 362, 380, 373]  # Right eye

    left_eye = np.array([landmarks[i] for i in left_eye_indices])
    right_eye = np.array([landmarks[i] for i in right_eye_indices])

    # Get center points of both eyes
    left_eye_center = np.mean(left_eye, axis=0)
    right_eye_center = np.mean(right_eye, axis=0)

    # Gaze estimation based on the relative position of the eye centers
    gaze_point_x = (left_eye_center[0] + right_eye_center[0]) / 2

    if gaze_point_x < w * 0.35:
        return "Looking Left"
    elif gaze_point_x > w * 0.65:
        return "Looking Right"
    else:
        return "Looking Forward"
