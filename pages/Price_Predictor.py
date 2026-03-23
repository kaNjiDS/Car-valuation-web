import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import OrdinalEncoder
import warnings; warnings.filterwarnings('ignore')
from components.styles import inject_styles

st.set_page_config(page_title="Price Predictor", page_icon="🔮", layout="wide")

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

st.markdown('<h1>Realistic Car Price Predictor</h1>', unsafe_allow_html=True)
st.caption("Enter the details of the vehicle you want to estimate")
st.caption("The estimated vehicle value may slightly deviate from the actual value.")

@st.cache_data
def load_data(): return pd.read_csv("dataset/car_price_dataset.csv")
df = load_data()

@st.cache_resource
def train_model(df):
    gm=df['Price'].mean(); bm=df.groupby('Brand')['Price'].mean()
    ms=df.groupby(['Brand','Model'])['Price'].agg(['mean','count']).reset_index()
    ms['bm']=ms['Brand'].map(bm)
    ms['smoothed']=(ms['count']*ms['mean']+5*ms['bm'])/(ms['count']+5)
    mm=ms.set_index(['Brand','Model'])['smoothed']
    d=df.copy(); d['be']=d['Brand'].map(bm).fillna(gm)
    d['me']=pd.Series(d.set_index(['Brand','Model']).index.map(mm),index=d.index).fillna(d['be'])
    enc=OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1)
    cat=enc.fit_transform(d[['Gear','Fuel Type']])
    X=np.hstack([d[['YOM','Engine (cc)','Millage(KM)','be','me']].values,cat])
    y=np.log(d['Price'].values)
    m=HistGradientBoostingRegressor(max_iter=300,learning_rate=0.05,max_depth=6,min_samples_leaf=20,random_state=42)
    m.fit(X,y); return m,enc,bm,mm,gm

model,enc,brand_means,model_map,global_mean = train_model(df)

col1,col2 = st.columns(2)
with col1:
    st.subheader("Vehicle")
    brand=st.selectbox("Brand",sorted(df['Brand'].unique()))
    models_for_brand=sorted(df[df['Brand']==brand]['Model'].unique())
    vehicle_model=st.selectbox("Model",models_for_brand)
    years_for_model=sorted(df[(df['Brand']==brand)&(df['Model']==vehicle_model)]['YOM'].unique())
    year=st.selectbox("Year of Manufacture",years_for_model)
with col2:
    st.subheader("Key Specs")
    engine_options=sorted(df[(df['Brand']==brand)&(df['Model']==vehicle_model)]['Engine (cc)'].unique())
    engine_cc=st.selectbox("Engine Capacity (cc)",engine_options)
    trans_options=sorted(df[(df['Brand']==brand)&(df['Model']==vehicle_model)]['Gear'].unique())
    transmission=st.selectbox("Transmission",trans_options)

if st.button(" Predict Fair Price",type="primary",use_container_width=True):
    row=pd.DataFrame({'YOM':[year],'Engine (cc)':[engine_cc],'Millage(KM)':[50000],
        'be':[brand_means.get(brand,global_mean)],
        'me':[model_map.get((brand,vehicle_model),brand_means.get(brand,global_mean))]})
    cat=enc.transform([[transmission,df['Fuel Type'].mode()[0]]])
    X_in=np.hstack([row.values,cat]).reshape(1,-1)
    price=np.exp(model.predict(X_in)[0])

    st.markdown(
        '<div style="background:linear-gradient(135deg,#012208 0%,#015c18 45%,#009929 80%,#00bf35 100%);'
        'border-radius:22px;padding:48px 56px;margin:22px 0;'
        'box-shadow:0 14px 50px rgba(1,94,24,0.32);text-align:center;position:relative;overflow:hidden;">'
        '<div style="position:absolute;right:32px;top:50%;transform:translateY(-50%);'
        'font-size:110px;opacity:0.07;line-height:1;">&#128663;</div>'
        '<div style="font-family:Inter,sans-serif;font-size:12px;font-weight:800;'
        'letter-spacing:2.5px;color:rgba(255,255,255,0.52);text-transform:uppercase;margin-bottom:12px;">'
        'Estimated Fair Market Price</div>'
        '<div style="font-family:Sora,sans-serif;font-size:3.6rem;font-weight:800;'
        'color:#fff;line-height:1.1;margin-bottom:10px;">LKR '+f'{price:,.0f}'+' Laks</div>'
        '<div style="font-family:Inter,sans-serif;color:rgba(255,255,255,0.62);font-size:16px;">'
        +str(year)+' &nbsp;'+brand+' &nbsp;'+vehicle_model+'</div></div>',
        unsafe_allow_html=True
    )
    cl,ch = st.columns(2)
    cl.metric("Lower Estimate (−12%)", f"LKR {price*0.88:,.0f} Laks")
    ch.metric("Upper Estimate (+12%)", f"LKR {price*1.12:,.0f} Laks")
    st.caption("Interpretation: This prediction uses only the most important features for the gradient boost model.")