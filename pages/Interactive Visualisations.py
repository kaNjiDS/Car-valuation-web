import streamlit as st
import pandas as pd
import plotly.express as px
from components.custom_components import show_card

st.set_page_config(page_title="Interactive Visualisations", page_icon="📈", layout="wide")

st.title("📈 Interactive Visualisations")
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("dataset/processed_data.csv")

df = load_data()

# ── SIDEBAR FILTERS (controls 2×2 grid & KPIs only) ─────────────────
st.sidebar.header("🔍 Main Filters")
selected_brands = st.sidebar.multiselect("Brand", options=sorted(df['brand'].unique()), default=[])
selected_fuel = st.sidebar.multiselect("Fuel Type", options=sorted(df['fuel_type'].unique()), default=df['fuel_type'].unique())
selected_trans = st.sidebar.multiselect("Transmission", options=sorted(df['transmission'].unique()), default=df['transmission'].unique())

min_year, max_year = st.sidebar.slider("Year of Manufacture", 
                                       int(df['yom'].min()), int(df['yom'].max()), 
                                       (int(df['yom'].min()), int(df['yom'].max())))

max_mileage = st.sidebar.slider("Maximum Mileage (KM)", 
                                0, int(df['mileage'].max()), int(df['mileage'].max() * 0.7))

# Apply sidebar filters for 2×2 grid & KPIs
filtered = df.copy()
if selected_brands:
    filtered = filtered[filtered['brand'].isin(selected_brands)]
if selected_fuel:
    filtered = filtered[filtered['fuel_type'].isin(selected_fuel)]
if selected_trans:
    filtered = filtered[filtered['transmission'].isin(selected_trans)]
filtered = filtered[(filtered['yom'] >= min_year) & (filtered['yom'] <= max_year)]
filtered = filtered[filtered['mileage'] <= max_mileage]

st.sidebar.success(f"Showing **{len(filtered):,}** cars")

# ── KPI CARDS ────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Cars", f"{len(filtered):,}")
c2.metric("Avg Price", f"LKR {filtered['price'].mean():,.0f} Laks")
c3.metric("Avg Age", f"{(2025 - filtered['yom']).mean():.1f} years")
c4.metric("Avg Mileage", f"{filtered['mileage'].mean():,.0f} km")
c5.metric("Brands Shown", len(filtered['brand'].unique()))

st.divider()

# ── 2×2 GRID WITH INTERPRETATIONS ────────────────────────────────────
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Most Expensive Models")
    top10_models = filtered.groupby(['brand', 'model'])['price'].mean().reset_index()
    top10_models = top10_models.sort_values('price', ascending=False).head(10)
    fig1 = px.bar(top10_models, x="price", y="model", orientation='h', color="brand", title="Top 10 Expensive Models")
    fig1.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': top10_models['model'].tolist()[::-1]})
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("**Interpretation**: These are the most expensive models in selected filters. Luxury brands and specific high-end models (like Lexus, Mercedes) usually top the list.")

with row1_col2:
    st.subheader("Highest Average Price Brands")
    top10_brands = df.groupby('brand')['price'].mean().reset_index()   # Global (ignores sidebar)
    top10_brands = top10_brands.sort_values('price', ascending=False).head(10)
    fig2 = px.bar(top10_brands, x="price", y="brand", orientation='h', 
                  title="Top 10 Brands by Average Price (Global)", color="price")
    fig2.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': top10_brands['brand'].tolist()[::-1]})
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("**Interpretation**: This shows which brands hold the highest average value in the entire Sri Lankan market. Toyota and luxury brands dominate.")

# ── PRICE OVER TIME TREND ────────────────────────────────────────────
st.subheader("📈 Price Over Time Trend")
st.write("**Select models to compare their price trend over years** (independent of sidebar)")

model_counts = df.groupby('model').size().reset_index(name='count')
top15_models = model_counts.nlargest(15, 'count')['model'].tolist()

selected_time_models = st.multiselect(
    "Top 15 Most Common Models",
    options=top15_models,
    default=top15_models[:5] if top15_models else []
)

if selected_time_models:
    time_filtered = df[df['model'].isin(selected_time_models)]
    time_filtered = time_filtered[(time_filtered['yom'] >= min_year) & (time_filtered['yom'] <= max_year)]
    
    time_df = time_filtered.groupby(['yom', 'model'])['price'].mean().reset_index()
    fig_time = px.line(time_df, x="yom", y="price", color="model", markers=True,
                       title="Price Trend Over Years by Selected Models")
    fig_time.update_layout(height=500)
    st.plotly_chart(fig_time, use_container_width=True)
    st.caption("**Interpretation**: This line shows how prices of selected models have changed over the years. Newer models generally hold higher value, while older models depreciate faster.")
else:
    st.info("👉 Select models above to see how their prices changed over time.")

# ── BOTTOM CHARTS WITH INTERPRETATIONS ───────────────────────────────
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.subheader("Price by Fuel Type")
    fig3 = px.box(filtered, x="fuel_type", y="price", color="fuel_type", title="Fuel Type Impact")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("**Interpretation**: Hybrid and Electric vehicles generally have higher prices than Petrol or Diesel cars.")

with row2_col2:
    st.subheader("Price by Transmission")
    fig4 = px.box(filtered, x="transmission", y="price", color="transmission", title="Automatic Premium")
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("**Interpretation**: Automatic cars are usually more expensive than Manual cars due to driving convenience.")

# Download
csv = filtered.to_csv(index=False).encode()
st.download_button("📥 Download Filtered Data", csv, "dashboard_data.csv", "text/csv")

# ── ASSUMPTIONS & LIMITATIONS ────────────────────────────────────────
show_card(
    title="📌 Assumptions & Limitations",
    content="""
    • Prices shown are asking prices (not final sold prices)<br>
    • Data comes only from online listings (ikman.lk & Riyasewana)<br>
    • No brand-new cars are included (only secondary market)<br>
    • Results depend on the filters you apply<br>
    • Data is up to early 2025
    """
)
