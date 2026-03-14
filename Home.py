import streamlit as st

st.set_page_config(
    page_title="Sri Lankan Car Valuation",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Professional Modern CSS ──────────────────────────────────────────
st.markdown("""
<style>
div.stButton > button {
    background-color: #008000 !important;
    color: white !important;
    font-size: 18px !important;
    padding: 14px 32px !important;
    border-radius: 50px !important;
    font-weight: bold !important;
}

div.stButton > button:hover {
    background-color: #006400 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ─────────────────────────────────────────────────────────
st.sidebar.caption("s16829 • ST 3011 Project • Group 7")

# Overlay text on the banner (placed directly below the image for clean look)
col_center = st.columns([1, 4, 1])[1]
st.markdown(
   '<h1 style="text-align: center; font-size:35px;color:#008000;">Determinants of Vehicle Valuation in the Sri Lankan Online Secondary Market</h1>',
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)
# ── THREE CARDS (Fixed - Now renders properly) ───────────────────────
st.subheader("Study Context and Modeling Approach")
st.markdown("<br>", unsafe_allow_html=True)

colA, colB, colC = st.columns(3)

with colA:
    st.markdown("""
    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); text-align: center; min-height: 260px;">
        <h2 style="color: #006400; font-size: 28px;">📣</h2>
        <h4 style="color: #006400;">Data set contains</h4>
        <p style="color: #555;">web scraped car listings from ikman.lk and Riyasewana.com.</p>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown("""
    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); text-align: center; min-height: 260px;">
        <h2 style="color: #006400; font-size: 28px;">🚢</h2>
        <h4 style="color: #006400;">Vehicle sales</h4>
        <p style="color: #555;">during the 2020–2024 import baned time period</p>
    </div>
    """, unsafe_allow_html=True)

with colC:
    st.markdown("""
    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); text-align: center; min-height: 260px;">
        <h2 style="color: #006400; font-size: 28px;">🎯</h2>
        <h4 style="color: #006400;">Predict Prices</h4>
        <p style="color: #555;">Predictive modeling using Gradient Boosting.</p>
    </div>
    """, unsafe_allow_html=True)


# ── CENTERED TEXT + BUTTON SECTION ───────────────────────────────────
col_center = st.columns([1, 4, 1])[1]   # This centers everything

with col_center:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
    '<p class="hero-sub" style="text-align: center;font-size:28px; font-weight: bold;">Find out how much your vehicle is worth</p>',
    unsafe_allow_html=True
)
    st.markdown(
    '<p class="hero-sub" style="text-align: center;font-size:18px;">   See what you could get if you sold your car yourself, or get a guide price if you’re looking to buy a second hand vehicle.</p>',
    unsafe_allow_html=True
    )


    
    # Predict Button
    if st.button("Get your valuation now", key="valuation_btn", use_container_width=True):
        st.switch_page("pages/Price_Predictor.py")

st.divider()

# ── WHY PREDICTIVE MODELLING & GRADIENT BOOSTING? ────────────────────
st.subheader("Why Predictive Modelling?")
st.write("""
This study employs predictive modelling to estimate used vehicle prices in the Sri Lankan market during the import restriction period. Although vehicle imports have since resumed, market prices have not returned to pre-ban levels. This is largely due to the severe inflation Sri Lanka experienced during its economic crisis, which permanently reset the nominal price base across all goods. As a result, newly imported vehicles are being sold at prices that closely match the inflated values of used vehicles from the restriction period, making the data collected during the ban a valid and representative basis for price estimation in today's market.
""")

st.subheader("Why Gradient Boosting?")
st.write("""
Gradient Boosting was selected as the modelling method due to the structural complexity of this dataset, which contains over 1,500 unique vehicle model combinations. the majority having very few listings, making simpler linear or additive models unreliable. Gradient Boosting handles this effectively through target encoding, capturing non-linear relationships and interaction effects between features such as age, fuel type, and engine size. In terms of performance, the model achieved a Mean Absolute Percentage Error (MAPE) of **12.2%** and an R² of **0.928**. This represents a significant improvement over the GAM-based baseline, which recorded a MAPE of **27.5%** and an R² of **0.755**, confirming that Gradient Boosting is the most accurate and appropriate method for this study.
""")


st.caption("©s16829 • ST 3011 • Group 7 ")