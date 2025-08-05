import subprocess

# Start FastAPI
fastapi_proc = subprocess.Popen(["uvicorn", "fastapi_backend:app", "--reload", "--port", "8000"])

# Start Streamlit
streamlit_proc = subprocess.Popen(["streamlit", "run", "streamlit_frontend.py"])

# Wait for both
fastapi_proc.wait()
streamlit_proc.wait()