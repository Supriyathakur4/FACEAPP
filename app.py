import cv2
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import os
def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ---------------- CONFIG ----------------
FACE_SIZE = (200, 200)
CONF_THRESHOLD = 70
MIN_CONFIDENCE_PERCENT = 60

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

# ---------------- LOAD MODELS ----------------
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

face_cascade = cv2.CascadeClassifier(
    "haarcascade/haarcascade_frontalface_default.xml"
)

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="FaceApp", layout="wide")
st.title("🎓 FaceApp – Smart Attendance System")

col1, col2 = st.columns(2)
start = col1.button("▶ Start Camera")
stop = col2.button("⏹ Stop Camera")

FRAME_WINDOW = st.image([])

# ---------------- ATTENDANCE FILE ----------------
today = datetime.now().strftime("%Y-%m-%d")
attendance_file = f"attendance_{today}.csv"

if not os.path.exists(attendance_file):
    pd.DataFrame(columns=["Name", "Time", "Confidence"]).to_csv(attendance_file, index=False)

attendance_df = pd.read_csv(attendance_file)
marked_names = set(attendance_df["Name"].tolist())

unknown_count = 0

# ---------------- SIDEBAR ----------------
st.sidebar.header("📊 Live Dashboard")
st.sidebar.write(f"📅 Date: {today}")
st.sidebar.write(f"👥 Trained students: {len(id_name)}")
st.sidebar.write(f"✅ Marked today: {len(marked_names)}")

# ---------------- CAMERA ----------------
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
                    pd.DataFrame([[name, time_now, confidence_percent]],
                                 columns=["Name", "Time", "Confidence"]) \
                        .to_csv(attendance_file, mode="a", header=False, index=False)
                    marked_names.add(name)

                label = f"{name} ({confidence_percent}%)"
                color = (0, 255, 0)
            else:
                label = "Unknown"
                color = (0, 0, 255)
                unknown_count += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

else:
    cap.release()

# ---------------- SUMMARY ----------------
st.markdown("---")
st.subheader("📊 Attendance Summary")

df = pd.read_csv(attendance_file)
st.write(f"✅ Total Present: {df['Name'].nunique()}")
st.write(f"❓ Unknown Faces Detected: {unknown_count}")

if not df.empty:
    st.write(f"⏰ First Entry: {df.iloc[0]['Time']}")
    st.write(f"⏰ Last Entry: {df.iloc[-1]['Time']}")

# ---------------- DOWNLOAD ----------------
st.markdown("---")
st.subheader("📥 Download Attendance")

with open(attendance_file, "rb") as f:
    st.download_button(
        "⬇ Download Attendance CSV",
        f,
        file_name=attendance_file,
        mime="text/csv"
    )

# ---------------- TABLE ----------------
st.subheader("📋 Attendance Records")
st.dataframe(df)
