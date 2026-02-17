# ProTrader-V2

## 1) Run backend (FastAPI)
Start the API server first:

```bash
uvicorn main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

## 2) Run frontend (Streamlit)
Use **`streamlit_app.py`** as your Streamlit app entry file:

```bash
streamlit run streamlit_app.py
```

By default the app calls backend URL `http://localhost:8000` (editable from sidebar).

## 3) Install dependencies

```bash
pip install -r requirements.txt
```

## 4) Validate backend

```bash
python -m pytest -q
```

---

## Deploy as a Streamlit app (Streamlit Community Cloud)
1. Push this repo to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Create app and point it to this repo/branch.
4. Set **Main file path** to `streamlit_app.py`.
5. Add secrets/environment variables only if your backend URL is remote.

If backend is hosted elsewhere, set it in sidebar input after app launch.
