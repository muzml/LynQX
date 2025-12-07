import streamlit as st

# Set page configuration
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


