import streamlit as st
import pandas as pd

st.title("🛒 Grocery Price Tracker")

food_data = {
    "Item": ["Mjölk (1.5L)", "Smör (500g)", "Pasta (1kg)"],
    "Willys": [16.50, 48.90, 19.90],
    "ICA": [17.90, 54.90, 22.50]
}

df = pd.DataFrame(food_data)
search = st.text_input("Search items...")
if search:
    df = df[df["Item"].str.contains(search, case=False)]

st.dataframe(df, use_container_width=True)