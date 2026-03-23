import streamlit as st


def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Sora:wght@700;800&display=swap');

    :root {
        --g900:#012208; --g800:#023d10; --g700:#015c18;
        --g600:#027a20; --g500:#009929; --g400:#00bf35;
        --g100:#dff7e7; --g50:#f2fbf4;
        --amber:#d97706; --amber-lt:#fbbf24;
        --blue:#1d4ed8;  --violet:#6d28d9;
        --surf:#ffffff;  --bg:#eef6ef;
        --bdr:#b0d8ba;   --txt:#0a1f0e; --mut:#3d5e45;
        --r:14px; --sh:0 2px 16px rgba(1,94,24,0.11);
        --shlg:0 10px 40px rgba(1,94,24,0.19);
    }

    /* ── Base ── */
    html, body, .stApp {
        font-family: 'Inter', sans-serif !important;
        background: var(--bg) !important;
        color: var(--txt) !important;
        font-size: 17px !important;
        line-height: 1.78 !important;
    }
    .block-container {
        max-width: 1220px !important;
        padding: 1.8rem 2.5rem 7rem !important;
    }

    /* ── Headings ── */
    h1 {
        font-family:'Sora',sans-serif !important;
        font-size:2.6rem !important; font-weight:800 !important;
        color:var(--g800) !important; line-height:1.18 !important;
        border-bottom:3px solid #b8f0c8 !important; padding-bottom:10px !important;
    }
    h2 {
        font-family:'Sora',sans-serif !important;
        font-size:1.75rem !important; font-weight:700 !important;
        color:var(--g700) !important;
        border-bottom:2px solid #d8f5e0 !important; padding-bottom:6px !important;
    }
    h3 {
        font-family:'Inter',sans-serif !important;
        font-size:1.25rem !important; font-weight:700 !important;
        color:var(--g700) !important;
    }
    p { font-size:17px !important; line-height:1.82 !important; }

    /* subheader / st.subheader */
    [data-testid="stHeading"] h2 {
        font-size:1.55rem !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(175deg, var(--g900) 0%, #024012 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] * {
        color:#c0e8c8 !important;
        font-family:'Inter',sans-serif !important;
        font-size:15.5px !important;
    }
    [data-testid="stSidebarNav"] a {
        border-radius:8px !important; padding:7px 14px !important;
        transition:background .2s !important;
    }
    [data-testid="stSidebarNav"] a:hover { background:rgba(0,153,41,0.20) !important; }
    [data-testid="stSidebarNav"] [aria-selected="true"] {
        background:rgba(0,153,41,0.28) !important;
        border-left:3px solid var(--g400) !important;
    }
    [data-testid="stSidebarNav"] span {
        font-size:15.5px !important; font-weight:600 !important; color:#d8f0de !important;
    }
    [data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {
        color:#e8f9eb !important; font-family:'Sora',sans-serif !important; border:none !important;
    }
    [data-testid="stSidebar"] [data-testid="stSuccess"] {
        background:rgba(0,153,41,0.18) !important;
        border:1px solid rgba(0,153,41,0.38) !important;
        border-radius:8px; color:#c0e8c8 !important; font-size:15px !important;
    }

    /* ── Metric cards  ── */
    [data-testid="stMetric"] {
        background:var(--surf) !important;
        border:1.5px solid var(--bdr) !important;
        border-radius:16px !important;
        padding:22px 18px !important;
        box-shadow:var(--sh) !important;
        position:relative; overflow:visible !important;
        transition:transform .2s,box-shadow .2s;
    }
    [data-testid="stMetric"]:hover { transform:translateY(-3px); box-shadow:var(--shlg) !important; }
    [data-testid="stMetric"]::after {
        content:''; position:absolute; bottom:0; left:0; right:0; height:4px;
        border-radius:0 0 16px 16px;
        background:linear-gradient(90deg,var(--g500),var(--amber-lt));
    }
    [data-testid="stMetricLabel"] {
        font-family:'Inter',sans-serif !important;
        font-size:12px !important; font-weight:800 !important;
        text-transform:uppercase; letter-spacing:1px;
        color:var(--mut) !important; white-space:normal !important;
    }
    [data-testid="stMetricValue"] {
        font-family:'Sora',sans-serif !important;
        font-size:1.8rem !important; font-weight:800 !important;
        color:var(--g700) !important;
        white-space:normal !important; overflow:visible !important;
        text-overflow:clip !important; line-height:1.2 !important;
        word-break:break-word !important;
    }

    /* ── Buttons ── */
    div.stButton > button {
        background:linear-gradient(135deg,var(--g600) 0%,var(--g900) 100%) !important;
        color:#fff !important; font-family:'Inter',sans-serif !important;
        font-size:24px !important; font-weight:800 !important;
        padding:15px 44px !important; border-radius:50px !important; border:none !important;
        box-shadow:0 5px 22px rgba(1,94,24,0.38) !important;
        transition:all .22s ease !important; letter-spacing:.3px !important;
    }
    div.stButton > button:hover {
        background:linear-gradient(135deg,var(--g500) 0%,var(--g700) 100%) !important;
        box-shadow:0 8px 32px rgba(0,153,41,0.52) !important; transform:translateY(-2px) !important;
    }
    div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00c853 0%, #006400 100%) !important;
    color: white !important;
    font-size: 22px !important;
    padding: 16px !important;
    border-radius: 50px !important;
    font-weight: bold !important;
    box-shadow: 0 6px 20px rgba(0,200,83,0.4) !important;
    }

    div.stButton > button[kind="primary"]:hover {
    transform: scale(1.05);
    
    }
                
    div.stDownloadButton > button {
        background:var(--g50) !important; color:var(--g700) !important;
        border:2px solid var(--g600) !important; border-radius:50px !important;
        font-weight:800 !important; font-size:16px !important;
    }

    /* ── Inputs ── */
    [data-baseweb="select"] > div,[data-baseweb="input"] > div {
        border-radius:10px !important; border-color:var(--bdr) !important;
        background:var(--surf) !important;
        font-family:'Inter',sans-serif !important; font-size:16px !important;
    }
    [data-baseweb="select"] > div:focus-within {
        border-color:var(--g600) !important;
        box-shadow:0 0 0 3px rgba(0,122,32,0.16) !important;
    }
    .stMultiSelect [data-baseweb="tag"] {
        background:var(--g600) !important; border-radius:20px !important;
        color:#fff !important; font-weight:700 !important; font-size:14px !important;
    }
    label,.stSelectbox label,.stMultiSelect label,.stSlider label {
        font-size:15px !important; font-weight:700 !important; color:var(--g800) !important;
    }

    /* ── Slider ── */
    [data-testid="stSlider"] > div > div > div > div {
        background:linear-gradient(90deg,var(--g600),var(--amber-lt)) !important;
    }
    [data-testid="stSlider"] p { font-size:15px !important; }

    /* ── DataFrame ── */
    [data-testid="stDataFrame"] iframe {
        border-radius:14px !important; border:1.5px solid var(--bdr) !important;
        box-shadow:var(--sh) !important;
    }

    /* ── Alerts ── */
    [data-testid="stSuccess"] {
        background:var(--g50) !important; border-left:5px solid var(--g500) !important;
        border-radius:12px !important; font-size:17px !important; font-weight:700 !important;
    }
    [data-testid="stInfo"] {
        border-left:5px solid var(--blue) !important; border-radius:12px !important;
        font-size:16px !important;
    }
    [data-testid="stWarning"] {
        background:#fffbeb !important; border-left:5px solid var(--amber) !important;
        border-radius:12px !important; font-size:16px !important;
    }
    [data-testid="stError"] {
        border-left:5px solid #be123c !important; border-radius:12px !important;
    }

    /* ── Divider ── */
    hr { border:none !important; height:2px !important;
         background:linear-gradient(90deg,transparent,var(--bdr),transparent) !important;
         margin:2.2rem 0 !important; }

    /* ── Caption ── */
    .stCaption,caption {
        color:var(--mut) !important; font-size:14.5px !important;
        font-family:'Inter',sans-serif !important;
    }

    /* ── Selectbox popup text ── */
    [data-baseweb="select"] * { font-size:15.5px !important; }

    /* ── Write / paragraph text ── */
    .stMarkdown p, .stText p { font-size:17px !important; line-height:1.82 !important; }
    </style>
    """, unsafe_allow_html=True)


def sidebar_logo():
    
    st.sidebar.markdown("""
    <div style="position:fixed;bottom:0;left:0;width:278px;
                background:linear-gradient(0deg,#012208 60%,transparent 100%);
                padding:22px 0 26px;text-align:center;z-index:100;pointer-events:none;">
      <div style="font-size:38px;line-height:1;margin-bottom:6px;">&#128663;</div>
      <div style="font-family:Sora,sans-serif;font-size:0.95rem;font-weight:800;
                  color:#e0f5e4;letter-spacing:.3px;">CarValuation.lk</div>
      <div style="font-family:Inter,sans-serif;font-size:10px;font-weight:700;
                  letter-spacing:1.5px;color:rgba(255,255,255,0.32);
                  text-transform:uppercase;margin-top:3px;">Sri Lankan Market</div>
      <div style="font-family:Inter,sans-serif;font-size:11px;
                  color:rgba(255,255,255,0.25);margin-top:5px;">s16829 · ST 3011 · Group 7</div>
    </div>
    """, unsafe_allow_html=True)