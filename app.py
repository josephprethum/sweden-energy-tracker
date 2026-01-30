import streamlit as st

st.set_page_config(page_title="Sweden Smart Hub", page_icon="🇸🇪")

st.title("Välkommen! 🇸🇪")
st.write("Welcome to your 2026 Swedish Life Dashboard.")

st.info("Use the sidebar on the left to switch between Energy tracking and Grocery prices.")

# Quick summary metrics could go here
st.metric("Stockholm (SE3) Price Today", "1.12 SEK/kWh")