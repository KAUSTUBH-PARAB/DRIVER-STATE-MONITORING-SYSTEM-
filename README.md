# 🛡️ Driver State Monitoring System (DSMS)

An real-time monitoring solution that detects driver drowsiness, distraction, gaze deviation, and emotional states using computer vision. This system aims to reduce road accidents by providing timely alerts and logging incidents locally.

---

## 📌 Features

- 😴 Drowsiness Detection using Eye Aspect Ratio (EAR)
- 👀 Gaze Estimation for attention tracking
- 😡 Emotion Recognition from facial expressions
- 🚫 Distraction Detection using face orientation
- 🔊 Real-time audio alerts (customizable)
- 🧠 Modular and extendable architecture
- 💾 Logs alerts to local SQLite database

---

## 📁 Project Structure

```

DSMS\_PRO/
├── main.py                         # Entry point for real-time monitoring
├── requirements.txt                # Dependencies
├── alert.wav / police.ogg          # Alert sounds
├── monitoring\_log.db               # SQLite logging database
│
├── database/
│   ├── driver\_logs.db              # Additional log database
│   └── Monitoring.py               # DB interface logic
│
├── utils/
│   ├── alert\_system.py             # Plays alert sounds
│   ├── Drowsiness\_Detection.py     # Detects eye closure
│   ├── Emotion\_Recognition.py      # Detects emotions
│   ├── Gaze\_Estimation.py          # Detects gaze direction
│   ├── Face\_Detection.py           # Face detection logic
│   ├── Distraction\_Detection.py    # Checks for driver distraction

````

---

## ⚙️ Setup Instructions

### 1. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

```bash
python main.py
```

The webcam will activate, and real-time driver monitoring will begin. Alerts will be played if any abnormal driver behavior is detected.

---

## 💡 Tech Stack

* **Python 3.x**
* **OpenCV** – Video stream and image processing
* **Dlib / Mediapipe** – Facial landmarks
* **TensorFlow/Keras** – (if using deep models)
* **SQLite** – Data logging
* **Pygame / Playsound** – Audio alerts

---

## 📋 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgments

Inspired by advancements in driver monitoring systems and road safety technologies.

---
