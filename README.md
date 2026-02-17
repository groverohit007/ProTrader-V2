# ProTrader-V2

## Backend (FastAPI)
Run the API server:

```bash
uvicorn main:app --reload --port 8000
```

Open docs at `http://localhost:8000/docs`.

## Streamlit frontend
Use `streamlit_app.py` as the Streamlit entry file.

```bash
streamlit run streamlit_app.py
```

In the sidebar, keep base URL as `http://localhost:8000` (or change if your API runs elsewhere).

## Quick health check

```bash
python -m pytest -q
```
