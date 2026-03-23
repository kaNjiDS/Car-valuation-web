import streamlit as st
import streamlit.components.v1 as components
from components.styles import inject_styles, sidebar_logo
from components.custom_components import hero_slideshow

st.set_page_config(page_title="Sri Lankan Car Valuation", page_icon="🚗",
                   layout="wide", initial_sidebar_state="expanded")

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
sidebar_logo()   # logo at bottom 

#  HERO SLIDESHOW 
hero_slideshow()
st.markdown("<br>", unsafe_allow_html=True)


#  THREE INFO CARDS 
st.subheader("Study Context and Modeling Approach")
st.markdown("<br>", unsafe_allow_html=True)


components.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
body{background:transparent;}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;width:100%;}
.card{
    background:#fff;
    border-radius:18px;
    padding:36px 26px 32px;
    box-shadow:0 6px 28px rgba(1,94,24,0.10);
    text-align:center;
    display:flex;flex-direction:column;align-items:center;
    /* equal height = stretch in grid */
}
.icon-ring{
    width:84px;height:84px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    margin:0 auto 18px;font-size:46px;
    box-shadow:0 4px 18px rgba(0,0,0,0.12);
    flex-shrink:0;
}
.card-title{
    font-family:Sora,sans-serif;font-size:1.15rem;font-weight:800;
    margin-bottom:12px;
}
.card-body{
    font-family:Inter,sans-serif;color:#374151;
    font-size:16px;line-height:1.78;
    flex:1;
}
</style>
<div class="grid">

  <!-- Card 1: Data Source — blue -->
  <div class="card" style="border-top:6px solid #1d4ed8;">
    <div class="icon-ring" style="background:#eff6ff;">&#128225;</div>
    <div class="card-title" style="color:#1d4ed8;">Data set contains</div>
    <p class="card-body">
      Web scraped car listings from <strong>ikman.lk</strong>
      and <strong>Riyasewana.com</strong> 
    </p>
  </div>

  <!-- Card 2: Study Period — amber -->
  <div class="card" style="border-top:6px solid #d97706;">
    <div class="icon-ring" style="background:#fffbeb;">&#128674;</div>
    <div class="card-title" style="color:#d97706;">Vehicle sales</div>
    <p class="card-body">
      During the <strong>2020–2024 import ban</strong> period. 
      An era of abnormal price appreciation driven by supply shortages
      and economic inflation.
    </p>
  </div>

  <!-- Card 3: Predictive Model — green -->
  <div class="card" style="border-top:6px solid #009929;">
    <div class="icon-ring" style="background:#f2fbf4;">&#127919;</div>
    <div class="card-title" style="color:#009929;">Predict Prices</div>
    <p class="card-body">
      Predictive modeling using <strong>Gradient Boosting</strong>
       achieving MAPE&nbsp;12.2% and R²&nbsp;0.928 on 9,676 real listings.
    </p>
  </div>

</div>
""", height=320, scrolling=False)

st.markdown("<br>", unsafe_allow_html=True)

#  LARGE CTA BOX 
components.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}body{background:transparent;}
.cta{background:linear-gradient(135deg,#012208 0%,#015c18 40%,#009929 80%,#00bf35 100%);
  border-radius:22px;padding:52px 60px;text-align:center;position:relative;overflow:hidden;
  box-shadow:0 14px 52px rgba(1,94,24,0.34);}
.cta-road{position:absolute;bottom:0;left:0;right:0;height:6px;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.20) 0 44px,transparent 44px 88px);}
.cta-car{position:absolute;right:40px;top:50%;transform:translateY(-50%);
  font-size:130px;opacity:0.06;line-height:1;}
.cta-tag{display:inline-block;background:rgba(255,255,255,.12);
  border:1px solid rgba(255,255,255,.25);border-radius:30px;
  padding:5px 18px;font-family:Inter,sans-serif;font-size:13px;font-weight:700;
  letter-spacing:1.5px;color:rgba(255,255,255,.60);text-transform:uppercase;margin-bottom:18px;}
.cta-title{font-family:Sora,sans-serif;font-size:2.5rem;font-weight:800;
  color:#fff;margin-bottom:14px;line-height:1.2;}
.cta-sub{font-family:Inter,sans-serif;font-size:17px;color:rgba(255,255,255,.80);
  max-width:560px;margin:0 auto 28px;line-height:1.78;}
.stats{display:flex;justify-content:center;gap:48px;}
.stat-val{font-family:Sora,sans-serif;font-size:2.2rem;font-weight:800;color:#6bffab;}
.stat-lbl{font-family:Inter,sans-serif;font-size:12px;font-weight:700;letter-spacing:1px;
  text-transform:uppercase;color:rgba(255,255,255,.50);margin-top:4px;}
</style>
<div class="cta">
  <div class="cta-road"></div>
  <div class="cta-car">&#128663;</div>
  <div class="cta-tag">Free Valuation Tool</div>
  <div class="cta-title">Find out how much your vehicle is worth</div>
  <p class="cta-sub">See what you could get if you sold your car yourself,
  or get a guide price if you're looking to buy a second hand vehicle.</p>
  <div class="stats">
    <div><div class="stat-val">9,676</div><div class="stat-lbl">Listings analysed</div></div>
    <div><div class="stat-val">0.928</div><div class="stat-lbl">Model R²</div></div>
    <div><div class="stat-val">12.2%</div><div class="stat-lbl">MAPE error</div></div>
  </div>
</div>
""", height=400, scrolling=False)

import streamlit as st

st.markdown("""
<style>
button[kind="secondary"] {
    color: #FFFFFF !important;
    background-color: #ff4b4b !important;
}
</style>
""", unsafe_allow_html=True)

_, col_btn, _ = st.columns([1, 2, 1])
with col_btn:
    if st.button("Get your valuation now", key="valuation_btn", use_container_width=True):
        st.switch_page("pages/Price_Predictor.py")

st.divider()

#  WHY SECTIONS 
st.subheader("Why Predictive Modelling?")
st.write("""
This study employs predictive modelling to estimate used vehicle prices in the Sri Lankan market during the import restriction period. Although vehicle imports have since resumed, market prices have not returned to pre-ban levels. This is largely due to the severe inflation Sri Lanka experienced during its economic crisis, which permanently reset the nominal price base across all goods. As a result, newly imported vehicles are being sold at prices that closely match the inflated values of used vehicles from the restriction period, making the data collected during the ban a valid and representative basis for price estimation in today's market.
""")

st.subheader("Why Gradient Boosting?")
st.write("""
Gradient Boosting was selected as the modelling method due to the structural complexity of this dataset, which contains over 1,500 unique vehicle model combinations. the majority having very few listings, making simpler linear or additive models unreliable. Gradient Boosting handles this effectively through target encoding, capturing non-linear relationships and interaction effects between features such as age, fuel type, and engine size. In terms of performance, the model achieved a Mean Absolute Percentage Error (MAPE) of **12.2%** and an R² of **0.928**. This represents a significant improvement over the GAM-based baseline, which recorded a MAPE of **27.5%** and an R² of **0.755**, confirming that Gradient Boosting is the most accurate and appropriate method for this study.
""")

st.caption("©s16829 • ST 3011 • Group 7")