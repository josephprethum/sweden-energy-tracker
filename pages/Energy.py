import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("⚡ Energy & Fuel Comparison")

# --- 1. SETTINGS ---
region = st.sidebar.selectbox("Region", ["SE1", "SE2", "SE3", "SE4"], index=2)
petrol_price = st.sidebar.number_input("E10 Petrol (kr/L)", value=15.14)

# --- 2. DYNAMIC FETCHING WITH BACKUP ---
date_str = datetime.now().strftime('%Y/%m-%d')
url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_str}_{region}.json"

try:
    response = requests.get(url, timeout=10)
    data = response.json()
    
    # CHECK: Is the data actually there?
    if not data or len(data) == 0:
        st.warning("⚠️ API returned empty data for today. Showing estimated prices.")
        # Create dummy data so the app doesn't look broken
        data = [{"time_start": "2026-01-30T12:00:00", "SEK_per_kWh": 1.20}]

    rows = []
    for item in data[::4]:  # Skip by 4 to show hourly even with 15-min data
        el_price = item.get('SEK_per_kWh', 0)
        cost_ev = round(el_price * 2.0, 2)
        cost_gas = round(petrol_price * 0.65, 2)
        
        rows.append({
            "Time": item['time_start'][11:16],
            "Electricity (kr/kWh)": el_price,
            "EV Cost /10km": f"{cost_ev} kr",
            "Petrol Cost /10km": f"{cost_gas} kr",
            "Winner": "⚡ Electric" if cost_ev < cost_gas else "⛽ Petrol"
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True)

except Exception as e:
    st.error(f"📡 Connection Error: {e}")
    st.info("The electricity API might be down. Please try refreshing in 5 minutes.")