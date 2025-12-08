import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Set Generate page configuration
st.set_page_config(page_title="LynQX - Generate Test Scenarios", layout="wide")

# Load API KEY
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


# Set Home page configuration
st.set_page_config(page_title="LynQX", layout="wide") 

# Sidebar Navigation
with st.sidebar:
    st.title("Process Steps")
    st.markdown("""
    1. Input User Story
    2. Generate Test Scenarios
    3. Review Scenarios
    4. Create Test Cases
    5. Verify Coverage
    6. Prepare for Execution
    7. Upload Test Results
    8. Generate Report
    """)
    st.markdown("---")
    st.caption("LynQX - Streamlining Your Testing Process")

# Main Page Header
html = """
<div style="margin-top:40px;">
  <div style="text-align:center;">
    <h1 style="font-size:3rem;font-weight:800;color:white;margin-bottom:0.4rem;">
      LynQx
    </h1>
  </div>
  <div style="text-align:left;margin-left:2px;">
    <h2 style="font-size:1.8rem;font-weight:700;color:white;margin-top:0.2rem;">
      Step&nbsp;1:&nbsp;Input&nbsp;User&nbsp;Stories
    </h2>
  </div>
</div>
"""
st.markdown(html, unsafe_allow_html=True)

# Input Section
tab1, tab2 = st.tabs(["📝 Enter Text", "📁 Upload File"])

with tab1:
    user_input = st.text_area("Enter User Stories (any format)", height=200, placeholder="Type your user stories here...")

with tab2:
    uploaded_file = st.file_uploader("Upload a file containing user stories", type=["txt", "docx", "pdf", "csv"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        user_input = st.text_area("File Content", value=content, height=200)

# Instructions
with st.expander("Instructions"):
    st.markdown("""
    - Each user story should describe **a feature or requirement**.  
    - Follow the format: `US001: <Description>`  
    - Example:
        - US001: Add Student Record  
        - US002: Update Student Record  
        - US003: Delete Student Record  
    - Click **Next** to generate test scenarios automatically.
    """)

# Next Button
if st.button("Next: Generate Test Scenarios", type="primary"):
    if user_input.strip() == "":
        st.success("✅ User stories recorded successfully! Proceed to Step 2.")
    else:
        st.warning("⚠️ Please enter or upload at least one user story before proceeding.")
        # Here you would typically redirect to the next page or process the input