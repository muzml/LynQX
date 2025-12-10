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
            
# ---------------------- (Step2) Generate test case -------------------------
# Step 2 page layout
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

# ---------------------- (Step3) Review Test Case -------------------------
if "show_step3" not in st.session_state:
    st.session_state["show_step3"] = False

if st.session_state.get("show_step2", False) and "generated_test_cases" in st.session_state:
    if st.button("Next: Review Test Scenarios", type="primary"):
        st.session_state["show_step3"] = True
        st.session_state["show_step2"] = False
        st.success("✅ Proceeding to scenario review...")
        st.rerun()

# Step 3 page layout]
# ---------------------- (STEP 3) Review Test Scenarios -------------------------
# ---------------------- (STEP 3) Review Test Scenarios -------------------------
# ---------------------- (STEP 3) Scenario Verification -------------------------
elif st.session_state["current_step"] == 3:
    import streamlit as st

    # ========== Header ==========
    html = """
    <head>
      <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
      <style>
        .lynqx-title {
          font-family: 'Dancing Script', cursive;
          font-size: 5rem;
          font-weight: 900;
          color: white;
          text-shadow: 0 0 10px rgba(255,255,255,0.4), 0 0 30px rgba(164,116,255,0.3);
          margin-bottom: 1rem;
        }
        .subtitle {
          font-family: 'Poppins', sans-serif;
          font-size: 1.6rem;
          font-weight: 500;
          color: white;
          margin-bottom: 1rem;
        }
        hr {border: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem;}
        .custom-expander > div:first-child {
          border: 2px solid rgba(255, 99, 71, 0.6) !important;
          border-radius: 10px !important;
          background-color: rgba(255,99,71,0.05) !important;
        }
        .approve-btn {
          background-color: #176d47;
          color: white;
          border: none;
          border-radius: 6px;
          padding: 6px 24px;
          font-family: 'Poppins', sans-serif;
          font-weight: 500;
        }
        .approve-btn:hover {background-color: #1b8a5e;}
        .reject-btn {
          background-color: #7c2525;
          color: white;
          border: none;
          border-radius: 6px;
          padding: 6px 24px;
          font-family: 'Poppins', sans-serif;
          font-weight: 500;
        }
        .reject-btn:hover {background-color: #a43c3c;}
      </style>
    </head>

    <div class="lynqx-title">LynQX</div>
    <div class="subtitle">Step 3: Scenario Verification</div>
    <hr>
    """
    st.markdown(html, unsafe_allow_html=True)

    # ========== Create Custom Scenario ==========
    with st.expander("+ Create Custom Scenario", expanded=False):
        st.markdown("### Add Your Own Test Scenario")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Scenario Name")
        with col2:
            scen_type = st.selectbox("Scenario Type", ["Positive", "Negative", "Edge Case"])
        scen_id = st.text_input("Scenario ID", "TS009", disabled=True)
        desc = st.text_area("Description", height=100)
        related = st.text_input("Related User Story")
        if st.button("Add Scenario"):
            if name and desc and related:
                line = f"{scen_id}: {name} - {desc}"
                st.session_state["generated_test_cases"] = st.session_state.get("generated_test_cases", "") + "\n" + line
                st.success("✅ Custom Scenario Added!")
            else:
                st.warning("⚠️ Fill all fields before adding a scenario.")

    st.markdown("---")
    st.subheader("Review Test Scenarios")

    # ========== Review Section ==========
    gen = st.session_state.get("generated_test_cases", "")
    if not gen.strip():
        st.warning("⚠️ No scenarios found. Go back to Step 2.")
    else:
        if "scenario_status" not in st.session_state:
            st.session_state["scenario_status"] = {}

        lines = [l.strip() for l in gen.split("\n") if l.strip()]
        for i, sc in enumerate(lines):
            status = st.session_state["scenario_status"].get(i, "pending")
            border_style = (
                "border:2px solid rgba(46,204,113,0.7);" if status == "approved"
                else "border:2px solid rgba(255,99,71,0.6);" if status == "rejected"
                else "border:1px solid rgba(255,255,255,0.1);"
            )

            with st.container():
                col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
                with col1:
                    with st.expander(f"TS00{i+1}: {sc} " +
                                     ("(Approved ✅)" if status=="approved" else "(Rejected ❌)" if status=="rejected" else "(Pending Review)"),
                                     expanded=False):
                        st.markdown(f"**Type:** Positive")
                        st.markdown(f"**Description:** Enter valid username and password, and verify redirection.")
                        st.markdown(f"**Related User Story:** US00{i+1}")
                        st.text_area(f"Feedback for TS00{i+1}", placeholder="Enter feedback (optional)")
                with col2:
                    if st.button("Approve", key=f"a_{i}"):
                        st.session_state["scenario_status"][i] = "approved"
                        st.rerun()
                with col3:
                    if st.button("Reject", key=f"r_{i}"):
                        st.session_state["scenario_status"][i] = "rejected"
                        st.rerun()
                st.markdown(f"<div style='{border_style} border-radius:8px; margin-bottom:10px;'></div>", unsafe_allow_html=True)

        approved = [s for s in st.session_state["scenario_status"].values() if s == "approved"]
        st.markdown(f"**Approved Scenarios:** {len(approved)}/{len(lines)}")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Back to Step 2"):
                st.session_state["current_step"] = 2
                st.rerun()
        with col2:
            if st.button("Next ➜ Create Test Cases"):
                if approved:
                    st.session_state["approved_scenarios"] = approved
                    st.session_state["current_step"] = 4
                    st.rerun()
                else:
                    st.warning("⚠️ Approve at least one scenario to continue.")
