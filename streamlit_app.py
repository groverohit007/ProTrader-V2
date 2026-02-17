from datetime import datetime
from typing import List

import httpx
import streamlit as st


st.set_page_config(page_title="ProTrader V2", page_icon="📈", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 1.5rem;}
    .hero {
        padding: 1rem 1.25rem;
        border-radius: 14px;
        background: linear-gradient(120deg, #0f172a 0%, #1d4ed8 60%, #0ea5e9 100%);
        color: white;
        margin-bottom: 1rem;
    }
    .muted {opacity: 0.85;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h2 style="margin:0;">📈 ProTrader V2 Dashboard</h2>
      <p class="muted" style="margin:0.35rem 0 0 0;">Live quotes, explainable predictions, and health checks from your FastAPI backend.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def api_get(url: str, timeout: int = 10):
    try:
        response = httpx.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json(), None
    except httpx.HTTPError as exc:
        return None, str(exc)


def api_post(url: str, payload: dict, timeout: int = 20):
    try:
        response = httpx.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json(), None
    except httpx.HTTPError as exc:
        return None, str(exc)


def parse_prices(raw: str) -> List[float]:
    return [float(x.strip()) for x in raw.split(",") if x.strip()]


with st.sidebar:
    st.header("⚙️ Connection")
    base_url = st.text_input("FastAPI Base URL", "http://localhost:8000")
    symbol = st.text_input("Symbol", "AAPL").upper()
    st.caption("Tip: Start backend first with `uvicorn main:app --reload --port 8000`.")

if "quote_history" not in st.session_state:
    st.session_state.quote_history = []

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Selected Symbol", symbol)

with col2:
    st.metric("Backend URL", base_url.replace("http://", "").replace("https://", ""))

with col3:
    st.metric("Last refresh", datetime.now().strftime("%H:%M:%S"))

health_tab, quote_tab, prediction_tab = st.tabs(["🩺 Health", "💹 Quote", "🧠 Prediction"])

with health_tab:
    st.subheader("Backend Health")
    if st.button("Check Health", type="primary"):
        data, error = api_get(f"{base_url}/health")
        if error:
            st.error(f"Health check failed: {error}")
        else:
            st.success("Backend is reachable.")
            st.json(data)

with quote_tab:
    st.subheader("Live Quote")
    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("Fetch Latest Quote", use_container_width=True):
            data, error = api_get(f"{base_url}/market/quote/{symbol}")
            if error:
                st.error(f"Quote request failed: {error}")
            else:
                st.session_state.quote_history.append(
                    {
                        "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
                        "price": data.get("price", 0),
                    }
                )
                st.success(f"Latest {symbol} quote loaded.")
                st.json(data)

    with c2:
        if st.button("Clear Quote History", use_container_width=True):
            st.session_state.quote_history = []
            st.info("Quote history cleared.")

    if st.session_state.quote_history:
        st.line_chart([row["price"] for row in st.session_state.quote_history], height=240)
        st.dataframe(st.session_state.quote_history, use_container_width=True)
    else:
        st.caption("No quote history yet. Click **Fetch Latest Quote**.")

with prediction_tab:
    st.subheader("Explainable Prediction")

    default_prices = ",".join(str(100 + i) for i in range(30))
    prices_text = st.text_area("Input prices (comma-separated, min 30)", default_prices, height=120)

    if st.button("Run Prediction", type="primary"):
        try:
            prices = parse_prices(prices_text)
            if len(prices) < 30:
                st.warning("Please provide at least 30 prices.")
            else:
                payload = {"symbol": symbol, "prices": prices}
                data, error = api_post(f"{base_url}/predictions/explain", payload)
                if error:
                    st.error(f"Prediction request failed: {error}")
                else:
                    st.success("Prediction generated successfully.")

                    left, right = st.columns(2)
                    with left:
                        st.metric("Signal", data.get("signal", "N/A"))
                        st.metric("Confidence", data.get("confidence", "N/A"))
                    with right:
                        st.write("Probabilities")
                        st.bar_chart(data.get("probabilities", {}))

                    st.write("Feature Contributions")
                    st.bar_chart(data.get("contributions", {}))
                    st.json(data)
        except ValueError:
            st.error("Invalid price format. Please use numbers separated by commas.")
