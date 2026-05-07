# ============================================================
# app.py — Entry point: sidebar routing + page rendering
# ============================================================

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import team

st.set_page_config(
    page_title="HireRight AI — Futuristic",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Must be imported AFTER set_page_config
from styles import inject_styles
import home, upload, dashboard, candidate, report,team

inject_styles()

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px 0;'>
        <div style='font-size:52px; filter:drop-shadow(0 0 20px #667eea);'>🤖</div>
        <div style='font-size:22px; font-weight:800; background:linear-gradient(135deg,#667eea,#f093fb);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>HIRE RIGHT AI</div>
        <div style='font-size:10px; color:#555; margin-top:4px; letter-spacing:2px; text-transform:uppercase;'>
            Intelligence That Hires Right</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["🏠  Home", "📤  Upload & Analyze", "📊  Dashboard", "👤  Candidate Detail", "📄  Report","👥 Team"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px; color:#333; text-align:center;'>"
        "9 Modules • RoBERTa-based NLP<br/>Cosine Similarity + LR Classifier</div>",
        unsafe_allow_html=True)

# ── PAGE ROUTING ──────────────────────────────────────────────
if   page == "🏠  Home":               home.render()
elif page == "📤  Upload & Analyze":   upload.render()
elif page == "📊  Dashboard":          dashboard.render()
elif page == "👤  Candidate Detail":   candidate.render()
elif page == "📄  Report":             report.render()
elif "Team" in page:                   team.render()