from train_ui import train_model_ui
from capture_faces import capture_faces_ui
from student_ui import student_registration_ui
import cv2
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import os

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
st.title("🎓 FaceApp – Smart Attendance System")

theme = st.sidebar.selectbox("🎨 Select Theme", ["Light", "Dark"])
load_css(theme)

# -------- Sidebar Navigation --------
page = st.sidebar.radio(
    "Navigate",
    ["📷 Attendance", "👤 Student Registration", "📸 Capture Faces", "🧠 Train Model"]
)

# ================= ATTENDANCE PAGE =================
if page == "📷 Attendance":
    col1, col2 = st.columns(2)
    start = col1.button("▶ Start Camera")
    stop = col2.button("⏹ Stop Camera")
    snapshot_btn = st.button("📸 Take Snapshot")

    FRAME_WINDOW = st.image([])

    today = datetime.now().strftime("%Y-%m-%d")
    attendance_file = f"attendance_{today}.csv"

    if not os.path.exists(attendance_file):
        pd.DataFrame(columns=["Name", "Time", "Confidence"]).to_csv(attendance_file, index=False)

    attendance_df = pd.read_csv(attendance_file)
    marked_names = set(attendance_df["Name"].tolist())
    unknown_count = 0

    st.sidebar.header("Live Dashboard")
    st.sidebar.write(f"Date: {today}")
    st.sidebar.write(f" Trained students: {len(id_name)}")
    st.sidebar.write(f"Marked today: {len(marked_names)}")

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

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(rgb_frame)

            if snapshot_btn:
                if not os.path.exists("snapshots"):
                    os.makedirs("snapshots")
                filename = f"snapshots/snap_{datetime.now().strftime('%H%M%S')}.png"
                cv2.imwrite(filename, frame)
                st.success(f"Snapshot saved: {filename}")
    else:
        cap.release()

    st.markdown("---")
    st.subheader("📋 Attendance Records")
    df = pd.read_csv(attendance_file)
    st.dataframe(df)

    st.subheader("📈 Attendance Visualization")
    if not df.empty:
        chart_data = df["Name"].value_counts().reset_index()
        chart_data.columns = ["Name", "Count"]
        st.bar_chart(chart_data.set_index("Name"))

    st.subheader("🏆 Student Attendance Ranking")
    if not df.empty:
        ranking = df["Name"].value_counts().reset_index()
        ranking.columns = ["Name", "Attendance Count"]
        ranking["Rank"] = ranking["Attendance Count"].rank(ascending=False).astype(int)
        ranking = ranking.sort_values("Rank")
        st.table(ranking)

# ================= OTHER PAGES =================
elif page == "👤 Student Registration":
    student_registration_ui()

elif page == "📸 Capture Faces":
    capture_faces_ui()

elif page == "🧠 Train Model":
    train_model_ui()
