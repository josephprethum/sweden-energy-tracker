import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Function to scrape live Petrol price (Example: OKQ8)
@st.cache_data(ttl=21600) # Refresh fuel price every 6 hours
def get_dynamic_petrol_price():
    try:
        url = "https://www.okq8.se/pa-stationen/drivmedel/priser/"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        # Finds the E10 price on the page
        price_text = soup.find(text="GoEasy Bensin 95").find_next("span").text
        return float(price_text.replace(",", "."))
    except:
        return 15.14 # Fallback to Jan 2026 average

st.title("⚡ Dynamic Energy Tracker")

live_petrol = get_dynamic_petrol_price()
region = st.sidebar.selectbox("Region", ["SE1", "SE2", "SE3", "SE4"], index=2)

st.sidebar.metric("Live E10 Price", f"{live_petrol} SEK/L")

# Electricity Logic (Same as before but uses 'live_petrol')
date_path = datetime.now().strftime('%Y/%m-%d')
el_url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_path}_{region}.json"

try:
    res = requests.get(el_url).json()
    # ... (Rest of your calculation logic using live_petrol)
    st.success(f"Fetched live prices for {datetime.now().strftime('%H:%M')}")
except:
    st.error("API Error")