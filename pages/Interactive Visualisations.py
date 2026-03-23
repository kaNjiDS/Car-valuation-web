import streamlit as st
import pandas as pd
import plotly.express as px
from components.custom_components import show_card, CHART_COLORS, FUEL_COLORS, TRANS_COLORS
from components.styles import inject_styles


st.set_page_config(page_title="Interactive Visualisations", page_icon="📈", layout="wide")

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

st.markdown('<h1>Interactive Visualisations</h1>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data
def load_data(): return pd.read_csv("dataset/processed_data.csv")
df = load_data()

_L = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_family="Inter", font=dict(size=15), title_font_size=17,
    legend_font_size=14,
    margin=dict(l=10,r=10,t=46,b=10)
)

#  SIDEBAR 
st.sidebar.markdown("""
<div style="font-family:Sora,sans-serif;font-size:1.1rem;font-weight:800;
color:#e8f9eb;padding:10px 0 6px;border-bottom:1px solid rgba(255,255,255,0.10);
margin-bottom:10px;">&#128269; Main Filters</div>
""", unsafe_allow_html=True)

selected_brands = st.sidebar.multiselect("Brand", options=sorted(df['brand'].unique()), default=[])
selected_fuel   = st.sidebar.multiselect("Fuel Type", options=sorted(df['fuel_type'].unique()), default=list(df['fuel_type'].unique()))
selected_trans  = st.sidebar.multiselect("Transmission", options=sorted(df['transmission'].unique()), default=list(df['transmission'].unique()))
min_year,max_year = st.sidebar.slider("Year of Manufacture",
    int(df['yom'].min()),int(df['yom'].max()),(int(df['yom'].min()),int(df['yom'].max())))
max_mileage = st.sidebar.slider("Maximum Mileage (KM)",
    0,int(df['mileage'].max()),int(df['mileage'].max()*0.7))

filtered = df.copy()
if selected_brands: filtered=filtered[filtered['brand'].isin(selected_brands)]
if selected_fuel:   filtered=filtered[filtered['fuel_type'].isin(selected_fuel)]
if selected_trans:  filtered=filtered[filtered['transmission'].isin(selected_trans)]
filtered=filtered[(filtered['yom']>=min_year)&(filtered['yom']<=max_year)]
filtered=filtered[filtered['mileage']<=max_mileage]
st.sidebar.success(f"Showing **{len(filtered):,}** cars")

# KPIs 
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Cars",  f"{len(filtered):,}")
c2.metric("Avg Price",   f"LKR {filtered['price'].mean():,.0f} Laks")
c3.metric("Avg Age",     f"{(2025-filtered['yom']).mean():.1f} yrs")
c4.metric("Avg Mileage", f"{filtered['mileage'].mean():,.0f} km")
c5.metric("Brands",      len(filtered['brand'].unique()))
st.divider()

#  CHART 1 & 2 
r1a, r1b = st.columns(2)

with r1a:
    st.subheader("Most Expensive Models")
    top10m = filtered.groupby(['brand','model'])['price'].mean().reset_index()
    top10m = top10m.sort_values('price',ascending=False).head(10)
    fig1 = px.bar(top10m, x="price", y="model", orientation='h', color="brand",
                  title="Top 10 Expensive Models", template="plotly_white",
                  color_discrete_sequence=CHART_COLORS)
    fig1.update_layout(
        yaxis={'categoryorder':'array','categoryarray':top10m['model'].tolist()[::-1]},
        **_L)
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("**Interpretation**: Luxury brands and high-end models (like Lexus, Mercedes) usually top the list.")

with r1b:
    st.subheader("Highest Average Price Brands")
    top10b = df.groupby('brand')['price'].mean().reset_index().sort_values('price',ascending=False).head(10)
    fig2 = px.bar(top10b, x="price", y="brand", orientation='h', color="price",
                  title="Top 10 Brands by Average Price (Global)", template="plotly_white",
                  color_continuous_scale=["#012208","#009929","#d97706","#fbbf24"])
    fig2.update_layout(
        yaxis={'categoryorder':'array','categoryarray':top10b['brand'].tolist()[::-1]},
        coloraxis_showscale=True, **_L)
    fig2.update_traces(marker_line_width=0)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("**Interpretation**: Toyota and luxury brands hold the highest average values.")

#  PRICE OVER TIME — bigger heading 
st.markdown("""
<div style="font-family:Sora,sans-serif;font-size:1.55rem;font-weight:700;
color:#015c18;border-bottom:2px solid #d8f5e0;padding-bottom:6px;margin:28px 0 14px;">
 Price Over Time Trend
</div>
<p style="font-family:Inter,sans-serif;font-size:17px;font-weight:600;
color:#0a1f0e;margin-bottom:12px;">
<strong>Select models to compare their price trend over years</strong>
<span style="color:#3d5e45;font-weight:500;"> (independent of sidebar)</span>
</p>
""", unsafe_allow_html=True)

model_counts = df.groupby('model').size().reset_index(name='count')
top15 = model_counts.nlargest(15,'count')['model'].tolist()
sel_models = st.multiselect("Top 15 Most Common Models", options=top15,
                             default=top15[:5] if top15 else [])
if sel_models:
    tf = df[df['model'].isin(sel_models)]
    tf = tf[(tf['yom']>=min_year)&(tf['yom']<=max_year)]
    tdf = tf.groupby(['yom','model'])['price'].mean().reset_index()
    fig_t = px.line(tdf, x="yom", y="price", color="model", markers=True,
                    title="Price Trend Over Years by Selected Models",
                    template="plotly_white", color_discrete_sequence=CHART_COLORS)
    fig_t.update_layout(height=480, **_L)
    fig_t.update_traces(line_width=2.8, marker_size=9)
    st.plotly_chart(fig_t, use_container_width=True)
    st.caption("**Interpretation**: Newer models hold higher value; older models depreciate faster. Sharp spikes post-2020 reflect the import-ban effect.")
else:
    st.info("👉 Select models above to see how their prices changed over time.")

#  FUEL & TRANSMISSION 
r2a,r2b = st.columns(2)

with r2a:
    st.subheader("Price by Fuel Type")
    fig3 = px.box(filtered, x="fuel_type", y="price", color="fuel_type",
                  title="Fuel Type vs Price (LKR Lakhs)", template="plotly_white",
                  color_discrete_map=FUEL_COLORS)
    fig3.update_layout(showlegend=True, **_L)
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("**Interpretation**: Hybrid and Electric vehicles generally have higher prices than Petrol or Diesel cars.")

with r2b:
    st.subheader("Price by Transmission")
    fig4 = px.box(filtered, x="transmission", y="price", color="transmission",
                  title="Automatic vs Manual Premium", template="plotly_white",
                  color_discrete_map=TRANS_COLORS)
    fig4.update_layout(showlegend=True, **_L)
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("**Interpretation**: Automatic cars are usually more expensive than Manual cars due to driving convenience.")

csv = filtered.to_csv(index=False).encode()
st.download_button("📥 Download Filtered Data", csv, "dashboard_data.csv", "text/csv")

show_card(" Assumptions & Limitations",
    "• Prices shown are asking prices (not final sold prices)<br>"
    "• Data comes only from online listings (ikman.lk &amp; Riyasewana)<br>"
    "• No brand-new cars are included (only secondary market)<br>"
    "• Results depend on the filters you apply<br>"
    "• Data is up to early 2025")