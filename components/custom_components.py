import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go

#  Colour palettes for charts

CHART_COLORS   = ["#009929","#d97706","#1d4ed8","#be123c","#6d28d9","#0891b2","#065f46","#92400e"]
CHART_GRADIENT = ["#012208","#015c18","#009929","#d97706","#fbbf24"]   # for continuous scales

FUEL_COLORS = {
    "Petrol":   "#d97706",   # amber
    "Diesel":   "#1d4ed8",   # blue
    "Hybrid":   "#009929",   # green
    "Electric": "#6d28d9",   # violet
}
TRANS_COLORS = {
    "Automatic": "#009929",
    "Manual":    "#d97706",
}


def show_card(title: str, content: str, color: str = "#dff7e7"):
    safe = content.replace("</div>","").replace("<div>","")
    st.markdown(
        '<div style="background:linear-gradient(135deg,'+color+' 0%,#fff 100%);'
        'border:1.5px solid #b0d8ba;border-left:7px solid #009929;'
        'border-radius:16px;padding:24px 30px;margin:18px 0;'
        'box-shadow:0 2px 16px rgba(1,94,24,0.10);font-family:Inter,sans-serif;">'
        '<div style="font-family:Sora,sans-serif;font-size:1.1rem;font-weight:800;'
        'color:#015c18;margin-bottom:12px;">'+title+'</div>'
        '<div style="font-size:15.5px;color:#1a3d22;line-height:1.85;">'+safe+'</div>'
        '</div>',
        unsafe_allow_html=True
    )


def verdict_card(reject: bool, h0: str, h1: str):
    """
    GREEN card = Reject H0 (significant)   — like original st.success
    RED   card = Fail to reject H0          — like original st.error
    """
    if reject:
        bg      = "#fff1f2"
        bdr     = "#be123c"
        pill    = "#be123c"
        icon    = "&#10007;"
        msg     = "Reject H&#8320; &mdash; Statistically Significant"
    else:
        bg      = "#e8f9ef"
        bdr     = "#009929"
        pill    = "#009929"
        icon    = "&#10003;"
        msg     = "Do Not Reject H&#8320; &mdash; Not Significant"

    html = (
        '<div style="background:' + bg + ';border:1.5px solid ' + bdr + ';'
        'border-left:8px solid ' + bdr + ';border-radius:16px;'
        'padding:24px 30px;margin:18px 0;font-family:Inter,sans-serif;">'

        '<div style="font-family:Sora,sans-serif;font-size:1.05rem;font-weight:800;'
        'color:#012208;margin-bottom:14px;">Hypothesis &amp; Verdict</div>'

        '<p style="font-size:16px;color:#1a1a1a;margin:0 0 8px;">'
        '<strong>H&#8320;:</strong> ' + h0 + '</p>'

        '<p style="font-size:16px;color:#1a1a1a;margin:0 0 22px;">'
        '<strong>H&#8321;:</strong> ' + h1 + '</p>'

        '<div style="display:inline-flex;align-items:center;gap:9px;'
        'background:' + pill + ';color:#fff;border-radius:30px;'
        'padding:10px 28px;font-size:15px;font-weight:800;letter-spacing:0.2px;">'
        + icon + ' &nbsp;' + msg +
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def interactive_scatter(df, x, y, color, title, size=None):
    possible_hover = ['model', 'town', 'brand']
    actual_hover = [c for c in possible_hover if c in df.columns]
    fig = px.scatter(df, x=x, y=y, color=color, size=size,
                     hover_data=actual_hover or None, title=title,
                     template="plotly_white",
                     color_discrete_sequence=CHART_COLORS)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font_family="Inter")
    st.plotly_chart(fig, use_container_width=True)


def hero_slideshow():
    """Auto-rotating slideshow via components.html so JS works."""
    html = """<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:transparent;overflow:hidden;}
.ss{position:relative;width:100%;height:360px;border-radius:22px;overflow:hidden;
    box-shadow:0 14px 52px rgba(1,94,24,0.30);}
.sl{position:absolute;inset:0;background-size:cover;background-position:center;
    opacity:0;transition:opacity 1.4s ease;}
.sl.on{opacity:1;}
.ov{position:absolute;inset:0;
    background:linear-gradient(115deg,rgba(1,34,8,.90) 0%,rgba(1,92,24,.68) 38%,rgba(0,153,41,.22) 100%);}
.road{position:absolute;bottom:0;left:0;right:0;height:6px;
      background:repeating-linear-gradient(90deg,rgba(255,255,255,.22) 0 44px,transparent 44px 88px);z-index:3;}
.cnt{position:absolute;bottom:0;left:0;right:0;padding:32px 48px 42px;z-index:2;}
.eye{font-family:Inter,sans-serif;font-size:11px;font-weight:800;letter-spacing:3px;
     color:rgba(255,255,255,.52);text-transform:uppercase;margin-bottom:12px;}
.ttl{font-family:Sora,sans-serif;font-size:2.2rem;font-weight:800;color:#fff;line-height:1.18;margin-bottom:12px;}
.sub{font-family:Inter,sans-serif;font-size:15.5px;color:rgba(255,255,255,.82);max-width:580px;line-height:1.75;}
.sub strong{color:#6bffab;}
.badge{display:inline-flex;align-items:center;gap:8px;margin-top:18px;
       background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);
       border-radius:40px;padding:7px 20px;
       font-family:Inter,sans-serif;font-size:13px;font-weight:700;color:rgba(255,255,255,.88);}
.badge span{color:#6bffab;font-weight:900;}
.dots{position:absolute;bottom:20px;right:28px;z-index:4;display:flex;gap:9px;align-items:center;}
.dot{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.32);
     cursor:pointer;border:none;outline:none;transition:all .3s;}
.dot.on{background:#fff;transform:scale(1.4);}
</style>
</head>
<body>
<div class="ss">
  <div class="sl on" style="background-image:url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1400&q=80')">
    <div class="ov"></div>
    <div class="cnt">
      <div class="eye">Sri Lanka &bull; Secondary Vehicle Market &bull; 2020–2025</div>
      <div class="ttl">Determinants of Vehicle Valuation<br>in the Sri Lankan Secondary Market</div>
      <p class="sub">A data-driven study of <strong>9,676 listings</strong> from ikman.lk &amp; Riyasewana.com  uncovering what really drives used car prices.</p>
      
    </div>
  </div>
  <div class="sl" style="background-image:url('https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=1400&q=80')">
    <div class="ov"></div>
    <div class="cnt">
      <div class="eye">Gradient Boosting Model &bull; MAPE 12.2%</div>
      <div class="ttl">Predict Your Vehicle's<br>Fair Market Price</div>
      <p class="sub">Our model achieves R² of <strong>0.928</strong>  capturing brand equity, age, engine size &amp; fuel type effects on Sri Lankan prices.</p>
    </div>
  </div>
  <div class="sl" style="background-image:url('https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=1400&q=80')">
    <div class="ov"></div>
    <div class="cnt">
      <div class="eye">Import Ban Era &bull; 2020–2024</div>
      <div class="ttl">Market Insights During<br>Sri Lanka's Import Restriction</div>
      <p class="sub">Prices never returned to pre-ban levels. Explore how <strong>economic crisis &amp; supply shocks</strong> permanently reshaped the market.</p>
    </div>
  </div>
  <div class="sl" style="background-image:url('https://images.unsplash.com/photo-1485291571150-772bcfc10da5?w=1400&q=80')">
    <div class="ov"></div>
    <div class="cnt">
      <div class="eye">Explore &bull; Analyse &bull; Predict</div>
      <div class="ttl">Interactive Dashboards<br>for Every User</div>
      <p class="sub">Filter 9,676 real listings, run hypothesis tests, visualise price trends, and predict fair prices  built for <strong>buyers &amp; sellers</strong>.</p>
    </div>
  </div>
  <div class="road"></div>
  <div class="dots">
    <button class="dot on" onclick="go(0)"></button>
    <button class="dot" onclick="go(1)"></button>
    <button class="dot" onclick="go(2)"></button>
    <button class="dot" onclick="go(3)"></button>
  </div>
</div>
<script>
var c=0,n=4;
function go(i){
  document.querySelectorAll('.sl').forEach(function(s,j){s.classList.toggle('on',j===i);});
  document.querySelectorAll('.dot').forEach(function(d,j){d.classList.toggle('on',j===i);});
  c=i;
}
setInterval(function(){go((c+1)%n);},5000);
</script>
</body>
</html>"""
    components.html(html, height=370, scrolling=False)