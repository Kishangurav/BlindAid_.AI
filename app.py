import cv2
import time
print("DEBUG: Starting app...")

from detection.yolo_detector import detect_objects
from audio.text_to_speech import speak

print("DEBUG: Imports successful")

cap = cv2.VideoCapture(0)
print("DEBUG: Camera initialized")

if not cap.isOpened():
    print("❌ ERROR: Camera not opened")
    exit()

print("✅ Camera opened successfully")
print("Press Q to quit")

import time

last_spoken_time = 0
SPEAK_DELAY = 4  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame, objects = detect_objects(frame)

    # Remove duplicates
    unique_objects = list(set(objects))

    current_time = time.time()

    # Speak only once every few seconds
    if unique_objects and (current_time - last_spoken_time > SPEAK_DELAY):
        sentence = "I can see " + ", ".join(unique_objects)
        print(sentence)
        speak(sentence)
        last_spoken_time = current_time

    cv2.imshow("VisionAssist+", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("DEBUG: App closed")
