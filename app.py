import streamlit as st

# ── Colour palette (edit these to restyle the whole app) ──────────────────────
CLR_BG           = "#0D0D12"
CLR_SURFACE      = "#14141F"
CLR_SURFACE2     = "#1C1C2E"
CLR_BORDER       = "#2A2A40"
CLR_PURPLE       = "#7C3AED"
CLR_PURPLE_LIGHT = "#A78BFA"
CLR_PURPLE_DIM   = "#4C1D95"
CLR_GREEN        = "#10B981"
CLR_GREEN_LIGHT  = "#6EE7B7"
CLR_GREEN_DIM    = "#064E3B"
CLR_TEXT         = "#E2E8F0"
CLR_TEXT_MUTED   = "#94A3B8"
CLR_ACCENT       = "#F0FDF4"

st.set_page_config(
    page_title="KaryoScan — Chromosomal Abnormality Detection",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

GLOBAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {{
    background-color: {CLR_BG};
    color: {CLR_TEXT};
    font-family: 'DM Sans', sans-serif;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {CLR_SURFACE};
    border-right: 1px solid {CLR_BORDER};
}}

/* Radio group label ("NAVIGATE" heading) */
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
    color: {CLR_TEXT_MUTED} !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    font-family: 'Space Mono', monospace !important;
}}

/* Every radio option label — target all possible Streamlit class patterns */
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [data-testid="stRadioLabel"],
[data-testid="stSidebar"] .stRadio div[data-testid] p,
[data-testid="stSidebar"] [role="radio"] + * p,
[data-testid="stSidebar"] [class*="stRadio"] label p,
[data-testid="stSidebar"] [class*="radio"] label span,
[data-testid="stSidebar"] [class*="radio"] p {{
    color: {CLR_TEXT} !important;
    font-size: 0.92rem !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}}

/* Selected radio option */
[data-testid="stSidebar"] [aria-checked="true"] + * p,
[data-testid="stSidebar"] [aria-checked="true"] ~ * p {{
    color: {CLR_PURPLE_LIGHT} !important;
    font-weight: 600 !important;
}}

/* Page-wide block container */
.block-container {{
    padding: 2.5rem 3rem 4rem 3rem;
    max-width: 1200px;
}}

/* Headers */
h1, h2, h3 {{
    font-family: 'Space Mono', monospace;
    letter-spacing: -0.02em;
}}

/* Gradient headline */
.grad-title {{
    background: linear-gradient(135deg, {CLR_PURPLE_LIGHT} 0%, {CLR_GREEN_LIGHT} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}}
.grad-title-sm {{
    background: linear-gradient(135deg, {CLR_PURPLE_LIGHT} 0%, {CLR_GREEN_LIGHT} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    line-height: 1.2;
}}

/* Cards */
.kcard {{
    background: {CLR_SURFACE};
    border: 1px solid {CLR_BORDER};
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
}}
.kcard-accent {{
    background: linear-gradient(135deg, {CLR_PURPLE_DIM}55 0%, {CLR_GREEN_DIM}55 100%);
    border: 1px solid {CLR_PURPLE};
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
}}

/* Pill badges */
.pill-normal {{
    display:inline-block;
    background:{CLR_GREEN_DIM};
    color:{CLR_GREEN_LIGHT};
    border:1px solid {CLR_GREEN};
    border-radius:999px;
    padding:2px 12px;
    font-size:0.78rem;
    font-family:'Space Mono',monospace;
    letter-spacing:0.06em;
}}
.pill-ambig {{
    display:inline-block;
    background:{CLR_PURPLE_DIM};
    color:{CLR_PURPLE_LIGHT};
    border:1px solid {CLR_PURPLE};
    border-radius:999px;
    padding:2px 12px;
    font-size:0.78rem;
    font-family:'Space Mono',monospace;
    letter-spacing:0.06em;
}}

/* Stat block */
.stat-box {{
    background:{CLR_SURFACE2};
    border:1px solid {CLR_BORDER};
    border-radius:10px;
    padding:1rem 1.25rem;
    text-align:center;
}}
.stat-num {{
    font-family:'Space Mono',monospace;
    font-size:2rem;
    color:{CLR_GREEN_LIGHT};
    line-height:1;
}}
.stat-label {{
    font-size:0.75rem;
    color:{CLR_TEXT_MUTED};
    letter-spacing:0.1em;
    text-transform:uppercase;
    margin-top:0.25rem;
}}

/* Step pipeline */
.step-row {{
    display:flex;
    align-items:flex-start;
    gap:1rem;
    margin-bottom:1rem;
}}
.step-num {{
    flex-shrink:0;
    width:32px;height:32px;
    border-radius:50%;
    background:linear-gradient(135deg, {CLR_PURPLE} 0%, {CLR_GREEN} 100%);
    display:flex;align-items:center;justify-content:center;
    font-family:'Space Mono',monospace;
    font-size:0.82rem;
    color:#fff;
    font-weight:700;
}}
.step-body {{
    flex:1;
    padding-top:4px;
}}
.step-title {{
    font-weight:600;
    color:{CLR_TEXT};
    font-size:0.95rem;
}}
.step-desc {{
    color:{CLR_TEXT_MUTED};
    font-size:0.85rem;
    margin-top:2px;
}}

/* Limitation item */
.limit-item {{
    display:flex;gap:0.75rem;align-items:flex-start;
    background:{CLR_SURFACE2};
    border-left:3px solid {CLR_PURPLE};
    border-radius:0 8px 8px 0;
    padding:0.75rem 1rem;
    margin-bottom:0.6rem;
}}
.limit-icon {{font-size:1rem;flex-shrink:0;}}
.limit-text {{font-size:0.88rem;color:{CLR_TEXT_MUTED};line-height:1.5;}}

/* Divider */
.kdivider {{
    border: none;
    border-top: 1px solid {CLR_BORDER};
    margin: 2rem 0;
}}

/* File uploader tweak */
[data-testid="stFileUploader"] {{
    background:{CLR_SURFACE2};
    border:1px dashed {CLR_PURPLE};
    border-radius:10px;
    padding:1rem;
}}

/* Slider accent */
[data-testid="stSlider"] .st-emotion-cache-1g6gooi {{
    background:{CLR_PURPLE} !important;
}}

/* Muted text helper */
.muted {{color:{CLR_TEXT_MUTED};font-size:0.88rem;}}
.mono {{font-family:'Space Mono',monospace;}}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:1.25rem 0 1rem 0;'>
        <div style='font-family:Space Mono,monospace;font-size:1.1rem;
                    background:linear-gradient(135deg,{CLR_PURPLE_LIGHT},{CLR_GREEN_LIGHT});
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    font-weight:700;letter-spacing:-0.02em;'>
            🧬 KaryoScan
        </div>
        <div style='font-size:0.72rem;color:{CLR_TEXT_MUTED};
                    letter-spacing:0.12em;text-transform:uppercase;margin-top:2px;'>
            Chromosomal Abnormality Detection
        </div>
    </div>
    <hr style='border:none;border-top:1px solid {CLR_BORDER};margin:0 0 1rem 0;'/>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATE",
        ["🏠  Home", "⚙️  How It Works", "📊  Model Performance", "🔬  Let's Detect"],
        label_visibility="visible",
    )
    st.markdown(f"""
    <hr style='border:none;border-top:1px solid {CLR_BORDER};margin:1.5rem 0 1rem 0;'/>
    <div style='font-size:0.72rem;color:{CLR_TEXT_MUTED};line-height:1.6;'>
        <b style='color:{CLR_PURPLE_LIGHT};'>Stack</b><br>
        YOLO26 · DTW · Streamlit<br><br>
        <b style='color:{CLR_PURPLE_LIGHT};'>Classifier</b><br>
        Denver System · Rule-based
    </div>
    """, unsafe_allow_html=True)

page_key = page.split("  ")[-1]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if page_key == "Home":
    from pages.home import render
    render(CLR_PURPLE, CLR_PURPLE_LIGHT, CLR_GREEN, CLR_GREEN_LIGHT,
           CLR_TEXT, CLR_TEXT_MUTED, CLR_SURFACE, CLR_SURFACE2, CLR_BORDER,
           CLR_PURPLE_DIM, CLR_GREEN_DIM)

elif page_key == "How It Works":
    from pages.how_it_works import render
    render(CLR_PURPLE, CLR_PURPLE_LIGHT, CLR_GREEN, CLR_GREEN_LIGHT,
           CLR_TEXT, CLR_TEXT_MUTED, CLR_SURFACE, CLR_SURFACE2, CLR_BORDER,
           CLR_PURPLE_DIM, CLR_GREEN_DIM)

elif page_key == "Model Performance":
    from pages.model_performance import render
    render(CLR_PURPLE, CLR_PURPLE_LIGHT, CLR_GREEN, CLR_GREEN_LIGHT,
           CLR_TEXT, CLR_TEXT_MUTED, CLR_SURFACE, CLR_SURFACE2, CLR_BORDER,
           CLR_PURPLE_DIM, CLR_GREEN_DIM)

elif page_key == "Let's Detect":
    from pages.detect import render
    render(CLR_PURPLE, CLR_PURPLE_LIGHT, CLR_GREEN, CLR_GREEN_LIGHT,
           CLR_TEXT, CLR_TEXT_MUTED, CLR_SURFACE, CLR_SURFACE2, CLR_BORDER,
           CLR_PURPLE_DIM, CLR_GREEN_DIM)