# ProTrader-V2

## 1) Install dependencies
```bash
pip install -r requirements.txt
```

## 2) Run backend (FastAPI)
```bash
uvicorn main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

## 3) Run frontend (Streamlit)
Use **`streamlit_app.py`** as your Streamlit app entrypoint:
```bash
streamlit run streamlit_app.py
```

## 4) Validate backend
```bash
python -m pytest -q
```

---

## Streamlit features
- Gradient dashboard header + cleaner layout
- Health check with clear API error messages
- Quote fetch with in-session history chart
- Explainable prediction cards + probability/contribution charts
- Sidebar controls for backend URL and symbol

## Troubleshooting
- If Streamlit says command not found, run:
  ```bash
  pip install -r requirements.txt
  ```
- Start backend before Streamlit.
- If backend is hosted remotely, set the URL in sidebar (e.g. `https://your-api.example.com`).

## Deploy as a Streamlit app (Streamlit Community Cloud)
1. Push this repo to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Create app and select your repo/branch.
4. Set **Main file path** to `streamlit_app.py`.
5. Deploy.
