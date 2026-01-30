import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import io

# 1. Page Configuration
st.set_page_config(page_title="Sweden Energy Tracker 2026", layout="wide", page_icon="🇸🇪")

# 2. Sidebar Settings
with st.sidebar:
    st.header("⚙️ Dashboard Settings")
    region = st.selectbox("Electricity Region", ["SE1", "SE2", "SE3", "SE4"], index=2)
    selected_date = st.date_input("Select Report Date", datetime.now())
    
    st.divider()
    st.subheader("Vehicle Efficiency")
    # This input value will now be displayed in your new table column
    petrol_price = st.number_input("Current E10 Price (SEK/L)", value=15.04, step=0.10)
    cons_petrol = st.slider("Petrol (L/10km)", 0.4, 1.2, 0.65)
    cons_ev = st.slider("Electric (kWh/10km)", 1.0, 3.5, 2.0)

# 3. Data Fetching (Cached for Speed)
@st.cache_data(ttl=3600)
def get_live_data(date_obj, reg):
    date_str = date_obj.strftime('%Y/%m-%d')
    url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_str}_{reg}.json"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

# 4. Main UI Logic
st.title("🇸🇪 Sweden Energy & Driving Tracker")
st.info(f"Viewing data for **{selected_date.strftime('%Y-%m-%d')}** | Region: **{region}**")

raw_data = get_live_data(selected_date, region)

if raw_data:
    processed_list = []
    for i in range(0, len(raw_data), 4):  # Group by Hour
        item = raw_data[i]
        el_cost = item['SEK_per_kWh']
        
        # Driving Cost Calculations
        cost_mil_petrol = round(petrol_price * cons_petrol, 2)
        cost_mil_ev = round(el_cost * cons_ev, 2)
        savings = round(cost_mil_petrol - cost_mil_ev, 2)
        
        # Define each row of the table
        processed_list.append({
            "Date": selected_date.strftime('%Y-%m-%d'),
            "Time": item['time_start'][11:16],
            "El Price (kr/kWh)": round(el_cost, 2),
            "E10 Petrol (kr/L)": petrol_price,  # <--- YOUR NEW COLUMN
            "EV Cost/10km": f"{cost_mil_ev} kr",
            "Petrol Cost/10km": f"{cost_mil_petrol} kr",
            "Winner": "⚡ Electric" if savings > 0 else "⛽ Petrol",
            "Net Savings (kr)": savings
        })

    df = pd.DataFrame(processed_list)

    # 5. Display the Table
    st.subheader("Daily Comparison Report")
    
    # Styled table to highlight expensive/cheap hours
    st.dataframe(
        df.style.highlight_max(subset=['El Price (kr/kWh)'], color='#ffcccc')
                .highlight_min(subset=['El Price (kr/kWh)'], color='#ccffcc'),
        use_container_width=True
    )

    # 6. Export Feature
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download This Table as CSV", data=csv, file_name=f"energy_report_{selected_date}.csv")

else:
    st.error("No data available for this date/region. Please select another.")
