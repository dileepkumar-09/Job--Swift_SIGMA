import streamlit as st
import google.generativeai as genai
import pdfplumber
import requests
from bs4 import BeautifulSoup


genai.configure(api_key="AIzaSyChQymJA8UPXvVqzLx1fo_KN8HzlN-rQ_w")  # Replace with your API key
model = genai.GenerativeModel('models/gemini-1.5-pro')


def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text


def find_company_website(company_name):
    try:
        search_query = f"company website {company_name}"
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('a')
        if link and "url?q=" in link['href']:
            url = link['href'].split("url?q=")[1].split("&")[0]
            if url.startswith("http"):
                return url
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error finding website: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

st.header("Job Suggestions")
uploaded_resume_jobs = st.file_uploader("Upload your resume (PDF format) for job recommendations", type=["pdf"], key="resume_jobs")
preferred_jobs = st.text_area("Enter your preferred job roles (comma-separated):")

if st.button("Generate Job Suggestions"):
    if uploaded_resume_jobs and preferred_jobs:
        resume_text_jobs = extract_text_from_pdf(uploaded_resume_jobs)
        prompt_jobs = f"""Based on the following resume, suggest suitable job roles, including the company name: {preferred_jobs}
        \nResume:\n{resume_text_jobs}\n\nJob Suggestions:"""

        try:
            response_jobs = model.generate_content(prompt_jobs)
            job_suggestions_list = response_jobs.text.split("\n")
            st.success("✅ Job Suggestions Generated!")

            for job in job_suggestions_list:
                if job.strip():
                    parts = job.split("at")
                    company_name = parts[1].strip() if len(parts) > 1 else None

                    st.markdown(
                        f"""
                        <div style='border: 1px solid #ddd; padding: 10px; border-radius: 8px; margin: 5px 0; background-color: black; color:white;'>
                        <strong>{job}</strong>
                        </div>
                        """, unsafe_allow_html=True
                    )
                    if company_name:
                        website = find_company_website(company_name)
                        if website:
                            st.markdown(f"Apply here: <a href='{website}' target='_blank'>{company_name} Website</a>", unsafe_allow_html=True)
                        else:
                            st.write(f"Could not find a website for {company_name}.")

        except Exception as e:
            st.error(f"Error generating job suggestions: {e}")
    else:
        st.warning("⚠ Please upload a resume and enter preferred job roles.")
