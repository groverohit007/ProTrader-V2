import requests
import streamlit as st

st.set_page_config(page_title="ProTrader V2 Dashboard", layout="wide")
st.title("ProTrader V2 + FastAPI")

base_url = st.sidebar.text_input("FastAPI base URL", "http://localhost:8000")
symbol = st.sidebar.text_input("Symbol", "AAPL").upper()

st.subheader("Health")
if st.button("Check backend health"):
    r = requests.get(f"{base_url}/health", timeout=10)
    st.json(r.json())

st.subheader("Quote")
if st.button("Get quote"):
    r = requests.get(f"{base_url}/market/quote/{symbol}", timeout=10)
    st.json(r.json())

st.subheader("Prediction")
prices_text = st.text_area("Prices (comma separated)", "100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129")
if st.button("Explain prediction"):
    prices = [float(x.strip()) for x in prices_text.split(",") if x.strip()]
    payload = {"symbol": symbol, "prices": prices}
    r = requests.post(f"{base_url}/predictions/explain", json=payload, timeout=20)
    st.json(r.json())
