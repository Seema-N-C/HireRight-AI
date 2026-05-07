# ============================================================
# pages/home.py — Home / landing page
# ============================================================

import streamlit as st


def render():
    st.markdown("""
    <div style='
        background: linear-gradient(160deg, rgba(102,126,234,0.18) 0%, rgba(118,75,162,0.22) 50%, rgba(240,147,251,0.12) 100%);
        border: 1px solid rgba(102,126,234,0.3);
        border-radius: 24px;
        padding: 70px 60px 60px 60px;
        text-align: center;
        margin-bottom: 36px;
        position: relative;
        box-shadow: 0 0 60px rgba(102,126,234,0.12), inset 0 1px 0 rgba(255,255,255,0.05);
    '>
        <div style='position:absolute;top:-40px;left:50%;transform:translateX(-50%);
                    width:220px;height:220px;background:radial-gradient(circle,rgba(102,126,234,0.18) 0%,transparent 70%);
                    border-radius:50%;pointer-events:none;'></div>
        <div style='font-size:90px; margin-bottom:20px; line-height:1;
                    filter:drop-shadow(0 0 30px #667eea) drop-shadow(0 0 60px rgba(102,126,234,0.5)); opacity:1;'>🤖</div>
        <h1 style='font-size:62px;font-weight:900;margin:0 0 10px 0;letter-spacing:-1px;
                   background:linear-gradient(135deg,#a78bfa 0%,#667eea 40%,#f093fb 100%);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                   filter:drop-shadow(0 0 20px rgba(102,126,234,0.4));line-height:1.1;'>HIRE RIGHT AI</h1>
        <h2 style='font-size:20px;font-weight:500;margin:0 0 18px 0;
                   color:#c4b5fd !important;-webkit-text-fill-color:#c4b5fd !important;letter-spacing:0.5px;'>
            AI Powered Intelligent Recruitment &amp; Candidate Analytics System</h2>
        <div style='width:80px;height:2px;background:linear-gradient(90deg,transparent,#667eea,#f093fb,transparent);
                    margin:0 auto 18px auto;border-radius:2px;'></div>
        <p style='color:rgba(255,255,255,0.25);font-size:12px;margin:0;letter-spacing:1.5px;text-transform:uppercase;'>
            Automated Resume Parsing • Advanced Skill Detection • Intelligent Candidate Matching</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>📋 How It Works — 5 Simple Steps</div>", unsafe_allow_html=True)
    steps = [
        ("📄", "Step 1", "Upload Resumes",        "Upload single or multiple PDF / DOCX resumes through the Upload & Analyze page."),
        ("📋", "Step 2", "Paste Job Description", "Enter the job description you want to match candidates against."),
        ("🧠", "Step 3", "AI Analysis",           "The system parses resumes, detects skills, and generates semantic embeddings using RoBERTa."),
        ("📊", "Step 4", "Ranking & Scoring",     "Candidates are ranked via cosine similarity + ML prediction. Statuses are assigned automatically."),
        ("📄", "Step 5", "View Reports",           "Explore the Dashboard for analytics, Candidate Detail for deep insights, and download the PDF report."),
    ]
    cols = st.columns(5)
    for col, (icon, step, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""<div class='glass-card' style='text-align:center;min-height:200px;'>
                <div style='font-size:32px;'>{icon}</div>
                <div style='font-size:10px;color:#667eea;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:6px 0 2px 0;'>{step}</div>
                <div style='font-size:13px;font-weight:700;color:#a78bfa;margin-bottom:8px;'>{title}</div>
                <div style='font-size:11px;color:#444;line-height:1.6;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>💡 Why HireRight AI?</div>", unsafe_allow_html=True)
    w1, w2, w3, w4 = st.columns(4)
    for col, (icon, title, desc) in zip([w1,w2,w3,w4], [
        ("⏱️", "Saves Time",  "Screens 100 resumes in minutes"),
        ("⚖️", "Bias Free",   "AI-driven objective evaluation"),
        ("🎯", "Accurate",    "RoBERTa semantic matching"),
        ("📊", "Insightful",  "Visual analytics & skill trends"),
    ]):
        with col:
            st.markdown(
                f"<div class='glass-card' style='text-align:center;'>"
                f"<div style='font-size:30px;'>{icon}</div>"
                f"<div style='font-size:13px;font-weight:700;color:#a78bfa;margin:8px 0 4px 0;'>{title}</div>"
                f"<div style='font-size:12px;color:#444;'>{desc}</div></div>",
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Go to **Upload & Analyze** to get started!")
