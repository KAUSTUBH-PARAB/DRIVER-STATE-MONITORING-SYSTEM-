import time
import pygame

pygame.mixer.init()
last_alert_time = 0  # Global variable to track last alert time

def play_alert_sound():
    """Plays an alert sound with a cooldown and prevents repeated playback."""
    global last_alert_time
    current_time = time.time()

    # Stop any currently playing sound
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    # Only play the alert if 5 seconds have passed
    if current_time - last_alert_time > 5:
        pygame.mixer.music.load("alert.wav")
        pygame.mixer.music.play()
        last_alert_time = current_time  # Update last played time
