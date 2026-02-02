import streamlit as st
import pandas as pd
from firebase_config import db

def attendance_report_ui():
    st.title("Attendance Dashboard")

    try:
        data = db.child("attendance").get()
    except:
        st.warning("No attendance data yet. Mark attendance first.")
        return

    if not data.each():
        st.warning("No attendance records found.")
        return

    records = []

    for item in data.each():
        val = item.val()
        records.append([
            val.get("name"),
            val.get("date"),
            val.get("time"),
            val.get("confidence")
        ])

    df = pd.DataFrame(records, columns=["Name", "Date", "Time", "Confidence"])

    st.subheader("Overall Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Total Students", df["Name"].nunique())
    col3.metric("Total Days", df["Date"].nunique())

    st.markdown("---")

    students = df["Name"].unique()
    selected_student = st.selectbox("Select Student Profile", students)

    student_df = df[df["Name"] == selected_student]

    st.subheader(f"Profile: {selected_student}")
    st.metric("Days Present", student_df["Date"].nunique())
    st.metric("Total Entries", len(student_df))
    st.dataframe(student_df.sort_values("Date", ascending=False))

