import streamlit as st
import google.generativeai as genai
import pdfplumber
from fpdf import FPDF

genai.configure(api_key="AIzaSyChQymJA8UPXvVqzLx1fo_KN8HzlN-rQ_w")  # Replace with actual API key
model = genai.GenerativeModel('models/gemini-1.5-pro')

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def generate_pdf(content, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    sections = content.split("\n\n")
    for section in sections:
        if section.strip():
            lines = section.split("\n")
            if lines[0].strip().isupper():  
                pdf.set_font("Arial", 'B', size=14)
                pdf.cell(0, 10, lines[0], 0, 1, 'L')
                pdf.set_font("Arial", size=12)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())  
                lines = lines[1:]
            for line in lines:
                safe_line = line.encode("latin-1", "ignore").decode("latin-1")
                pdf.multi_cell(0, 8, safe_line, 0, 'L')
    pdf_file_path = f"./{filename}"
    pdf.output(pdf_file_path, "F")
    return pdf_file_path

def generate_optimized_resume(resume_text, job_description):
    prompt = f"""Optimize the following resume for the given job description:
    \nResume:\n{resume_text}\n\nJob Description:\n{job_description}\n\nOptimized Resume:"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating resume: {e}"

st.set_page_config(page_title="Resume Optimizer", layout="centered")
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
        }
        .stTextArea>textarea {
            font-size: 16px;
        }
        .stMarkdown {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Resume Optimizer")
st.write("Enhance your resume to match the job description and improve your chances!")

uploaded_resume = st.file_uploader("📂 Upload your resume (PDF format)", type=["pdf"])
job_description = st.text_area("📝 Enter the job description for optimization:", height=150)

if st.button("🔍 Optimize Resume"):
    if uploaded_resume and job_description:
        with st.spinner("Extracting text from resume..."):
            resume_text = extract_text_from_pdf(uploaded_resume)

        with st.spinner("Optimizing resume with AI..."):
            optimized_resume = generate_optimized_resume(resume_text, job_description)

        st.success("✅ Optimized Resume Generated!")
        st.markdown("### 🎯 Optimized Resume Preview")
        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; background-color: black;">
        <pre>{optimized_resume}</pre>
        </div>
        """, unsafe_allow_html=True)

        pdf_path = generate_pdf(optimized_resume, "Optimized_Resume.pdf")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download Optimized Resume (PDF)", f, file_name="Optimized_Resume.pdf")
    else:
        st.warning("⚠ Please upload a resume and enter a job description.")
