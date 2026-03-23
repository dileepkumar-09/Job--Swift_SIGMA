1. Problem Definition

The job application process is fragmented.

A typical candidate has to:

Edit resumes for each job
Prepare for interviews
Write networking emails
Search for relevant roles

These tasks are:

Repetitive
Time-consuming
Require different tools
Objective

Build a single platform that uses Generative AI to streamline the entire workflow.

2. Solution Overview

We built Job-Swift AI, a GenAI-powered career assistant that integrates multiple job-seeking tasks into one system.

Core Features:
Resume Optimization
Mock Interview Simulation
Networking Email Generation
Job Role Suggestions

3. Key Design Philosophy
The project is NOT about training AI models
It is about engineering workflows around a powerful LLM

So the focus is:

Prompt engineering
Input structuring
Output post-processing
User experience


4. System Architecture
High-Level Flow
User Input (PDF / Text)
        ↓
Preprocessing Layer
        ↓
Prompt Engineering Layer
        ↓
Gemini 1.5 Pro (LLM API)
        ↓
Post-processing Layer
        ↓
UI Output (Streamlit)


6. Input Handling
   
Example: Resume Upload
User uploads a PDF
We do NOT send PDF directly to AI
We extract text using pdfplumber
PDF → Text Extraction → Clean Text

Then:
Combine with user input (job description)
Inject into prompt template

6. Prompt Engineering Layer
Instead of:
"Improve my resume"

we generate structured prompts like:

Optimize the following resume for this job description.

Resume:
<extracted text>

Job Description:
<user input>
Why this matters:
Reduces ambiguity
Increases relevance
Produces consistent outputs

7. Model Layer
We used:
Google Gemini 1.5 Pro

Important clarification:
❌ No internet search
❌ No real-time data
❌ No semantic retrieval (RAG)

✔ Uses pretrained knowledge + prompt context

8. Module Breakdown
8.1 Resume Optimizer

Flow:

PDF → Text → Prompt → Gemini → Optimized Resume → PDF

Output:
Structured resume
Downloadable PDF

8.2 Mock Interview System
Flow:
Job Role → Prompt → Questions
User Answers → Prompt → Feedback

Features:

Multi-question flow
Session tracking
Structured evaluation:
Rating
Strengths
Improvements

8.3 Networking Email Generator
Flow:

User Intent → Prompt → Professional Email

Use cases:

Cold outreach
Referral requests
LinkedIn messages

8.4 Job Suggestions
Flow:

Resume + Preferences → Prompt → Suggested Roles + Companies

These are AI-generated suggestions, NOT real job listings

9. Post-Processing Layer

After AI response:

Resume → Converted to PDF using FPDF
Interview → Structured display
Emails → Editable text box
10. Tech Stack
Frontend: Streamlit
LLM: Google Gemini 1.5 Pro
PDF Handling: pdfplumber, FPDF
State Management: Streamlit session state

Key strengths:

Task-specific prompt engineering
Modular architecture
End-to-end workflow design
Handling unstructured inputs (PDFs)
Converting AI outputs into usable artifacts

12. Limitations

No real job API integration
No RAG / embeddings
Outputs depend on LLM reliability
No automated validation layer
API keys not securely managed
