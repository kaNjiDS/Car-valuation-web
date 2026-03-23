import streamlit as st
import pandas as pd
from components.custom_components import show_card
from components.styles import inject_styles

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")

st.markdown("""
<style>
    /* 1. Load the official Google Material font properly */
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

    /* 2. Target EVERY possible collapse arrow in Streamlit (covers both "sides"/states) */
    button[data-testid="collapsedControl"] span,
    [data-testid="stSidebarCollapseButton"] span,
    button[data-testid="stSidebarCollapseButton"] span,
    .st-emotion-cache-1f3w5w0 span,
    .st-emotion-cache-1f3w5w0 button span,
    button span {
        font-family: 'Material Symbols Outlined' !important;
        font-size: 15px !important;
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
        color: #FFFFF !important;
        display: inline-block !important;
    }

    /* 3. Extra safety for any remaining raw text */
    [data-testid="collapsedControl"]::before,
    button[data-testid="collapsedControl"]::before {
        content: 'keyboard_double_arrow_right' !important;
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

inject_styles()

st.markdown('<h1>Data Explorer</h1>', unsafe_allow_html=True)
st.caption("9,676 Real Sri Lankan Used Car Listings • Filter & Explore")

@st.cache_data
def load_data():
    return pd.read_csv("dataset/car_price_dataset.csv")
df = load_data()

st.subheader("🔍 Filter the Dataset")
col1,col2,col3,col4 = st.columns(4)
with col1:
    selected_brands = st.multiselect("Brand", options=sorted(df['Brand'].unique()), default=["TOYOTA"])
with col2:
    avail = sorted(df[df['Brand'].isin(selected_brands)]['Model'].unique()) if selected_brands else []
    selected_models = st.multiselect("Model", options=avail)
with col3:
    selected_fuel = st.multiselect("Fuel Type", options=sorted(df['Fuel Type'].unique()), default=list(df['Fuel Type'].unique()))
with col4:
    selected_gear = st.multiselect("Transmission", options=sorted(df['Gear'].unique()), default=list(df['Gear'].unique()))

min_year,max_year = st.slider("Year of Manufacture",
    int(df['YOM'].min()), int(df['YOM'].max()),
    (int(df['YOM'].min()), int(df['YOM'].max())))

filtered = df.copy()
if selected_brands: filtered = filtered[filtered['Brand'].isin(selected_brands)]
if selected_models: filtered = filtered[filtered['Model'].isin(selected_models)]
filtered = filtered[(filtered['YOM']>=min_year)&(filtered['YOM']<=max_year)]
if selected_fuel: filtered = filtered[filtered['Fuel Type'].isin(selected_fuel)]
if selected_gear: filtered = filtered[filtered['Gear'].isin(selected_gear)]

st.success(f"**Showing {len(filtered):,} cars**")
st.divider()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Cars",      f"{len(filtered):,}")
c2.metric("Average Price",   f"LKR {filtered['Price'].mean():,.0f} Laks")
c3.metric("Average Age",     f"{(2025-filtered['YOM']).mean():.1f} yrs")
c4.metric("Average Mileage", f"{filtered['Millage(KM)'].mean():,.0f} km")

st.subheader("Filtered Data Table")
st.dataframe(filtered.style.format({"Price":"LKR {:,.0f}","Millage(KM)":"{:,.0f} km"}),
             use_container_width=True, height=500)
st.download_button("📥 Download Filtered Data as CSV",
                   filtered.to_csv(index=False).encode(),
                   "filtered_cars.csv","text/csv")
st.divider()