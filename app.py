import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Sweden Smart Tracker 2026", layout="wide", page_icon="🇸🇪")

# 2. Sidebar Settings (Shared by all tabs)
with st.sidebar:
    st.header("⚙️ Global Settings")
    region = st.selectbox("Electricity Area", ["SE1", "SE2", "SE3", "SE4"], index=2)
    petrol_price = st.number_input("E10 Petrol (kr/L)", value=15.04)
    st.divider()
    st.info("These settings affect both the Energy and Food comparison math.")

# 3. Fetch Energy Data (We do this ONCE at the top)
date_path = datetime.now().strftime('%Y/%m-%d')
el_url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_path}_{region}.json"

energy_df = pd.DataFrame() # Placeholder
try:
    res = requests.get(el_url).json()
    rows = []
    for i in range(0, len(res), 4):
        el_kwh = res[i]['SEK_per_kWh']
        cost_ev = round(el_kwh * 2.0, 2)
        cost_petrol = round(petrol_price * 0.65, 2)
        rows.append({
            "Time": res[i]['time_start'][11:16],
            "El Price (kr/kWh)": round(el_kwh, 2),
            "EV Cost/10km": f"{cost_ev} kr",
            "Petrol Cost/10km": f"{cost_petrol} kr",
            "Winner": "⚡ Electric" if cost_ev < cost_petrol else "⛽ Petrol"
        })
    energy_df = pd.DataFrame(rows)
except:
    st.sidebar.error("Could not fetch Live Energy data.")

# 4. Create the Tabs
tab_energy, tab_food = st.tabs(["⚡ Energy & Driving", "🛒 Grocery Tracker"])

# --- ENERGY TAB ---
with tab_energy:
    st.header("Electricity vs. Petrol Comparison")
    if not energy_df.empty:
        st.dataframe(energy_df, use_container_width=True)
    else:
        st.warning("No energy data to display.")

# --- FOOD TAB ---
with tab_food:
    st.header("🛒 All Items Price Comparison")
    
    # Master List of Items
    food_data = {
        "Category": ["Dairy", "Dairy", "Pantry", "Pantry", "Meat", "Produce"],
        "Item": ["Mjölk (1.5L)", "Prästost (1kg)", "Pasta (1kg)", "Kaffe (450g)", "Nötfärs (500g)", "Gurka (st)"],
        "Willys": [16.50, 99.00, 19.90, 52.00, 55.00, 11.90],
        "ICA": [17.90, 115.00, 22.50, 59.00, 62.00, 14.50],
        "Coop": [18.20, 119.00, 24.00, 62.00, 65.00, 15.00]
    }
    df_food = pd.DataFrame(food_data)
    
    # Search Bar
    search = st.text_input("🔍 Search for an item", "")
    if search:
        df_food = df_food[df_food["Item"].str.contains(search, case=False)]
    
    st.dataframe(df_food, use_container_width=True, hide_index=True)
