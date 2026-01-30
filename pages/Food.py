import streamlit as st
import requests
import pandas as pd

st.title("🛒 Dynamic Food Search")

query = st.text_input("Search Swedish Products", "Mjölk")

if query:
    # 2026 Search Endpoint
    url = f"https://se.openfoodfacts.org/cgi/search.pl?search_terms={query}&action=process&json=1"
    
    try:
        res = requests.get(url, timeout=5).json()
        products = res.get('products', [])
        
        if products:
            results = []
            for p in products[:10]:
                results.append({
                    "Product": p.get('product_name', 'Unknown'),
                    "Brand": p.get('brands', 'Generic'),
                    "Nutrition": p.get('nutrition_grades', 'N/A').upper()
                })
            st.dataframe(pd.DataFrame(results), use_container_width=True)
        else:
            st.warning(f"No live results found for '{query}'. Try searching for 'Arla' or 'Bredbar'.")
            
    except:
        st.error("Food database is currently offline.")