import streamlit as st
import cv2
import os
import time

FACE_SIZE = (200, 200)

def capture_faces_ui():
    st.title("Face Dataset Capture")

    user_id = st.text_input("Enter Numeric User ID")
    start = st.button("Start Capturing")

    FRAME_WINDOW = st.image([])

    if start and user_id:
        save_path = f"dataset/{user_id}"
        os.makedirs(save_path, exist_ok=True)

        face_cascade = cv2.CascadeClassifier(
            "haarcascade/haarcascade_frontalface_default.xml"
        )

        cap = cv2.VideoCapture(0)
        count = 0

        st.info("Keep your face in front of camera")

        while count < 40:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, FACE_SIZE)

                count += 1
                cv2.imwrite(f"{save_path}/{count}.jpg", face)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, f"Captured: {count}/40",
                            (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0,255,0), 2)

                time.sleep(0.2)

            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        cap.release()
        st.success("✅ Dataset captured successfully!")
