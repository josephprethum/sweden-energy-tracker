import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("⚡ Energy & Driving Comparison")

# --- 1. SETTINGS & INPUTS ---
with st.sidebar:
    st.header("Dashboard Settings")
    # Region SE3 is Stockholm/Central Sweden
    region = st.selectbox("Select Price Region", ["SE1", "SE2", "SE3", "SE4"], index=2)
    
    # Updated 2026 Petrol Price (SEK/L)
    petrol_price = st.number_input("E10 Petrol Price (kr/L)", value=15.14, step=0.10)
    
    st.divider()
    st.write("### Efficiency Defaults")
    cons_ev = st.slider("Electric (kWh/10km)", 1.0, 3.5, 2.0)
    cons_petrol = st.slider("Petrol (L/10km)", 0.4, 1.2, 0.65)

# --- 2. FETCH LIVE ELECTRICITY DATA ---
date_today = datetime.now().strftime('%Y/%m-%d')
el_url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_today}_{region}.json"

try:
    response = requests.get(el_url)
    el_data = response.json()
    
    # Prepare the table rows
    table_rows = []
    
    for item in el_data:
        # Time and Price
        time_start = item['time_start'][11:16]
        price_per_kwh = item['SEK_per_kWh']
        
        # Calculation: Cost to drive 10km (1 mil)
        cost_mil_ev = round(price_per_kwh * cons_ev, 2)
        cost_mil_petrol = round(petrol_price * cons_petrol, 2)
        
        # Determine the winner
        winner = "⚡ Electric" if cost_mil_ev < cost_mil_petrol else "⛽ Petrol"
        savings = round(abs(cost_mil_petrol - cost_mil_ev), 2)
        
        table_rows.append({
            "Time": time_start,
            "El Price (kr/kWh)": round(price_per_kwh, 2),
            "E10 Price (kr/L)": petrol_price,
            "EV Cost /10km": f"{cost_mil_ev} kr",
            "Petrol Cost /10km": f"{cost_mil_petrol} kr",
            "Cheapest": winner,
            "Difference (kr)": savings
        })

    # --- 3. DISPLAY DATA ---
    df = pd.DataFrame(table_rows)
    
    # Current Stats
    avg_el = df["El Price (kr/kWh)"].mean()
    st.metric("Avg Electricity Price Today", f"{avg_el:.2f} SEK/kWh")
    
    st.subheader(f"Hourly Comparison for {region}")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 4. Download Feature
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data as CSV", data=csv, file_name=f"energy_comparison_{date_today}.csv")

except Exception as e:
    st.error(f"Waiting for live price data... (API Status: {e})")