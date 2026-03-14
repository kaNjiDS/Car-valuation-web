import streamlit as st
import pandas as pd
from components.custom_components import show_card

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")

st.title("📊 Data Explorer")
st.caption("9,676 Real Sri Lankan Used Car Listings • Filter & Explore")

# ── Load Data ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("dataset/car_price_dataset.csv")

df = load_data()

# ── TOP DROPDOWN CHECKBOX FILTERS ────────────────────────────────────
st.subheader("🔍 Filter the Dataset")

col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_brands = st.multiselect(
        "Brand",
        options=sorted(df['Brand'].unique()),
        default=["TOYOTA"]
    )

with col2:
    available_models = sorted(df[df['Brand'].isin(selected_brands)]['Model'].unique()) if selected_brands else []
    selected_models = st.multiselect(
        "Model",
        options=available_models
    )

with col3:
    selected_fuel = st.multiselect(
        "Fuel Type",
        options=sorted(df['Fuel Type'].unique()),
        default=df['Fuel Type'].unique()
    )

with col4:
    selected_gear = st.multiselect(
        "Transmission",
        options=sorted(df['Gear'].unique()),
        default=df['Gear'].unique()
    )

# Year range
min_year, max_year = st.slider(
    "Year of Manufacture",
    int(df['YOM'].min()), 
    int(df['YOM'].max()), 
    (int(df['YOM'].min()), int(df['YOM'].max()))
)

# Apply filters
filtered = df.copy()
if selected_brands:
    filtered = filtered[filtered['Brand'].isin(selected_brands)]
if selected_models:
    filtered = filtered[filtered['Model'].isin(selected_models)]
filtered = filtered[(filtered['YOM'] >= min_year) & (filtered['YOM'] <= max_year)]
if selected_fuel:
    filtered = filtered[filtered['Fuel Type'].isin(selected_fuel)]
if selected_gear:
    filtered = filtered[filtered['Gear'].isin(selected_gear)]

st.success(f"**Showing {len(filtered):,} cars**")

st.divider()

# ── Summary Cards ────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Cars", f"{len(filtered):,}")
c2.metric("Average Price", f"LKR {filtered['Price'].mean():,.0f} Laks")
c3.metric("Average Age", f"{(2025 - filtered['YOM']).mean():.1f} years")
c4.metric("Average Mileage", f"{filtered['Millage(KM)'].mean():,.0f} km")

# ── Data Table + Download ────────────────────────────────────────────
st.subheader("Filtered Data Table")
st.dataframe(
    filtered.style.format({
        "Price": "LKR {:,.0f}",
        "Millage(KM)": "{:,.0f} km"
    }),
    use_container_width=True,
    height=500
)

# Download button
csv = filtered.to_csv(index=False).encode()
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_cars.csv",
    mime="text/csv"
)

st.divider()