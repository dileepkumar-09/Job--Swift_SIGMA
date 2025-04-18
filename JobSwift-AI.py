import streamlit as st
import google.generativeai as genai
import pdfplumber
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
# Configure Gemini API
genai.configure(api_key="AIzaSyBL16j3Opn57dHXSVgtv9K0ioW8h-zF8nc")
model = genai.GenerativeModel('models/gemini-1.5-pro')

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Function to generate and save a PDF
def generate_pdf(content, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    sections = content.split("\n\n")
    for section in sections:
        if section.strip():
            lines = section.split("\n")
            if lines[0].strip().isupper():  # Section header
                pdf.set_font("Arial", 'B', size=14)
                pdf.cell(0, 10, lines[0], 0, 1, 'L')
                pdf.set_font("Arial", size=12)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Add line separator
                lines = lines[1:]
            for line in lines:
                safe_line = line.encode("latin-1", "ignore").decode("latin-1")
                pdf.multi_cell(0, 8, safe_line, 0, 'L')
    pdf_file_path = f"./{filename}"
    pdf.output(pdf_file_path, "F")
    return pdf_file_path

# Function to generate optimized resume
def generate_optimized_resume(resume_text, job_description):
    prompt = f"""Optimize the following resume for the given job description:
    \nResume:\n{resume_text}\n\nJob Description:\n{job_description}\n\nOptimized Resume:"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating resume: {e}"

# Background Image CSS
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("genaiimage1.jpg");
background-size: cover;
background-repeat: no-repeat;
background-attachment: local;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Title with Deep Blue Color
st.markdown(
    """
    <style>
    .title {
        color: #00008B; /* Deep Blue color */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='title'>Job-Swift AI - SIGMA</h1>", unsafe_allow_html=True)

# Resume Optimization Section (Link to Page)
st.header("Resume Optimization")
if st.button("Go to Resume Optimizer"):
    st.markdown(
        f"""
        <a href="/resume_optimizer" target="_self">Go to Resume Optimizer</a>
        """,
        unsafe_allow_html=True,
    )

# Job Suggestions Redirect
st.header("Job Suggestions with your skill set")
if st.button("Go to Job Suggestions"):
    st.markdown(
        f"""
        <a href="/job_suggestions" target="_self">Go to Job Suggestions</a>
        """,
        unsafe_allow_html=True,
    )

# Mock Interview
st.header("Mock Interview")
if st.button("Go to Mock Interview"):
    st.markdown(
        f"""
        <a href="/mock_interview" target="_self">Go to Mock Interview</a>
        """,
        unsafe_allow_html=True,
    )

# Cover Letter Generation
st.header("Cover Letter Generation")
if st.button("Go to Cover Letter Generator"):
    st.markdown(
        f"""
        <a href="/cover_letter" target="_self">Go to Cover Letter Generator</a>
        """,
        unsafe_allow_html=True,
    )

# Networking Email Generator
st.header("Networking Email Generator")
if st.button("Go to Networking Email Generator"):
    st.markdown(
        f"""
        <a href="/networking_email" target="_self">Go to Networking Email Generator</a>
        """,
        unsafe_allow_html=True,
    )

#Automate Applications
st.header("Automate Application")
if st.button("Go to Automate Application"):
    st.markdown(
        f"""
        <a href="/automate_application" target="_self">Go to Automate Application</a>
        """,
        unsafe_allow_html=True,
    )
