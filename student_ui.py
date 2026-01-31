import cv2
import os
import streamlit as st
from datetime import datetime
import numpy as np
import subprocess

DATASET_DIR = "dataset"
FACE_COUNT = 30
FACE_SIZE = (200, 200)

face_cascade = cv2.CascadeClassifier(
    "haarcascade/haarcascade_frontalface_default.xml"
)

def get_next_id():
    if not os.path.exists(DATASET_DIR):
        return 1
    ids = [int(d) for d in os.listdir(DATASET_DIR) if d.isdigit()]
    return max(ids) + 1 if ids else 1

def student_registration_ui():
    st.subheader("👤 Student Registration")

    name = st.text_input("Enter Student Name")
    if not name:
        return

    student_id = get_next_id()
    st.info(f"Assigned Student ID: {student_id}")

    capture = st.button("📸 Capture Face Images")

    if capture:
        save_path = f"{DATASET_DIR}/{student_id}"
        os.makedirs(save_path, exist_ok=True)

        cap = cv2.VideoCapture(0)
        count = 0
        FRAME = st.image([])

        while count < FACE_COUNT:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, FACE_SIZE)

                count += 1
                cv2.imwrite(f"{save_path}/{count}.jpg", face)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, f"{count}/{FACE_COUNT}",
                            (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            FRAME.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        cap.release()
        st.success("✅ Face capture completed")

    if st.button("🧠 Train Model"):
        subprocess.run(["python", "train.py"])
        st.success("🎉 Model trained successfully")
