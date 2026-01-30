import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("⚡ Energy & Driving Comparison")

# Your sidebar settings for this page
region = st.sidebar.selectbox("Region", ["SE1", "SE2", "SE3", "SE4"], index=2)
petrol_price = st.sidebar.number_input("E10 Petrol (kr/L)", value=15.04)

# Your fetching and table logic goes here...
# (Paste the energy table code we wrote earlier)