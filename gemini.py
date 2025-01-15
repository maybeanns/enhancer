import streamlit as st
from PyPDF2 import PdfReader
from fpdf import FPDF
from bs4 import BeautifulSoup
import requests
from google.cloud import language_v1
from google.generativeai import PaLMClient

# Set up Google Cloud credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google-cloud-key.json"

# Initialize Google Natural Language Client
language_client = language_v1.LanguageServiceClient()

# Initialize PaLM Client
palm_client = PaLMClient()

# Title of the Streamlit App
st.title("AI-Powered Resume Enhancer (Google AI Edition)")

# Step 1: Upload Resume PDF
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

# Step 2: Input Job Information
company_name = st.text_input("Enter the Company Name:")
job_role = st.text_input("Enter the Role You're Applying For:")
job_post_url = st.text_input("Enter the Job Post URL:")

# Process if inputs are provided
if uploaded_file and company_name and job_role and job_post_url:
    # Step 3: Extract Content from Uploaded PDF
    pdf_reader = PdfReader(uploaded_file)
    original_content = ""
    for page in pdf_reader.pages:
        original_content += page.extract_text()

    st.write("Extracted Resume Content:")
    st.text(original_content)

    # Step 4: Scrape Job Description
    st.write("Fetching Job Description...")
    response = requests.get(job_post_url)
    soup = BeautifulSoup(response.content, "html.parser")
    job_description = soup.get_text()
    st.text("Job Description Extracted:")
    st.text(job_description[:500])  # Display part of the description

    # Step 5: Extract Keywords using Google NLP
    st.write("Extracting Keywords with Google NLP...")
    document = language_v1.Document(content=job_description, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = language_client.analyze_entities(document=document)
    extracted_keywords = [entity.name for entity in response.entities]
    st.write("Keywords Extracted:")
    st.text(", ".join(extracted_keywords))

    # Step 6: Enhance Resume using PaLM API
    st.write("Enhancing Resume with Google PaLM...")
    prompt = (
        f"Enhance the following resume content for the job role '{job_role}' at '{company_name}'. "
        f"Make it ATS-friendly by including these keywords: {', '.join(extracted_keywords)}.\n\n{original_content}"
    )
    enhanced_resume_content = palm_client.generate_text(prompt=prompt)
    st.write("Enhanced Resume Content:")
    st.text(enhanced_resume_content)

    # Step 7: Generate PDF with Enhanced Content
    st.write("Generating Enhanced Resume...")
    pdf_writer = FPDF()
    pdf_writer.add_page()
    pdf_writer.set_font("Arial", size=12)
    for line in enhanced_resume_content.split("\n"):
        pdf_writer.multi_cell(0, 10, line)

    output_pdf_path = "enhanced_resume.pdf"
    pdf_writer.output(output_pdf_path)

    # Step 8: Provide Download Option
    with open(output_pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Download Enhanced Resume",
            data=pdf_file,
            file_name="Enhanced_Resume.pdf",
            mime="application/pdf"
        )
else:
    st.write("Please upload your resume and fill out all fields to proceed.")