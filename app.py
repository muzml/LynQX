import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import re

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
if "scenarios" not in st.session_state:
    st.session_state["scenarios"] = []
if "approved_scenarios" not in st.session_state:
    st.session_state["approved_scenarios"] = []

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

# Generate CSS styling for sidebar buttons dynamically based on the current step
current_step = st.session_state["current_step"]
css_styles = []

for i in range(1, len(steps) + 1):
    if i < current_step:
        # Completed step: dark green background, bright green text
        css_styles.append(f"""
        div.st-key-nav_{i} button {{
            background-color: #133020 !important;
            color: #3ecf8e !important;
            border: 1px solid rgba(62, 207, 142, 0.15) !important;
        }}
        div.st-key-nav_{i} button:hover {{
            background-color: #1a3e2c !important;
            color: #3ecf8e !important;
        }}
        """)
    elif i == current_step:
        # Active step: dark blue/navy background, bright blue text
        css_styles.append(f"""
        div.st-key-nav_{i} button {{
            background-color: #1b2a47 !important;
            color: #3b82f6 !important;
            border: 1px solid rgba(59, 130, 246, 0.15) !important;
            font-weight: 600 !important;
        }}
        div.st-key-nav_{i} button:hover {{
            background-color: #21355c !important;
            color: #3b82f6 !important;
        }}
        """)
    else:
        # Future step: transparent background, white text, no border
        css_styles.append(f"""
        div.st-key-nav_{i} button {{
            background-color: transparent !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: none !important;
            padding-left: 0 !important;
        }}
        div.st-key-nav_{i} button:hover {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: #ffffff !important;
        }}
        """)

# Combine and inject all styles
st.markdown(f"""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
    
    /* Base button override */
    div[data-testid="stSidebar"] button {{
        display: flex !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 0.6rem 0.8rem !important;
        border-radius: 8px !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }}
    
    div[data-testid="stSidebar"] button * {{
        color: inherit !important;
        font-weight: inherit !important;
        font-family: inherit !important;
    }}
    
    {" ".join(css_styles)}
</style>
""", unsafe_allow_html=True)

# Sidebar clickable navigation
for i, step in enumerate(steps, start=1):
    if st.sidebar.button(step, key=f"nav_{i}", use_container_width=True):
        st.session_state["current_step"] = i
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("LynQX - Streamlining Your Testing Process")

# ---------------------- (Step 1) Input User Story -------------------------
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

    with st.expander("Instructions"):
        st.markdown("""
        ### How to provide user stories: 
                    
        Option 1:Enter text directly
        - Enter requirements in any format
        - Click "Format My Stories" to convert
        
        Option 2: Upload a file
        - Supported formats: .txt, .docx, .pdf, .csv
        """)

    if st.button("Next ➜ Generate Test Scenarios", type="primary"):
        if user_input.strip():
            st.session_state["user_stories"] = user_input.strip()
            st.session_state["current_step"] = 2
            st.rerun()
        else:
            st.warning("⚠️ Please enter or upload at least one user story before proceeding.")

# ---------------------- (Step 2) Generate Test Scenarios -------------------------
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

    user_stories_input = st.session_state["user_stories"]
    st.subheader("User Stories from Step 1")
    st.text_area("User Stories", user_stories_input, height=200, disabled=True)

    if st.button("Generate Test Scenarios", type="primary"):
        user_stories = [line.strip() for line in user_stories_input.split("\n") if line.strip()]

        prompt = f"""
        As a Test Scenario Generator, analyze these user stories and generate comprehensive test scenarios.
        Include positive test scenarios, negative test scenarios, and edge cases.
        - scenario_id: A unique identifier (TS001, TS002, etc.)
        - scenario_name: A descriptive name
        - scenario_type: "Positive", "Negative", or "Edge case"
        - description: Detailed description of the scenario
        - related_user_story: The ID or brief description of the related user story
        - status: "Pending Review"
    User Stories:
    {user_stories}
    Format: TestCaseID: Description — Expected Result
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
                st.text_area("Generated Test Scenarios", value=result, height=300)
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

# ---------------------- (Step 3) Review Test Scenarios -------------------------
if st.session_state["current_step"] == 3:
    import re

    # ---------- HEADER ----------
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
        hr {
          border: 1px solid rgba(255,255,255,0.1);
          margin-bottom: 2rem;
        }
      </style>
    </head>

    <div class="lynqx-title">LynQX</div>
    <div class="subtitle">Step 3: Scenario Verification</div>
    <hr>
    """
    st.markdown(html, unsafe_allow_html=True)

    gen = st.session_state.get("generated_test_cases", "")
    if not gen.strip():
        st.warning("⚠️ No test scenarios found. Please go back to Step 2 and generate them first.")
        st.stop()

    # ---------- PARSE SCENARIOS ONLY ONCE ----------
    if "scenarios" not in st.session_state or not st.session_state["scenarios"]:
        raw_lines = [l.strip() for l in gen.split("\n") if l.strip()]
        scenarios = []
        seen_names = set()

        for line in raw_lines:
            ts_match = re.match(r"^(?:\d+\.\s*)?(?:\*\*)?(TS\d{3})(?:\*\*)?:\s*(.*)", line)
            if ts_match:
                sid = ts_match.group(1).strip()
                name = ts_match.group(2).split("—")[0].split("-")[0].strip()

                # ✅ Prevent duplicates by scenario name
                if name.lower() not in seen_names:
                    seen_names.add(name.lower())
                    scenarios.append({
                        "scenario_id": sid,
                        "scenario_name": name,
                        "description": "",
                        "expected": "",
                        "related_user_story": "",
                        "scenario_type": "Positive",
                        "status": "Pending Review"
                    })

        st.session_state["scenarios"] = scenarios

    # ---------- ADD CUSTOM SCENARIO ----------
    with st.expander("➕ Create Custom Scenario", expanded=False):
        st.subheader("Add Your Own Test Scenario")

        name = st.text_input("Scenario Name")
        col1, col2 = st.columns(2)
        with col1:
            sid = f"TS{len(st.session_state['scenarios'])+1:03d}"
            st.text_input("Scenario ID", value=sid, disabled=True)
        with col2:
            stype = st.selectbox("Scenario Type", ["Positive", "Negative", "Edge Case"])
        desc = st.text_area("Description")
        exp = st.text_area("Expected Result")

        if st.button("Add Scenario", type="primary"):
            if name and desc:
                if name.lower() not in [s["scenario_name"].lower() for s in st.session_state["scenarios"]]:
                    st.session_state["scenarios"].append({
                        "scenario_id": sid,
                        "scenario_name": name.strip(),
                        "description": desc.strip(),
                        "expected": exp.strip(),
                        "scenario_type": stype,
                        "status": "Pending Review"
                    })
                    st.success(f"✅ Scenario {sid} added successfully!")
                    st.rerun()
                else:
                    st.warning("⚠️ Scenario already exists — choose another name.")
            else:
                st.warning("⚠️ Please fill Scenario Name and Description.")

    # ---------- REVIEW TEST SCENARIOS ----------
    st.markdown("---")
    st.subheader("Review Test Scenarios")

    for i, sc in enumerate(st.session_state["scenarios"]):
        status = sc["status"].lower()
        color = (
            "rgba(46,204,113,0.3)" if status == "approved"
            else "rgba(255,99,71,0.3)" if status == "rejected"
            else "rgba(255,255,255,0.05)"
        )
        icon = "🟢" if status == "approved" else "🔴" if status == "rejected" else "⚪"
        expander_title = f"{icon} {sc['scenario_id']}: {sc['scenario_name']} ({sc['status']})"

        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            with st.expander(expander_title, expanded=False):
                st.markdown(f"**Type:** {sc['scenario_type']}")
                st.markdown(f"**Description:** {sc.get('description','N/A')}")
                st.text_area(f"Feedback for {sc['scenario_id']}", placeholder="Enter feedback (optional)", key=f"fb_{i}")
            st.markdown(
                f"<div style='background-color:{color}; height:3px; margin-bottom:8px;'></div>",
                unsafe_allow_html=True
            )

        with col2:
            if st.button("Approve", key=f"a_{i}"):
                st.session_state["scenarios"][i]["status"] = "Approved"
                st.rerun()

        with col3:
            if st.button("Reject", key=f"r_{i}"):
                st.session_state["scenarios"][i]["status"] = "Rejected"
                st.rerun()

        with col4:
            if st.button("Delete", key=f"d_{i}"):
                st.session_state["scenarios"].pop(i)
                st.rerun()

    # ---------- FOOTER ----------
    approved = [s for s in st.session_state["scenarios"] if s["status"].lower() == "approved"]
    st.session_state["approved_scenarios"] = approved

    # Exclude rejected scenarios from total in footer
    total_active = len([s for s in st.session_state["scenarios"] if s["status"].lower() != "rejected"])
    st.markdown(f"**Approved Scenarios:** {len(approved)}/{total_active}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Step 2"):
            st.session_state["current_step"] = 2
            st.rerun()
    with col2:
        if st.button("Next ➜ Create Test Cases") and approved:
            st.session_state["current_step"] = 4
            st.rerun()

# ---------------------- (Step 4) Create Test Cases -------------------------
elif st.session_state["current_step"] == 4:

    html = """
    <div class="lynqx-title">LynQX</div>
    <div class="subtitle">Step 4: Create Test Cases</div>
    <hr>
    """
    st.markdown(html, unsafe_allow_html=True)

    approved = st.session_state.get("approved_scenarios", [])

    if not approved:
        st.warning("⚠️ No approved scenarios found. Please approve scenarios in Step 3.")
        st.stop()

    st.subheader("Approved Scenarios")

    test_cases = []

    for i, sc in enumerate(approved, start=1):
        with st.expander(f"{sc['scenario_id']}: {sc['scenario_name']}", expanded=False):
            steps = st.text_area(
                f"Test Steps for {sc['scenario_id']}",
                placeholder="1. Open application\n2. Enter credentials\n3. Click login",
                key=f"steps_{i}"
            )
            expected = st.text_area(
                f"Expected Result for {sc['scenario_id']}",
                placeholder="User should be logged in successfully",
                key=f"expected_{i}"
            )

            test_cases.append({
                "test_case_id": f"TC{i:03d}",
                "scenario_id": sc["scenario_id"],
                "scenario_name": sc["scenario_name"],
                "steps": steps,
                "expected": expected
            })

    st.session_state["test_cases"] = test_cases

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Review Scenarios"):
            st.session_state["current_step"] = 3
            st.rerun()

    with col2:
        if st.button("Next ➜ Verify Coverage"):
            st.session_state["current_step"] = 5
            st.rerun()


# ---------------------- (Step 5) Verify Coverage -------------------------
elif st.session_state["current_step"] == 5:

    html = """
    <div class="lynqx-title">LynQX</div>
    <div class="subtitle">Step 5: Test Coverage Verification</div>
    <hr>
    """
    st.markdown(html, unsafe_allow_html=True)

    scenarios = st.session_state.get("scenarios", [])
    approved = st.session_state.get("approved_scenarios", [])

    # Exclude rejected scenarios from coverage math
    active_scenarios = [s for s in scenarios if s["status"].lower() != "rejected"]
    total = len(active_scenarios)
    covered = len(approved)
    coverage_pct = int((covered / total) * 100) if total else 0

    st.subheader("Test Coverage Report")
    st.markdown(f"### {coverage_pct}%")

    st.progress(coverage_pct / 100)

    if coverage_pct >= 80:
        st.success("Coverage is acceptable")
    else:
        st.warning("Coverage needs improvement")

    # Covered Aspects
    with st.expander("Covered Aspects", expanded=True):
        for s in approved:
            st.markdown(f"• {s['scenario_name']}")

    # Coverage Gaps - only pending scenarios are considered gaps; rejected ones are ignored/out of scope
    uncovered = [s for s in scenarios if s["status"].lower() == "pending review"]

    with st.expander("Coverage Gaps", expanded=True):
        selected_gaps = []
        for s in uncovered:
            if st.checkbox(s["scenario_name"], key=f"gap_{s['scenario_id']}"):
                selected_gaps.append(s["scenario_name"])

    # Recommendations
    with st.expander("Recommendations", expanded=True):
        if not uncovered:
            st.markdown("✅ All active scenarios are covered.")
        else:
            for s in uncovered:
                st.markdown(
                    f"• Create a test case for **{s['scenario_name']}** to improve coverage."
                )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Create Test Cases"):
            st.session_state["current_step"] = 4
            st.rerun()

    with col2:
        if st.button("Continue to Test Preparation"):
            st.session_state["current_step"] = 6
            st.rerun()

# ---------------------- (Step 6) Prepare for Execution -------------------------
elif st.session_state["current_step"] == 6:
    html = """
    <div class="lynqx-title">LynQX</div>
    <div class="subtitle">Step 6: Prepare for Execution</div>
    <hr>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    st.subheader("Test Execution Preparation Checklist")
    st.checkbox("1. Verify the QA/Testing environment is active and running")
    st.checkbox("2. Ensure test seed data is successfully populated")
    st.checkbox("3. Allocate specific test runs to team members")
    st.checkbox("4. Confirm logging directories are cleared and writeable")
    
    st.markdown("---")
    st.subheader("Download Test Cases Suite")
    
    import json
    tc_suite = st.session_state.get("test_cases", [])
    tc_json = json.dumps(tc_suite, indent=2)
    
    st.download_button(
        label="📥 Export Test Suite (JSON)",
        data=tc_json,
        file_name="lynqx_test_suite.json",
        mime="application/json"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Coverage"):
            st.session_state["current_step"] = 5
            st.rerun()
    with col2:
        if st.button("Next ➜ Upload Test Results"):
            st.session_state["current_step"] = 7
            st.rerun()

# ---------------------- (Step 7) Upload Test Results -------------------------
elif st.session_state["current_step"] == 7:
    html = """
    <div class="lynqx-title">LynQX</div>
    <div class="subtitle">Step 7: Upload Test Results</div>
    <hr>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    st.subheader("Log Execution Run Results")
    
    if "execution_results" not in st.session_state:
        st.session_state["execution_results"] = {}
        
    tc_suite = st.session_state.get("test_cases", [])
    
    if not tc_suite:
        st.warning("⚠️ No test cases found. Please define them in Step 4.")
    else:
        for tc in tc_suite:
            tcid = tc["test_case_id"]
            title = tc["scenario_name"]
            
            st.markdown(f"##### {tcid}: {title}")
            outcome = st.selectbox(
                f"Execution Outcome for {tcid}",
                ["Not Run", "Passed", "Failed", "Blocked"],
                key=f"run_outcome_{tcid}"
            )
            st.session_state["execution_results"][tcid] = outcome
            st.markdown("---")
            
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Prep"):
            st.session_state["current_step"] = 6
            st.rerun()
    with col2:
        if st.button("Next ➜ Generate Report"):
            st.session_state["current_step"] = 8
            st.rerun()

# ---------------------- (Step 8) Generate Report -------------------------
elif st.session_state["current_step"] == 8:
    html = """
    <div class="lynqx-title">LynQX</div>
    <div class="subtitle">Step 8: Generate Report</div>
    <hr>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    st.subheader("Test Execution Report Summary")
    
    results = st.session_state.get("execution_results", {})
    if not results:
        st.warning("⚠️ No execution results captured yet. Please complete Step 7.")
    else:
        total = len(results)
        passed = sum(1 for status in results.values() if status == "Passed")
        failed = sum(1 for status in results.values() if status == "Failed")
        blocked = sum(1 for status in results.values() if status == "Blocked")
        not_run = sum(1 for status in results.values() if status == "Not Run")
        
        st.write(f"Total Executed: {total}")
        st.write(f"Passed: {passed}")
        st.write(f"Failed: {failed}")
        st.write(f"Blocked: {blocked}")
        st.write(f"Not Run: {not_run}")
        
    col1, _ = st.columns(2)
    with col1:
        if st.button("⬅ Back to Results Upload"):
            st.session_state["current_step"] = 7
            st.rerun()
