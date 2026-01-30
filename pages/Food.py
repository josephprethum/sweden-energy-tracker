import streamlit as st
import requests
import pandas as pd

st.title("🛒 Dynamic Food Search")

search_term = st.text_input("Search for a product (e.g., 'Mjölk' or 'Ost')")

if search_term:
    # Open Food Facts API for Sweden
    url = f"https://se.openfoodfacts.org/cgi/search.pl?search_terms={search_term}&action=process&json=1"
    
    try:
        response = requests.get(url).json()
        products = response.get('products', [])
        
        if products:
            food_list = []
            for p in products[:15]: # Limit to top 15 results
                food_list.append({
                    "Brand": p.get('brands', 'Unknown'),
                    "Product": p.get('product_name', 'Unknown'),
                    "Qty": p.get('quantity', 'N/A'),
                    "Nutrition Grade": p.get('nutrition_grades', 'N/A').upper()
                })
            
            st.dataframe(pd.DataFrame(food_list), use_container_width=True)
        else:
            st.write("No products found.")
    except:
        st.error("Could not connect to Food Database.")