import streamlit as st
import subprocess

def train_model_ui():
    st.title("🧠 Train Face Recognition Model")

    st.write("Click the button to train the model using current dataset images.")

    if st.button("🚀 Start Training"):
        with st.spinner("Training in progress..."):
            result = subprocess.run(
                ["python", "train.py"],
                capture_output=True,
                text=True
            )

        st.success("✅ Training completed!")
        st.code(result.stdout)
