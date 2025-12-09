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
  <div style="margin-top:7px;">
    <div style="text-align:center;">
      <h1 style="font-size:3rem;font-weight:800;color:white;margin-bottom:0.4rem;">
        LynQx
      </h1>
    </div>
    <div style="text-align:left;margin-left:2px;">
      <h2 style="font-size:1.8rem;font-weight:700;color:white;margin-top:0.2rem;">
        Step&nbsp;2:&nbsp;Generate&nbsp;Test&nbsp;Scenarios
      </h2>
    </div>
  </div>
  """
  st.markdown(html, unsafe_allow_html=True)
  st.markdown("<hr style='margin-top:5px; margin-bottom:10px;'>", unsafe_allow_html=True)

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