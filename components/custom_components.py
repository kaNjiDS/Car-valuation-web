import streamlit as st
import plotly.express as px

def show_card(title, content, color="#e6f3e6"):
    st.markdown(f"""
    <div style="background-color:{color}; padding:15px; border-radius:8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <h4 style="color:#006400;">{title}</h4>
    <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def interactive_scatter(df, x, y, color, title, size=None):
    # Automatically use only columns that actually exist for hover
    possible_hover = ['model', 'town', 'brand']
    actual_hover = [col for col in possible_hover if col in df.columns]
    
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        hover_data=actual_hover if actual_hover else None,
        title=title
    )
    st.plotly_chart(fig, width='stretch')  # Fixed deprecation

def loading_spinner(message, code):
    with st.spinner(message):
        exec(code)  # For simulations; use cautiously