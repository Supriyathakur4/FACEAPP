import streamlit as st
import pyrebase

def get_auth():
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
    return firebase.auth()


def login_ui():
    st.title("Login")

    choice = st.selectbox("Login / Signup", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    auth = get_auth()

    if choice == "Signup":
        if st.button("Create Account"):
            try:
                auth.create_user_with_email_and_password(email, password)
                st.success("Account created. Please login.")
            except Exception as e:
                st.error(e)

    if choice == "Login":
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state["user"] = user
                st.success("Logged in successfully")
                st.rerun()
            except Exception as e:
                st.error(e)


