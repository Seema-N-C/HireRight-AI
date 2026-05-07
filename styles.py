# ============================================================
# styles.py — All custom CSS / st.markdown injections
# ============================================================

import streamlit as st


def inject_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
    .stApp { background: #0f0c29; background-image: radial-gradient(ellipse at top, #1a1040 0%, #0f0c29 60%); }
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { background: rgba(255,255,255,0.02) !important; border-right: 1px solid rgba(255,255,255,0.05) !important; }
    [data-testid="stSidebar"] * { color: #aaa !important; }
    h1, h2, h3 { background: linear-gradient(135deg, #667eea, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stButton > button { background: linear-gradient(135deg, #667eea, #764ba2); color: white !important; border: none; border-radius: 12px; padding: 12px 28px; font-size: 15px; font-weight: 700; width: 100%; transition: all 0.3s; }
    .stButton > button:hover { background: linear-gradient(135deg, #f093fb, #667eea); transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.4); }
    .glass-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 20px; margin: 10px 0; transition: transform 0.2s, border-color 0.2s; }
    .glass-card:hover { transform: translateY(-3px); border-color: rgba(102,126,234,0.4); }
    .shortlisted  { border-left: 4px solid #4ade80 !important; }
    .under-review { border-left: 4px solid #fbbf24 !important; }
    .rejected     { border-left: 4px solid #f87171 !important; }
    .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
    .badge-green  { background: rgba(74,222,128,0.15); color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
    .badge-orange { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
    .badge-red    { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
    .skill-tag          { display: inline-block; background: rgba(102,126,234,0.1); color: #a78bfa; padding: 3px 10px; border-radius: 20px; font-size: 12px; margin: 2px; border: 1px solid rgba(102,126,234,0.2); }
    .skill-tag-expected { display: inline-block; background: rgba(74,222,128,0.1);  color: #4ade80; padding: 3px 10px; border-radius: 20px; font-size: 12px; margin: 2px; border: 1px solid rgba(74,222,128,0.2); }
    .skill-tag-missing  { display: inline-block; background: rgba(248,113,113,0.1); color: #f87171; padding: 3px 10px; border-radius: 20px; font-size: 12px; margin: 2px; border: 1px solid rgba(248,113,113,0.2); }
    .section-header { background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2)); border: 1px solid rgba(102,126,234,0.3); color: #a78bfa !important; padding: 12px 20px; border-radius: 12px; font-size: 16px; font-weight: 700; margin: 16px 0 12px 0; }
    .stTextArea label { color: #667eea !important; font-weight: 700 !important; font-size: 14px !important; }
    .stSelectbox label { color: #667eea !important; font-weight: 700 !important; font-size: 14px !important; }
    .stSelectbox > div > div { background: #0f0c29 !important; border: 1px solid rgba(167,139,250,0.4) !important; border-radius: 12px !important; color: #a78bfa !important; }
    .stSelectbox > div > div > div { color: #a78bfa !important; }
    .stSelectbox svg { fill: #a78bfa !important; }
    .stTextArea textarea { background: #0f0c29 !important; border: 1.5px solid rgba(102,126,234,0.5) !important; border-radius: 12px !important; color: #f5c518 !important; font-size: 14px !important; }
    .stTextArea textarea::placeholder { color: rgba(245,197,24,0.35) !important; }
    [data-testid="stFileUploader"] { background: rgba(10,8,40,0.6) !important; border: 2px dashed rgba(102,126,234,0.55) !important; border-radius: 14px !important; padding: 10px !important; }
    [data-testid="stFileUploader"] * { color: #a78bfa !important; }
    [data-testid="stFileUploaderDropzoneInput"] + div button,
    [data-testid="stBaseButton-secondary"] { background: linear-gradient(135deg, #667eea, #764ba2) !important; color: white !important; border: none !important; border-radius: 12px !important; font-weight: 700 !important; }
    [data-testid="stFileUploaderDropzone"] { background: transparent !important; }
    #MainMenu { visibility: hidden; } footer { visibility: hidden; }
    [data-testid='stExpander'] { border-radius: 12px !important; margin-bottom: 4px !important; }
    [data-testid='stExpander'] summary { font-weight: 700 !important; font-size: 14px !important; }
    [data-testid='stExpander']:nth-of-type(5n+1) summary p, [data-testid='stExpander']:nth-of-type(5n+1) summary { color: #667eea !important; }
    [data-testid='stExpander']:nth-of-type(5n+1) { border: 1px solid rgba(102,126,234,0.35) !important; }
    [data-testid='stExpander']:nth-of-type(5n+2) summary p, [data-testid='stExpander']:nth-of-type(5n+2) summary { color: #fbbf24 !important; }
    [data-testid='stExpander']:nth-of-type(5n+2) { border: 1px solid rgba(251,191,36,0.35) !important; }
    [data-testid='stExpander']:nth-of-type(5n+3) summary p, [data-testid='stExpander']:nth-of-type(5n+3) summary { color: #f093fb !important; }
    [data-testid='stExpander']:nth-of-type(5n+3) { border: 1px solid rgba(240,147,251,0.35) !important; }
    [data-testid='stExpander']:nth-of-type(5n+4) summary p, [data-testid='stExpander']:nth-of-type(5n+4) summary { color: #60a5fa !important; }
    [data-testid='stExpander']:nth-of-type(5n+4) { border: 1px solid rgba(96,165,250,0.35) !important; }
    [data-testid='stExpander']:nth-of-type(5n+5) summary p, [data-testid='stExpander']:nth-of-type(5n+5) summary { color: #4ade80 !important; }
    [data-testid='stExpander']:nth-of-type(5n+5) { border: 1px solid rgba(74,222,128,0.35) !important; }
    .stat-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(102,126,234,0.15); border-radius: 16px; padding: 20px; text-align: center; transition: all 0.3s; }
    .stat-card:hover { border-color: rgba(102,126,234,0.5); box-shadow: 0 0 20px rgba(102,126,234,0.15); }
    .stat-val { font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #667eea, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stat-sub { font-size: 11px; color: #444; margin-top: 2px; }
    .parse-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(102,126,234,0.25); border-left: 5px solid #667eea; border-radius: 16px; padding: 24px; margin: 12px 0; }
    .role-suggest-card { background: rgba(102,126,234,0.07); border: 1px solid rgba(102,126,234,0.25); border-radius: 12px; padding: 14px 18px; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)
