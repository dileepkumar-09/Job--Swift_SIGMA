import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime
import re


genai.configure(api_key="AIzaSyChQymJA8UPXvVqzLx1fo_KN8HzlN-rQ_w")  # Replace with your API key
model = genai.GenerativeModel('models/gemini-1.5-pro')


def clean_cover_letter(text, your_name):
    """Removes redundant occurrences of name, date, and closing signature."""
    text = re.sub(rf"{your_name}.*", "", text, flags=re.IGNORECASE)  
    text = re.sub(r"Date:.*\n?", "", text, flags=re.IGNORECASE)  
    text = re.sub(r"(Sincerely,|Best regards,|Yours truly,|Regards,)\n?.*", "", text, flags=re.IGNORECASE)  
    return text.strip()

def generate_cover_letter(your_name, job_description, company_name):
    prompt = f"Generate a professional cover letter.\nYour Name: {your_name}\nJob Description:\n{job_description}\nCompany Name: {company_name}\n\nCover Letter:"
    try:
        response = model.generate_content(prompt)
        return clean_cover_letter(response.text, your_name) 
    except Exception as e:
        return f"Error: {e}"

def create_cover_letter_pdf(your_name, company_name, cover_letter_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, your_name, ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "Email: example@example.com | Phone: +1234567890", ln=True, align="C")
    pdf.cell(200, 10, "", ln=True) 

    pdf.cell(200, 10, f"Date: {datetime.datetime.today().strftime('%B %d, %Y')}", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, f"To: Hiring Manager, {company_name}", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "", ln=True)

    pdf.set_font("Arial", "", 12)
    sections = cover_letter_text.split("\n\n") 
    for section in sections:
        pdf.multi_cell(0, 8, section)
        pdf.cell(200, 5, "", ln=True)

    pdf.cell(200, 10, "Sincerely,", ln=True)
    pdf.cell(200, 10, your_name, ln=True)

    pdf_file_path = "./Cover_Letter.pdf"
    pdf.output(pdf_file_path, "F")
    return pdf_file_path

st.set_page_config(page_title="AI-Powered Cover Letter Generator", layout="wide")
st.title("Cover Letter Generator")

your_name = st.text_input("Enter your name:")
company_name = st.text_input("Enter the company name:")
job_description = st.text_area("Enter the job description:")

if st.button("Generate Cover Letter"):
    if your_name and company_name and job_description:
        cover_letter_text = generate_cover_letter(your_name, job_description, company_name)
        pdf_path = create_cover_letter_pdf(your_name, company_name, cover_letter_text)

        st.success("✅ Cover Letter PDF Generated!")
        with open(pdf_path, "rb") as f:
            st.download_button("Download Cover Letter", f, file_name="Cover_Letter.pdf")
    else:
        st.warning("⚠ Please fill in all required fields.")
