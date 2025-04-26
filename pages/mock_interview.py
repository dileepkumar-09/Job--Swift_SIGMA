import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyChQymJA8UPXvVqzLx1fo_KN8HzlN-rQ_w")  # Replace with your actual API key
model = genai.GenerativeModel('models/gemini-1.5-pro')

st.set_page_config(page_title="Mock Interview System", layout="wide")
st.title("🎤 AI-Powered Mock Interview")

job_role = st.text_input("Enter the job role for the interview:")
num_questions = st.selectbox("Select the number of questions:", [1, 3, 5, 7, 10], index=2)

if st.button("Start Interview"):
    if job_role:
        prompt_interview = (
            f"As an expert interviewer, generate exactly {num_questions} well-structured and diverse interview questions for the role of {job_role}. "
            "Ensure they cover:\n"
            "- *Technical Skills* (related to the job role)\n"
            "- *Behavioral Questions* (STAR method)\n"
            "- *Problem-Solving & Situational Judgment*\n"
            "- *Communication & Teamwork*\n"
            "Each question should be *clear, specific, and numbered properly* (Q1, Q2, etc.).\n"
            "Do NOT include any explanations, only provide the questions."
        )
        try:
            response_interview = model.generate_content(prompt_interview)
            raw_questions = response_interview.text.strip().split("\n")
            questions = [q.strip() for q in raw_questions if q.strip().startswith("Q")]

            if len(questions) < num_questions:
                st.error("Some questions were incomplete. Please restart the interview.")
            else:
                st.session_state["questions"] = questions[:num_questions]
                st.session_state["answers"] = [""] * num_questions
                st.session_state["feedback"] = [""] * num_questions
                st.session_state["current_question"] = 0
                st.success("✅ Questions generated! Scroll down to answer.")
        except Exception as e:
            st.error(f"Error generating interview questions: {e}")
    else:
        st.warning("⚠ Please enter a job role to start the mock interview.")

if "questions" in st.session_state and st.session_state["current_question"] < len(st.session_state["questions"]):
    idx = st.session_state["current_question"]
    question = st.session_state["questions"][idx]

    st.subheader(f"Question {idx + 1}:")
    st.write(question)

    user_response = st.text_area("Your Answer", value=st.session_state["answers"][idx], key=f"answer_{idx}")

    if st.button("Submit Answer", key=f"submit_{idx}"):
        st.session_state["answers"][idx] = user_response

        feedback_prompt = (
            f"Evaluate this interview response based on the following criteria:\n"
            f"- Clarity of response\n"
            f"- Depth of knowledge\n"
            f"- Relevance to the question\n\n"
            f"Provide feedback in this structured format:\n"
            f"1️⃣ *Rating (1-5)*: Score the answer based on correctness & clarity.\n"
            f"2️⃣ *Strengths & Improvements*: Mention what was done well and areas to improve.\n"
            f"3️⃣ *Areas to Focus On*: Suggest topics the candidate should study further.\n\n"
            f"Question: {question}\n"
            f"Answer: {user_response}\n\n"
            f"Feedback:"
        )

        try:
            feedback_response = model.generate_content(feedback_prompt)
            st.session_state["feedback"][idx] = feedback_response.text.strip()
        except Exception as e:
            st.session_state["feedback"][idx] = f"Error generating feedback: {e}"

        st.session_state["current_question"] += 1
        st.rerun()  


if "feedback" in st.session_state and st.session_state["current_question"] > 0:
    idx = st.session_state["current_question"] - 1  
    question = st.session_state["questions"][idx]
    user_response = st.session_state["answers"][idx]
    feedback = st.session_state["feedback"][idx]

    st.write("### Feedback")
    st.write(feedback)


if "current_question" in st.session_state and st.session_state["current_question"] >= len(st.session_state["questions"]):
    st.success("🎉 Mock interview completed! Reviewing overall performance...")

    overall_feedback_prompt = (
        "Analyze the following interview responses and provide an overall performance evaluation.\n"
        "Consider the following:\n"
        "- Strengths and weaknesses in responses\n"
        "- How well the candidate demonstrated technical and soft skills\n"
        "- Any noticeable patterns in mistakes or areas needing improvement\n\n"
        "Provide the evaluation in this format:\n"
        "1️⃣ *Overall Rating (1-5)*: Assess the overall interview performance.\n"
        "2️⃣ *Key Strengths*: Highlight the candidate's best aspects.\n"
        "3️⃣ *Improvement Areas*: Suggest what to improve for better performance.\n"
        "4️⃣ *Final Advice*: Recommendations for further preparation.\n\n"
        "Responses:\n"
    )

    for idx, (q, ans, fb) in enumerate(zip(st.session_state["questions"], st.session_state["answers"], st.session_state["feedback"])):
        overall_feedback_prompt += f"Q{idx + 1}: {q}\nAnswer: {ans}\nFeedback: {fb}\n\n"

    try:
        overall_feedback_response = model.generate_content(overall_feedback_prompt)
        st.write("## 📊 Overall Interview Performance")
        st.write(overall_feedback_response.text.strip())
    except Exception as e:
        st.error(f"Error generating overall feedback: {e}")
