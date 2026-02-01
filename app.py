from train_ui import train_model_ui
from capture_faces import capture_faces_ui
from student_ui import student_registration_ui
from report_ui import attendance_report_ui
from login_ui import login_ui
from firebase_config import db

import cv2
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import os

# -------- LOGIN CHECK --------
if "user" not in st.session_state:
    login_ui()
    st.stop()

# ---------------- THEME CSS ----------------
def load_css(theme):
    css_file = "styles/dark.css" if theme == "Dark" else "styles/light.css"
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- CONFIG ----------------
FACE_SIZE = (200, 200)
CONF_THRESHOLD = 90
MIN_CONFIDENCE_PERCENT = 35

id_name = {
    1: "Supriya",
    2: "Pushkar",
    3: "Bhavyaan",
    4: "Jatin",
    5: "Raghav",
    6: "Pratham",
    7: "Shiva"
}

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

face_cascade = cv2.CascadeClassifier(
    "haarcascade/haarcascade_frontalface_default.xml"
)

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="FaceApp", layout="wide")
st.title("FaceApp - Smart Attendance System")

theme = st.sidebar.selectbox("Select Theme", ["Light", "Dark"])
load_css(theme)

page = st.sidebar.radio(
    "Navigate",
    [
        "Attendance",
        "Student Registration",
        "Capture Faces",
        "Train Model",
        "Attendance Report"
    ]
)

# ================= ATTENDANCE PAGE =================
if page == "Attendance":
    col1, col2 = st.columns(2)
    start = col1.button("Start Camera")
    stop = col2.button("Stop Camera")

    FRAME_WINDOW = st.image([])

    today = datetime.now().strftime("%Y-%m-%d")
    marked_names = set()

    cap = cv2.VideoCapture(0)
    run = start and not stop

    if run:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, FACE_SIZE)

                id_, conf = recognizer.predict(face)
                confidence_percent = max(0, int(100 - conf))

                if conf < CONF_THRESHOLD and confidence_percent >= MIN_CONFIDENCE_PERCENT:
                    name = id_name.get(id_, "Unknown")

                    if name not in marked_names:
                        time_now = datetime.now().strftime("%H:%M:%S")

                        # ✅ SAVE TO FIREBASE DB
                        db.child("attendance").push({
                            "name": name,
                            "time": time_now,
                            "confidence": confidence_percent,
                            "date": today
                        })

                        marked_names.add(name)

                    label = f"{name} ({confidence_percent}%)"
                    color = (0, 255, 0)
                else:
                    label = "Unknown"
                    color = (0, 0, 255)

                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(rgb_frame)
    else:
        cap.release()

# ================= OTHER PAGES =================
elif page == "Student Registration":
    student_registration_ui()

elif page == "Capture Faces":
    capture_faces_ui()

elif page == "Train Model":
    train_model_ui()

elif page == "Attendance Report":
    attendance_report_ui()
