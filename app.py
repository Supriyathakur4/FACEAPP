import cv2
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Load face detector
face_cascade = cv2.CascadeClassifier(
    "haarcascade/haarcascade_frontalface_default.xml"
)

# ID → Name mapping
id_name = {
    1: "Supriya",
    2: "Pushkar",
    3: "Bhavyaan",
    4: "Alisha",
    5: "Raghav",
    6: "Pratham",
    7: "Jatin"
}

st.title("🎓 Face Recognition Attendance System")

run = st.checkbox("Start Camera")
FRAME_WINDOW = st.image([])

attendance_file = "attendance.csv"

# Initialize webcam
cap = cv2.VideoCapture(0)

if run:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            id_, conf = recognizer.predict(face)

            if conf < 70:
                name = id_name.get(id_, "Unknown")
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                df = pd.DataFrame([[name, now]], columns=["Name", "Time"])
                df.to_csv(attendance_file, mode='a', header=False, index=False)

                cv2.putText(frame, name, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

else:
    cap.release()
