import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import OrdinalEncoder
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Price Predictor", page_icon="🔮", layout="wide")

st.title("🔮 Realistic Car Price Predictor")
st.caption("Enter the details of the vehicle you want to estimate")
st.caption("The estimated vehicle value may be slightly deviate from the actual value.")

# ── Load Data ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/car_price_dataset.csv")
    return df

df = load_data()

# ── Train Model (same powerful model) ─────────────────────────────────
@st.cache_resource
def train_model(df):
    global_mean = df['Price'].mean()  # using original Price for simplicity
    brand_means = df.groupby('Brand')['Price'].mean()
    
    model_stats = df.groupby(['Brand', 'Model'])['Price'].agg(['mean', 'count']).reset_index()
    model_stats['brand_mean'] = model_stats['Brand'].map(brand_means)
    model_stats['smoothed'] = (
        model_stats['count'] * model_stats['mean'] + 5 * model_stats['brand_mean']
    ) / (model_stats['count'] + 5)
    
    model_map = model_stats.set_index(['Brand', 'Model'])['smoothed']
    
    df = df.copy()
    df['brand_encoded'] = df['Brand'].map(brand_means).fillna(global_mean)
    mapped = df.set_index(['Brand', 'Model']).index.map(model_map)
    df['model_encoded'] = pd.Series(mapped, index=df.index).fillna(df['brand_encoded'])
    
    FEAT_COLS = ['YOM', 'Engine (cc)', 'Millage(KM)', 'brand_encoded', 'model_encoded']
    
    enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    cat_enc = enc.fit_transform(df[['Gear', 'Fuel Type']])
    
    X = np.hstack([df[FEAT_COLS].values, cat_enc])
    y = np.log(df['Price'].values)   # log price for better training
    
    model = HistGradientBoostingRegressor(
        max_iter=300, learning_rate=0.05, max_depth=6,
        min_samples_leaf=20, random_state=42
    )
    model.fit(X, y)
    
    return model, enc, brand_means, model_map, global_mean

model, enc, brand_means, model_map, global_mean = train_model(df)

# ── Dynamic Inputs (only real values from your dataset) ───────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Vehicle")
    brand = st.selectbox("Brand", sorted(df['Brand'].unique()))
    
    # Filter models for selected brand
    models_for_brand = sorted(df[df['Brand'] == brand]['Model'].unique())
    vehicle_model = st.selectbox("Model", models_for_brand)
    
    # Filter years for selected brand + model
    years_for_model = sorted(df[(df['Brand'] == brand) & (df['Model'] == vehicle_model)]['YOM'].unique())
    year = st.selectbox("Year of Manufacture", years_for_model)

with col2:
    st.subheader("Key Specs")
    # Filter engine CC for selected brand + model
    engine_options = sorted(df[(df['Brand'] == brand) & (df['Model'] == vehicle_model)]['Engine (cc)'].unique())
    engine_cc = st.selectbox("Engine Capacity (cc)", engine_options)
    
    # Transmission filtered
    trans_options = sorted(df[(df['Brand'] == brand) & (df['Model'] == vehicle_model)]['Gear'].unique())
    transmission = st.selectbox("Transmission", trans_options)

# ── Predict ──────────────────────────────────────────────────────────
if st.button("🔮 Predict Fair Price", type="primary", use_container_width=True):
    # Prepare input
    input_row = pd.DataFrame({
        'YOM': [year],
        'Engine (cc)': [engine_cc],
        'Millage(KM)': [50000],  # default average
        'brand_encoded': [brand_means.get(brand, global_mean)],
        'model_encoded': [model_map.get((brand, vehicle_model), brand_means.get(brand, global_mean))]
    })
    
    cat = enc.transform([[transmission, df['Fuel Type'].mode()[0]]])
    X_input = np.hstack([input_row.values, cat]).reshape(1, -1)
    
    log_pred = model.predict(X_input)[0]
    price = np.exp(log_pred)
    
    st.success(f"**Estimated Fair Price: LKR {price:,.0f} Laks**")
    
    col_low, col_high = st.columns(2)
    col_low.metric("Lower Estimate", f"LKR {price*0.88:,.0f} Laks")
    col_high.metric("Upper Estimate", f"LKR {price*1.12:,.0f} Laks")

    st.caption("Interpretation: This prediction uses only the most important features for the gradient boost model.")
