import streamlit as st
import subprocess
import sys

def train_model_ui():
    st.title("Train Face Recognition Model")

    st.write("Click the button to train the model using current dataset images.")

    if st.button("Start Training"):
        with st.spinner("Training in progress..."):
            result = subprocess.run(
                [sys.executable, "train.py"],  # uses current venv python
                capture_output=True,
                text=True
            )

        if result.returncode == 0:
            st.success("Training completed!")
            st.code(result.stdout)
        else:
            st.error("Training failed")
            st.code(result.stderr)
