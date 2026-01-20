import cv2
import os
import time

face_cascade = cv2.CascadeClassifier(
    "haarcascade/haarcascade_frontalface_default.xml"
)

user_id = input("Enter numeric user ID: ")
save_path = f"dataset/{user_id}"
os.makedirs(save_path, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("📸 Capturing faces...")
print("👉 Keep your face in front of camera")

while count < 30:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        continue

    for (x, y, w, h) in faces:
        count += 1
        face = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{save_path}/{count}.jpg", face)
        print(f"✅ Image saved: {count}/30")
        time.sleep(0.3)

cap.release()
print("🎉 Dataset collection completed successfully!")


