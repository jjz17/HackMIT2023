# Startup Application

1. start ngrok to expose localhost to internet
```ngrok http 8000```
2. start fastapi for backend services
```uvicorn jason.main:app --reload```
3. start streamlit for frontend
```streamlit run jason/frontend.py```
