FaceApp is an AI-powered attendance system that uses face recognition to automatically mark student attendance through a camera. Built with OpenCV, Streamlit, and Firebase, the application allows users to register students, capture face datasets, train a recognition model, and record attendance in real time using a browser camera. It includes secure login with Firebase Authentication, a cloud-based database to store attendance records, and an admin dashboard to view reports and analytics. The project demonstrates how computer vision, web deployment, and cloud services can be combined to create a practical, real-world automation solution for classrooms and institutions.


Features

- Face recognition using LBPH (OpenCV)
- Browser camera support on cloud deployment
- Student registration and dataset capture
- Model training interface
- Firebase Authentication (Login / Signup)
- Firebase Realtime Database for attendance storage
- Attendance dashboard and analytics
- Light / Dark theme UI
- Fully deployed on Streamlit Cloud

  Tech Stack
  
- Python
- OpenCV
- Streamlit
- Firebase (Auth + Realtime DB)
- NumPy, Pandas

How It Works

1. Register a student
2. Capture face images
3. Train the model
4. Login to the app
5. Take a photo from browser camera
6. Face is recognized and attendance is marked
7. View reports in the dashboard
How to run

1. Clone the repo
git clone https://github.com/Supriyathakur4/FACEAPP.git
cd FACEAPP

2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate    # Windows

3. Install dependencies
pip install numpy==1.24.4
pip install opencv-contrib-python-headless==4.5.5.64
pip install streamlit pandas pyrebase4 python-dateutil pillow

 4. Train the model (after capturing faces)
python train.py

 5. Run the app
streamlit run app.py


Project Structure

app.py – Main application
capture_faces.py – Dataset capture
train.py – Model training
student_ui.py – Student registration
report_ui.py – Attendance dashboard
login_ui.py – Firebase authentication

Future Improvements

Auto student name mapping from database
Admin controls for attendance records
Export reports as CSV
Multi-user classroom support
