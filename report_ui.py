import streamlit as st
import pandas as pd
from firebase_config import db

def attendance_report_ui():
    st.title("Attendance Report")

    data = db.child("attendance").get()

    if not data.each():
        st.warning("No attendance records found.")
        return

    records = []

    for item in data.each():
        val = item.val()
        records.append([
            val["name"],
            val["date"],
            val["time"],
            val["confidence"]
        ])

    df = pd.DataFrame(records, columns=["Name", "Date", "Time", "Confidence"])

    students = df["Name"].unique()
    selected_student = st.selectbox("Select Student", students)

    student_df = df[df["Name"] == selected_student]

    st.subheader(f"Attendance History for {selected_student}")
    st.dataframe(student_df)

    st.success(f"Total Days Present: {student_df['Date'].nunique()}")
