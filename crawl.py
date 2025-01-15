import streamlit as st
from PyPDF2 import PdfReader
from fpdf import FPDF
import asyncio
from crawl4ai import AsyncWebCrawler

# Initialize the asynchronous web crawler
crawler = AsyncWebCrawler()

# Streamlit app title
st.title("AI-Powered Resume Enhancer with Crawl4AI")

# Step 1: Upload Resume PDF
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

# Step 2: Input Job Information
company_name = st.text_input("Enter the Company Name:")
job_role = st.text_input("Enter the Role You're Applying For:")
job_post_url = st.text_input("Enter the Job Post URL:")

# Process if all inputs are provided
if uploaded_file and company_name and job_role and job_post_url:
    # Step 3: Extract Content from Uploaded PDF
    pdf_reader = PdfReader(uploaded_file)
    original_content = ""
    for page in pdf_reader.pages:
        original_content += page.extract_text()

    st.write("Extracted Resume Content:")
    st.text(original_content)

    # Step 4: Scrape Job Description with Crawl4AI
    st.write("Fetching Job Description...")

    async def fetch_job_description(url):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown

    job_description = asyncio.run(fetch_job_description(job_post_url))
    st.text("Job Description Extracted:")
    st.text(job_description[:500])  # Display part of the description

    # Step 5: Extract Keywords (Placeholder for actual implementation)
    st.write("Extracting Keywords...")
    # Implement your keyword extraction logic here
    extracted_keywords = ["example", "keywords"]  # Replace with actual keywords
    st.write("Keywords Extracted:")
    st.text(", ".join(extracted_keywords))

    # Step 6: Enhance Resume (Placeholder for actual implementation)
    st.write("Enhancing Resume...")
    # Implement your resume enhancement logic here
    enhanced_resume_content = original_content  # Replace with enhanced content
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
