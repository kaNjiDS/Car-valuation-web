import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import kruskal, mannwhitneyu, normaltest, spearmanr
import scikit_posthocs as sp
from itertools import combinations
from components.custom_components import show_card
from components.styles import inject_styles

st.set_page_config(page_title="Inference Tests", page_icon="📉", layout="wide")

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

st.markdown('<h1>Statistical Inference Tests</h1>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("dataset/processed_data.csv")

df = load_data()

if 'engine_segment' not in df.columns:
    df['engine_segment'] = pd.cut(df['engine_cc'],
                                  bins=[0, 800, 1200, 1600, float('inf')],
                                  labels=['Micro', 'Compact', 'Mid-Range', 'Large'])

_L = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
          font_family="Inter", font=dict(size=14), margin=dict(l=10,r=10,t=40,b=10))

test_choice = st.selectbox(
    "Select the test you want to run",
    [
        "Price Distribution (Normality Test)",
        "Fuel Type (Kruskal-Wallis)",
        "Transmission/Gear (Mann-Whitney U + Post-hoc)",
        "Engine Segment (Kruskal + Post-hoc Dunn)",
        "Age (Spearman Correlation)",
        "Mileage (KM) (Spearman Correlation)",
        "Urban vs Non-Urban (Mann-Whitney U)",
        "Air Conditioning (Mann-Whitney U)",
        "Power Steering (Mann-Whitney U)",
        "Power Mirror (Mann-Whitney U)",
        "Power Window (Mann-Whitney U)"
    ]
)

if st.button(" Run Test", type="primary"):
    st.divider()

    # PRICE NORMALITY 
    if test_choice == "Price Distribution (Normality Test)":
        stat, p = normaltest(df['price_transformed'])
        st.subheader("Hypothesis")
        st.write("**H₀**: Price is normally distributed")
        st.write("**H₁**: Price is not normally distributed")

        st.subheader(" Price Distribution Histograms")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.histogram(df, x="price", nbins=50, title="Original Price Distribution",
                                labels={"price": "Price (LKR)"},
                                color_discrete_sequence=["#009929"], template="plotly_white")
            fig1.add_vline(x=df['price'].mean(), line_dash="dash", line_color="#d97706", annotation_text="Mean")
            fig1.update_layout(**_L)
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.histogram(df, x="price_transformed", nbins=50, title="Log-Transformed Price Distribution",
                                labels={"price_transformed": "log(Price)"},
                                color_discrete_sequence=["#1d4ed8"], template="plotly_white")
            fig2.add_vline(x=df['price_transformed'].mean(), line_dash="dash", line_color="#d97706", annotation_text="Mean")
            fig2.update_layout(**_L)
            st.plotly_chart(fig2, use_container_width=True)

        if p < 0.05:
            st.error("❌ Reject H₀ → Price is NOT normally distributed")
        else:
            st.success("✅ Fail to reject H₀ → Price appears normally distributed")

        result_df = pd.DataFrame({"Statistic": [round(stat, 4)], "p-value": [round(p, 4)],
                                   "Decision": ["Reject H₀" if p < 0.05 else "Fail to reject H₀"]})
        st.dataframe(result_df, use_container_width=True, hide_index=True)
        st.caption("**Interpretation**: The original price distribution is heavily right-skewed. After log transformation it becomes closer to normal. This is why we used GAM and Gradient Boosting instead of simple linear regression.")

    #  FUEL TYPE 
    elif test_choice == "Fuel Type (Kruskal-Wallis)":
        petrol   = df[df['fuel_type'] == 'Petrol']['price_transformed']
        diesel   = df[df['fuel_type'] == 'Diesel']['price_transformed']
        hybrid   = df[df['fuel_type'] == 'Hybrid']['price_transformed']
        electric = df[df['fuel_type'] == 'Electric']['price_transformed']
        stat, p  = kruskal(petrol, diesel, hybrid, electric)

        st.subheader("Hypothesis")
        st.write("**H₀**: Median prices are the same across all fuel types")
        st.write("**H₁**: Median prices differ across fuel types")

        if p < 0.05:
            st.error("❌ Reject H₀ → Median prices differ across fuel types")
        else:
            st.success("✅ Fail to reject H₀ → No significant difference")

        result_df = pd.DataFrame({"Statistic": [round(stat, 4)], "p-value": [round(p, 4)],
                                   "Decision": ["Reject H₀" if p < 0.05 else "Fail to reject H₀"]})
        st.dataframe(result_df, use_container_width=True, hide_index=True)
        st.caption("**Interpretation**: Fuel type significantly affects price. Hybrid and Electric vehicles tend to have higher prices than Petrol or Diesel.")

    #  TRANSMISSION/GEAR 
    elif test_choice == "Transmission/Gear (Mann-Whitney U + Post-hoc)":
        auto   = df[df['transmission'] == 'Automatic']['price_transformed']
        manual = df[df['transmission'] == 'Manual']['price_transformed']
        u_stat, p_val = mannwhitneyu(auto, manual, alternative='greater')

        st.subheader("Hypothesis")
        st.write("**H₀**: Median price of Automatic ≤ Median price of Manual")
        st.write("**H₁**: Median price of Automatic > Median price of Manual")

        if p_val < 0.05:
            st.error("❌ Reject H₀ → Automatic vehicles have significantly higher prices")
        else:
            st.success("✅ Fail to reject H₀ → No evidence Automatic > Manual")

        result_df = pd.DataFrame({"U Statistic": [u_stat], "p-value": [round(p_val, 4)],
                                   "Decision": ["Reject H₀" if p_val < 0.05 else "Fail to reject H₀"]})
        st.dataframe(result_df, use_container_width=True, hide_index=True)

        st.subheader("Post-hoc Summary Table")
        pairs = [("Automatic", "Manual")]
        summary = []
        alpha = 0.05
        m = len(pairs)
        for g1, g2 in pairs:
            p_adj = min(p_val * m, 1.0)
            sig = "Yes" if p_adj < alpha else "No"
            summary.append([f"{g1} vs {g2}", round(p_val, 4), round(p_adj, 4), sig])
        summary_df = pd.DataFrame(summary, columns=['Comparison', 'Raw p-value', 'Adjusted p-value', 'Significant?'])
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        st.caption("**Interpretation**: Automatic transmission adds a clear premium due to driving convenience.")

    #  ENGINE SEGMENT 
    elif test_choice == "Engine Segment (Kruskal + Post-hoc Dunn)":
        segments = df['engine_segment'].unique()
        groups   = [df[df['engine_segment'] == seg]['price_transformed'] for seg in segments]
        stat, p  = kruskal(*groups)

        st.subheader("Hypothesis")
        st.write("**H₀**: Median prices are the same across all engine segments")
        st.write("**H₁**: Median prices differ across engine segments")

        if p < 0.05:
            st.error("❌ Reject H₀ → Significant difference across engine segments")
        else:
            st.success("✅ Fail to reject H₀ → No significant difference")

        result_df = pd.DataFrame({"Statistic": [round(stat, 3)], "p-value": [round(p, 3)],
                                   "Decision": ["Reject H₀" if p < 0.05 else "Fail to reject H₀"]})
        st.dataframe(result_df, use_container_width=True, hide_index=True)

        if p < 0.05:
            posthoc = sp.posthoc_dunn(groups, p_adjust='bonferroni')
            posthoc.index   = segments
            posthoc.columns = segments
            pairs   = list(combinations(segments, 2))
            summary = []
            alpha   = 0.05
            for g1, g2 in pairs:
                p_val = posthoc.loc[g1, g2]
                sig   = "Yes" if p_val < alpha else "No"
                summary.append([f"{g1} vs {g2}", round(p_val, 4), sig])
            summary_df = pd.DataFrame(summary, columns=['Comparison', 'p-value', 'Significant?'])
            summary_df['p-value'] = pd.to_numeric(summary_df['p-value'], errors='coerce')
            st.subheader("Post-hoc Dunn Test (Bonferroni corrected)")
            st.dataframe(summary_df.style.format({"p-value": "{:.4f}"}))

        st.caption("**Interpretation**: Larger engine segments (Mid-Range & Large) have significantly higher prices than smaller ones.")

    #  OTHER VARIABLES 
    else:
        col_map = {
            "Age (Spearman Correlation)":           "Age",
            "Mileage (KM) (Spearman Correlation)":  "mileage",
            "Urban vs Non-Urban (Mann-Whitney U)":   "town_is_urban",
            "Air Conditioning (Mann-Whitney U)":     "air_condition",
            "Power Steering (Mann-Whitney U)":       "power_steering",
            "Power Mirror (Mann-Whitney U)":         "power_mirror",
            "Power Window (Mann-Whitney U)":         "power_window"
        }
        col = col_map.get(test_choice)

        if "Spearman" in test_choice:
            stat, p = spearmanr(df[col], df['price_transformed'])
            st.subheader("Hypothesis")
            st.write(f"**H₀**: No correlation between {test_choice.split(' (')[0]} and Price")
            st.write(f"**H₁**: There is a correlation")

            if p < 0.05:
                st.error("❌ Reject H₀ → Significant correlation")
            else:
                st.success("✅ Fail to reject H₀ → No significant correlation")

            result_df = pd.DataFrame({"Statistic": [round(stat, 4)], "p-value": [round(p, 4)],
                                       "Decision": ["Reject H₀" if p < 0.05 else "Fail to reject H₀"]})
            st.dataframe(result_df, use_container_width=True, hide_index=True)
            st.caption("**Interpretation**: This variable has a statistically significant relationship with price.")
        else:
            group1  = df[df[col] == 1]['price_transformed']
            group0  = df[df[col] == 0]['price_transformed']
            u_stat, p = mannwhitneyu(group1, group0, alternative='greater')

            st.subheader("Hypothesis")
            st.write("**H₀**: No difference in median price between groups")
            st.write("**H₁**: There is a difference")

            if p < 0.05:
                st.error("❌ Reject H₀ → Significant effect")
            else:
                st.success("✅ Fail to reject H₀ → No significant effect")

            result_df = pd.DataFrame({"U Statistic": [round(u_stat, 1)], "p-value": [round(p, 4)],
                                       "Decision": ["Reject H₀" if p < 0.05 else "Fail to reject H₀"]})
            st.dataframe(result_df, use_container_width=True, hide_index=True)
            st.caption("**Interpretation**: This feature significantly affects vehicle price.")

st.divider()

show_card(
    title=" Assumptions & Limitations",
    content=(
        "• All tests assume the data is a representative sample of the Sri Lankan secondary market<br>"
        "• Prices are asking prices, not actual sold prices<br>"
        "• Data only includes online listings (ikman.lk &amp; Riyasewana)<br>"
        "• Results may change if different filters are applied<br>"
        "• Some tests (e.g. Mann-Whitney) assume independent samples"
    )
)