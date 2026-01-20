# FaceApp – Face Recognition Attendance System

FaceApp is a real-time face recognition attendance system built using
Python, OpenCV (LBPH), and Streamlit. It detects faces using a webcam
and automatically marks attendance.

## Features
- Face detection using Haar Cascade
- Face recognition using LBPH
- Streamlit-based web interface
- Automatic attendance marking

## How to Run
```bash
pip install numpy==1.24.4
pip install opencv-contrib-python-headless==4.5.5.64
pip install streamlit pandas
python train.py
streamlit run app.py
