import streamlit as st
import pyrebase

firebase_config = {
    "apiKey": st.secrets["apiKey"],
    "authDomain": st.secrets["authDomain"],
    "databaseURL": st.secrets["databaseURL"],
    "projectId": st.secrets["projectId"],
    "storageBucket": st.secrets["storageBucket"],
    "messagingSenderId": st.secrets["messagingSenderId"],
    "appId": st.secrets["appId"],
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()


