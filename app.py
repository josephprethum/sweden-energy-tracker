import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Sweden Smart Dashboard 2026", layout="wide", page_icon="🇸🇪")

# 2. Sidebar (Shared settings)
with st.sidebar:
    st.header("📍 Region & Data")
    region = st.selectbox("Electricity Area", ["SE1", "SE2", "SE3", "SE4"], index=2)
    petrol_price = st.number_input("E10 Petrol (kr/L)", value=15.04)
    st.divider()
    st.write("Current Date:", datetime.now().strftime('%Y-%m-%d'))

# 3. Define the Tabs
tab_energy, tab_food = st.tabs(["⚡ Energy & Driving", "🛒 Grocery Tracker"])

# --- TAB 1: ENERGY & COMPARISON ---
with tab_energy:
    st.header("Electricity vs. Petrol Comparison")
    
    # Fetch Live Data
    date_path = datetime.now().strftime('%Y/%m-%d')
    url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_path}_{region}.json"
    
    try:
        res = requests.get(url).json()
        energy_list = []
        for i in range(0, len(res), 4):
            item = res[i]
            el_kwh = item['SEK_per_kWh']
            # Cost to drive 10km (Assuming 2kWh/mil for EV and 0.65L/mil for Petrol)
            cost_ev = round(el_kwh * 2.0, 2)
            cost_petrol = round(petrol_price * 0.65, 2)
            
            energy_list.append({
                "Time": item['time_start'][11:16],
                "El Price (kr/kWh)": round(el_kwh, 2),
                "E10 Price (kr/L)": petrol_price,
                "EV Cost/10km": f"{cost_ev} kr",
                "Petrol Cost/10km": f"{cost_petrol} kr",
                "Winner": "⚡ Electric" if cost_ev < cost_petrol else "⛽ Petrol"
            })
        
        st.dataframe(pd.DataFrame(energy_list), use_container_width=True)
    except:
        st.error("Could not load live energy data. Check your connection.")

# --- TAB 2: FOOD INFO ---
with tab_food:
    st.header("Grocery Price Index & VAT Calculator")
    
    # Static 2026 Market Data
    st.write("### Weekly Staples Comparison (Average SEK)")
    food_data = {
        "Product": ["Milk (1.5L)", "Butter (500g)", "Bread (Loaf)", "Coffee (450g)"],
        "Willys": [16.50, 48.90, 24.00, 52.00],
        "ICA": [17.90, 54.90, 28.50, 59.00],
        "Coop": [18.20, 56.00, 29.00, 62.00]
    }
    st.table(pd.DataFrame(food_data))
    
    st.divider()
    
    # 2026 VAT Calculator
    st.subheader("💰 2026 VAT Relief Calculator")
    st.info("The Swedish government is reducing food VAT from 12% to 6% on April 1st, 2026.")
    user_bill = st.number_input("Enter your current grocery bill (SEK):", value=1000.0)
    
    # Math: Removing 12% VAT and adding 6% VAT
    price_no_vat = user_bill / 1.12
    new_price = price_no_vat * 1.06
    savings = user_bill - new_price
    
    st.metric(label="New Price After April 1st", value=f"{new_price:.2f} SEK", delta=f"-{savings:.2f} SEK")
