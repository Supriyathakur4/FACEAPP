from train_ui import train_model_ui
from capture_faces import capture_faces_ui
from student_ui import student_registration_ui
from report_ui import attendance_report_ui
from login_ui import login_ui
from firebase_config import db

import cv2
import streamlit as st
from datetime import datetime
from PIL import Image
import numpy as np


# -------- LOGIN CHECK --------
if "user" not in st.session_state:
    login_ui()
    st.stop()

st.set_page_config(page_title="FaceApp", layout="wide")


# -------- LOAD CSS --------
def load_css(theme):
    css_file = "styles/dark.css" if theme == "Dark" else "styles/light.css"
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# -------- SIDEBAR --------
with st.sidebar:
    st.title("Menu")

    theme = st.selectbox("Select Theme", ["Light", "Dark"])
    load_css(theme)

    page = st.radio(
        "Navigate",
        [
            "Attendance",
            "Student Registration",
            "Capture Faces",
            "Train Model",
            "Attendance Report"
        ]
    )

    st.markdown("---")
    if st.button("Logout"):
        del st.session_state["user"]
        st.rerun()


# -------- HEADER --------
st.markdown(
    '<div class="card"><h2 style="text-align:center;">FaceApp - Smart Attendance System</h2></div>',
    unsafe_allow_html=True
)


# -------- CONFIG --------
FACE_SIZE = (200, 200)
CONF_THRESHOLD = 90
MIN_CONFIDENCE_PERCENT = 35
id_name = {1: "Supriya"}

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

face_cascade = cv2.CascadeClassifier(
    "haarcascade/haarcascade_frontalface_default.xml"
)


# ================= ATTENDANCE =================
import numpy as np
from PIL import Image

if page == "Attendance":
    st.subheader("Mark Attendance")

    img_file = st.camera_input("Take a photo")

    if img_file is not None:
        image = Image.open(img_file)
        frame = np.array(image)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, FACE_SIZE)

            id_, conf = recognizer.predict(face)
            confidence_percent = max(0, int(100 - conf))

            if conf < CONF_THRESHOLD and confidence_percent >= MIN_CONFIDENCE_PERCENT:
                name = id_name.get(id_, "Unknown")

                time_now = datetime.now().strftime("%H:%M:%S")
                today = datetime.now().strftime("%Y-%m-%d")

                db.child("attendance").push({
                    "name": name,
                    "time": time_now,
                    "confidence": confidence_percent,
                    "date": today
                })

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, name, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                st.success(f"Attendance marked for {name}")
            else:
                st.error("Face not recognized")

        st.image(frame)



# ================= OTHER PAGES =================
elif page == "Student Registration":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    student_registration_ui()
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Capture Faces":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    capture_faces_ui()
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Train Model":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    train_model_ui()
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Attendance Report":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    attendance_report_ui()
    st.markdown('</div>', unsafe_allow_html=True)

