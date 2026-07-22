# LynQX Project Setup Guide

Follow these simple guidelines to run LynQX locally:

1. **Clone project** and enter working directory.
2. **Create Python virtual environment**:
   ```powershell
   python -m venv venv
   .\\venv\\Scripts\\activate
   ```
3. **Install python packages**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure GROQ API Key** inside `.env` file:
   ```env
   GROQ_API_KEY="your_api_key_here"
   ```
5. **Run Streamlit app**:
   ```bash
   streamlit run app.py
   ```
