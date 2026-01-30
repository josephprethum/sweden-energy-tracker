import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Sweden Energy Tracker 2026", layout="wide")

st.title("🇸🇪 Sweden Energy & Driving Tracker")
st.markdown("Live comparison of Electricity (15-min intervals) vs. E10 Petrol prices.")

# Sidebar for User Inputs
with st.sidebar:
    st.header("Settings")
    region = st.selectbox("Select Price Region", ["SE1", "SE2", "SE3", "SE4"], index=2)
    petrol_price = st.number_input("Current E10 Price (SEK/L)", value=15.14)
    consumption_ev = st.slider("EV Consumption (kWh/10km)", 1.0, 3.0, 2.0)
    consumption_petrol = st.slider("Petrol Consumption (L/10km)", 0.4, 1.2, 0.65)

# 1. Fetch Live Data
date_str = datetime.now().strftime('%Y/%m-%d')
el_url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_str}_{region}.json"

try:
    res = requests.get(el_url).json()
    
    # 2. Process Data
    table_data = []
    for i in range(0, len(res), 4): # Hourly
        item = res[i]
        el_kwh = item['SEK_per_kWh']
        cost_p = round(petrol_price * consumption_petrol, 2)
        cost_e = round(el_kwh * consumption_ev, 2)
        
        table_data.append({
            "Time": item['time_start'][11:16],
            "El (kr/kWh)": round(el_kwh, 2),
            "EV Cost/10km": cost_e,
            "Petrol Cost/10km": cost_p,
            "Winner": "⚡ Electric" if cost_e < cost_p else "⛽ Petrol"
        })

    df = pd.DataFrame(table_data)

    # 3. Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Electricity", f"{df['El (kr/kWh)'].mean():.2f} kr")
    col2.metric("Avg EV Cost/mil", f"{df['EV Cost/10km'].mean():.2f} kr")
    col3.metric("Petrol Cost/mil", f"{cost_p} kr")

    # 4. Interactive Table
    st.subheader(f"Hourly Comparison for {region}")
    st.dataframe(df.style.highlight_min(subset=['EV Cost/10km'], color='#ccffcc'), use_container_width=True)

except Exception as e:
    st.error(f"Could not connect to data: {e}")