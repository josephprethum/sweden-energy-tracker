import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import io

# 1. Page Configuration
st.set_page_config(page_title="Sweden Energy Tracker 2026", layout="wide", page_icon="🇸🇪")

# 2. Sidebar Settings & Date Selection
with st.sidebar:
    st.header("⚙️ Dashboard Settings")
    region = st.selectbox("Electricity Region", ["SE1", "SE2", "SE3", "SE4"], index=2, help="SE3 is Stockholm/Central Sweden")
    
    # User can pick any date (API supports recent past and today)
    selected_date = st.date_input("Select Report Date", datetime.now())
    
    st.divider()
    st.subheader("Vehicle Efficiency")
    petrol_price = st.number_input("Petrol Price (SEK/L)", value=15.04, step=0.10)
    cons_petrol = st.slider("Petrol (L/10km)", 0.4, 1.2, 0.65)
    cons_ev = st.slider("Electric (kWh/10km)", 1.0, 3.5, 2.0)

# 3. Data Fetching Logic
@st.cache_data(ttl=3600)  # Caches for 1 hour to stay fast
def get_live_data(date_obj, reg):
    date_str = date_obj.strftime('%Y/%m-%d')
    url = f"https://www.elprisetjustnu.se/api/v1/prices/{date_str}_{reg}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        return None

# 4. Main UI Logic
st.title("🇸🇪 Sweden Energy & Driving Tracker")
st.info(f"Viewing data for **{selected_date.strftime('%Y-%m-%d')}** in region **{region}**")

raw_data = get_live_data(selected_date, region)

if raw_data:
    processed_list = []
    for i in range(0, len(raw_data), 4):  # Step by 4 for hourly view (15-min intervals)
        item = raw_data[i]
        el_cost = item['SEK_per_kWh']
        
        # Calculation per 10km (1 mil)
        cost_mil_petrol = round(petrol_price * cons_petrol, 2)
        cost_mil_ev = round(el_cost * cons_ev, 2)
        savings = round(cost_mil_petrol - cost_mil_ev, 2)
        
        processed_list.append({
            "Date": selected_date.strftime('%Y-%m-%d'),
            "Time": item['time_start'][11:16],
            "El Price (kr/kWh)": round(el_cost, 2),
            "EV Cost/10km": cost_mil_ev,
            "Petrol Cost/10km": cost_mil_petrol,
            "Winner": "⚡ Electric" if savings > 0 else "⛽ Petrol",
            "Savings (kr)": savings
        })

    df = pd.DataFrame(processed_list)

    # 5. Key Metrics
    m1, m2, m3 = st.columns(3)
    avg_el = df["El Price (kr/kWh)"].mean()
    m1.metric("Avg Electricity", f"{avg_el:.2f} SEK")
    m2.metric("Avg EV mil-cost", f"{df['EV Cost/10km'].mean():.2f} SEK")
    m3.metric("Petrol mil-cost", f"{cost_mil_petrol} SEK")

    # 6. The Table
    st.subheader("Detailed Hourly Comparison")
    
    # Highlight the best and worst hours
    styled_df = df.style.highlight_max(subset=['El Price (kr/kWh)'], color='#ffcccc') \
                        .highlight_min(subset=['El Price (kr/kWh)'], color='#ccffcc')
    
    st.dataframe(styled_df, use_container_width=True)

    # 7. Export Feature
    st.divider()
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download This Report as CSV",
        data=csv,
        file_name=f"sweden_energy_{selected_date}.csv",
        mime="text/csv",
    )

else:
    st.error("Could not fetch data for this date. The API might not have released prices yet or the date is too far in the past.")