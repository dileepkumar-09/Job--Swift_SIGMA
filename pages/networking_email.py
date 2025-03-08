import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyD1H-_G1QINMtBOEd1dqqrzU9BBu6AJlbI") # Replace with your actual API key
model = genai.GenerativeModel('models/gemini-1.5-pro')

st.set_page_config(page_title="📧 Networking Email Generator", layout="centered")

st.title("📧 Networking Email Generator")

purpose = st.text_area("Enter the purpose of your networking email:")

if st.button("Generate Email"):
    if purpose:
        prompt_email = f"Generate a professional networking email for this purpose: {purpose}."
        try:
            response_email = model.generate_content(prompt_email)
            st.text_area("Generated Email:", response_email.text, height=200)
        except Exception as e:
            st.error(f"Error generating email: {e}")

    else:
        st.warning("⚠ Please enter the purpose.")