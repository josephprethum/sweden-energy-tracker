import streamlit as st
import pandas as pd

# --- (Existing Energy Logic here) ---

tab_energy, tab_food = st.tabs(["⚡ Energy & Driving", "🛒 Grocery Tracker"])

with tab_energy:
    st.write("Your Energy code lives here...")

with tab_food:
    st.header("🛒 All Items Price Comparison")
    
    # 1. Expandable Master List of Items (The "Database")
    # You can keep adding items to this list!
    data = {
        "Category": ["Dairy", "Dairy", "Dairy", "Pantry", "Pantry", "Pantry", "Bakery", "Bakery", "Meat", "Meat", "Produce", "Produce"],
        "Item": ["Mjölk (1.5L)", "Smör (500g)", "Prästost (1kg)", "Pasta (1kg)", "Kaffe (450g)", "Havregryn (1.5kg)", "Frallor (4-pack)", "Knäckebröd (500g)", "Nötfärs (500g)", "Kycklingfilé (1kg)", "Gurka (st)", "Tomater (1kg)"],
        "Willys": [16.50, 48.90, 99.00, 19.90, 52.00, 14.90, 18.00, 12.50, 55.00, 115.00, 11.90, 24.90],
        "ICA": [17.90, 54.90, 115.00, 22.50, 59.00, 16.50, 22.00, 15.50, 62.00, 129.00, 14.50, 29.90],
        "Coop": [18.20, 56.00, 119.00, 24.00, 62.00, 17.00, 21.50, 16.00, 65.00, 135.00, 15.00, 32.00]
    }
    
    df_food = pd.DataFrame(data)

    # 2. The Search & Filter System
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search for an item (e.g. 'Milk' or 'Pasta')", "")
    with col2:
        category_filter = st.selectbox("Filter by Category", ["All"] + list(df_food["Category"].unique()))

    # Apply Filters
    filtered_df = df_food.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["Item"].str.contains(search_query, case=False)]
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]

    # 3. Display the Data
    st.write(f"Showing **{len(filtered_df)}** items:")
    
    # Highlight the cheapest store for each row
    def highlight_cheapest(s):
        # Only look at columns with store prices
        stores = ["Willys", "ICA", "Coop"]
        is_min = s[stores] == s[stores].min()
        return ['background-color: #ccffcc' if is_min.get(col, False) else '' for col in s.index]

    st.dataframe(
        filtered_df.style.apply(highlight_cheapest, axis=1),
        use_container_width=True,
        hide_index=True
    )

    st.caption("Green highlights indicate the cheapest store for that specific item.")
