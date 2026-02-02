import streamlit as st
from firebase_config import db
import pandas as pd


def attendance_report_ui():
    st.subheader("Attendance Dashboard")

    data = db.child("attendance").get()

    if not data.each():
        st.info("No attendance data found.")
        return

    records = [i.val() for i in data.each()]
    df = pd.DataFrame(records)

    st.dataframe(df)

    st.subheader("Overall Stats")
    st.write("Total Records:", len(df))
    st.write("Total Students:", df["name"].nunique())
    st.write("Total Days:", df["date"].nunique())

    student = st.selectbox("Select Student Profile", df["name"].unique())

    sdf = df[df["name"] == student]

    st.subheader(f"Profile: {student}")
    st.write("Days Present:", sdf["date"].nunique())
    st.write("Total Entries:", len(sdf))



