import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

st.title("Automate Internshala Applications")

job_links = st.text_area("Enter Internshala job application links (one per line):")
name = st.text_input("Enter your full name:")
email = st.text_input("Enter your email address:")
phone = st.text_input("Enter your phone number:")
resume_path = st.file_uploader("Upload your resume (PDF):", type=["pdf"])
additional_details = st.text_area("Enter any additional details:")

if st.button("Open Browser and Wait for Login"):
    driver = webdriver.Chrome()
    driver.get("https://internshala.com/login")
    st.session_state.driver = driver
    st.session_state.manual_login_complete = False

if st.button("Continue with Applications") and "driver" in st.session_state and not st.session_state.manual_login_complete:
    st.session_state.manual_login_complete = True
    driver = st.session_state.driver
    links = job_links.splitlines()

    for link in links:
        try:
            driver.get(link.strip())
            print(f"Applying to {link.strip()}")

            # ... (your existing code to fill out the form and upload resume) ...

            try:
                proceed_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Proceed to application')]")))
                proceed_button.click()
                print("Proceed clicked. Please answer the questions in the browser window.")
            except Exception as e:
                st.error(f"Error clicking proceed: {e}")
                driver.save_screenshot(f"error_proceed_{link.strip().replace('/', '_')}.png")
                continue

            st.info(f"Please manually answer the multiple-choice questions for {link.strip()}. Then click 'Submit Application'.")
            st.session_state.current_link = link.strip() #store current link.
            st.session_state.application_submitted = False #reset application submission state.

            # Wait for manual submission
            while not st.session_state.application_submitted:
                time.sleep(1) #check every second.
                if st.button("Submit Application"):
                    st.session_state.application_submitted = True;
                    break;

            if st.session_state.application_submitted:
                st.success(f"Application submitted for {st.session_state.current_link}")

        except Exception as e:
            st.error(f"General error submitting application for {link.strip()}: {e}")
            driver.save_screenshot(f"error_general_{link.strip().replace('/', '_')}.png")
        finally:
            pass
    driver.quit()
    del st.session_state.driver
else:
    if "manual_login_complete" in st.session_state and st.session_state.manual_login_complete:
        pass
    elif "driver" in st.session_state:
        st.info("Please manually log in to Internshala, then click 'Continue with Applications'.")
    else:
        st.info("Click 'Open Browser and Wait for Login' to start.")