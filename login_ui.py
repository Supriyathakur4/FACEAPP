import streamlit as st
from firebase_config import auth

def login_ui():
    st.title("Login")

    choice = st.selectbox("Login / Signup", ["Login", "Signup"])

    with st.form("auth_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(choice)

        if submit:
            try:
                if choice == "Signup":
                    auth.create_user_with_email_and_password(email, password)
                    st.success("Account created. Please login.")
                else:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state["user"] = user
                    st.success("Logged in successfully")
                    st.rerun()
            except Exception as e:
                st.error("Invalid email or password")

