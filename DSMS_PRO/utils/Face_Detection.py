import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

def detect_face(frame):
    """Detects if a face is present in the frame using MediaPipe."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    results = face_detection.process(rgb_frame)
    
    return results.detections is not None  # Return True if a face is detected
