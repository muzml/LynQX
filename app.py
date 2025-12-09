import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Set Home page configuration
st.set_page_config(page_title="LynQX", layout="wide") 

# Load API KEY
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ Missing Groq API Key! Please add it to your .env file as GROQ_API_KEY='your_key_here'.")
    st.stop()

client = Groq(api_key=api_key)

# Initialize session state variables
if "current_step" not in st.session_state:
    st.session_state["current_step"] = 1
if "user_stories" not in st.session_state:
    st.session_state["user_stories"] = ""
if "generated_test_cases" not in st.session_state:
    st.session_state["generated_test_cases"] = ""

# Sidebar Navigation
st.sidebar.title("SDLC Process Steps")

steps = [
    "Input User Story",
    "Generate Test Scenarios",
    "Review Scenarios",
    "Create Test Cases",
    "Verify Coverage",
    "Prepare for Execution",
    "Upload Test Results",
    "Generate Report"
]

# Sidebar highlighting logic
for i, step in enumerate(steps, start=1):
    if i < st.session_state["current_step"]:
        st.sidebar.success(step)  # ✅ Completed
    elif i == st.session_state["current_step"]:
        st.sidebar.info(step)     # 🔵 Current
    else:
        st.sidebar.markdown(step) # ⚪ Future

st.sidebar.markdown("---")
st.sidebar.caption("LynQX - Streamlining Your Testing Process")

# Main Page Header
if st.session_state["current_step"] == 1:
  html = """
  <head>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>
      .lynqx-title {
        font-family: 'Dancing Script', cursive !important;
        font-size: 14rem;
        font-weight: 900;
        color: white;
        display: block;
        text-align: center;
        transform: scale(1.5);
        transform-origin: center;
        margin-top: 2rem;
        margin-bottom: 10rem;
        padding-bottom: 4rem;
        letter-spacing: 5px;
        line-height: 1.2;
        text-shadow: 0 0 6px rgba(255, 255, 255, 0.4),
                     0 0 15px rgba(164, 116, 255, 0.2);
      }
      .lynqx-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;         
        font-weight: 500;         
        color: rgba(255, 255, 255, 0.85);  
        text-align: left;
        margin-left: 10px;
        margin-top: 3rem;
      }
      .block-container {
        max-width: 100% !important;
        padding-left: 2rem;
        padding-right: 2rem;
      }
    </style>
  </head>

  <div>
    <h1 class="lynqx-title">LynQX</h1>
    <h2 class="lynqx-subtitle">Step&nbsp;1:&nbsp;Input&nbsp;User&nbsp;Stories</h2>
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
  if st.button("Next ➜ Generate Test Scenarios", type="primary"):
        if user_input.strip():
            st.session_state["user_stories"] = user_input.strip()
            st.session_state["current_step"] = 2  # move to Step 2
            st.rerun()
        else:
            st.warning("⚠️ Please enter or upload at least one user story before proceeding.")

# Generate test case page Header
elif st.session_state["current_step"] == 2:
  html = """
  <head>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>
      .lynqx-container-v4 {
        position: relative;
        width: 100%;
        margin-bottom: 1rem;       
      }

      .lynqx-title-v4 {
        font-family: 'Dancing Script', cursive !important;
        font-size: 22rem;
        font-weight: 900;
        color: white;
        text-align: left;
        margin: 0;
        padding-left: 2rem;
        margin-top: 1rem;
        margin-bottom: 3rem;       
        letter-spacing: 7px;
        line-height: 1.1;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.5),
                     0 0 20px rgba(164, 116, 255, 0.25),
                     0 0 40px rgba(164, 116, 255, 0.15);
      }

      .lynqx-subtitle-v4 {
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.85);
        text-align: left;
        margin-left: 10px;
        margin-top: 2rem;           
        margin-bottom: 0rem;    
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 0.3rem;   
        width: 98%;
      }

      .block-container {
        max-width: 100% !important;
        padding-left: 2rem;
        padding-right: 2rem;
      }
    </style>
  </head>

  <div class="lynqx-container-v4">
    <h1 class="lynqx-title-v4">LynQX</h1>
    <h2 class="lynqx-subtitle-v4">Step&nbsp;2:&nbsp;Generate&nbsp;Test&nbsp;Scenarios</h2>
  </div>
  """
  st.markdown(html, unsafe_allow_html=True)

# Load User Stories from Step 1
  user_stories_input = st.session_state["user_stories"]
  st.subheader("User Stories from Step 1")
  st.text_area("User Stories", user_stories_input, height=200, disabled=True)

# AI Test Case Generation
  if st.button("Generate Test Scenarios", type="primary"):
      user_stories = [line.strip() for line in user_stories_input.split("\n") if line.strip()]

      prompt = f"""
You are an expert QA engineer. Genrate 2-3 detailed test cases for each of the following user stories:

{user_stories}

Format:
TestCaseID: Description - Expected Result
"""
      with st.spinner("Generating test scenarios..."):
          try:
              response = client.chat.completions.create(
              model="llama-3.3-70b-versatile",
              messages=[{"role": "user", "content": prompt}],
              )
              result = response.choices[0].message.content
        
              st.success("✅ Test scenarios generated successfully! (Scroll down to view them)")
              st.markdown("---")
              st.text_area("Generated Test Scenarios", value = result, height = 300)

              st.session_state["generated_test_cases"] = result

          except Exception as e:
              st.error(f"❌ An error occurred while generating test scenarios: {e}")

  col1, col2 = st.columns(2)
  with col1:
      if st.button("⬅ Back to Step 1"):
        st.session_state["current_step"] = 1
        st.rerun()
  with col2:
      if st.button("Next ➜ Review Scenarios"):
        st.session_state["current_step"] = 3
        st.rerun()