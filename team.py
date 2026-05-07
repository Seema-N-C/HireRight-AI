# ============================================================
# pages/team.py — Meet The Team Page
# ============================================================

import streamlit as st


def render():

    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-size:28px; font-weight:800; color:#a78bfa; letter-spacing:1px;'>
            👥 MEET THE TEAM
        </div>
        <div style='font-size:13px; color:#9ca3af; margin-top:6px;'>
            AI-Powered Intelligent Recruitment System
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MODULE OVERVIEW ──────────────────────────────────────
    st.markdown("""
    <div style='background:rgba(167,139,250,0.08); border:1px solid rgba(167,139,250,0.25);
    border-radius:12px; padding:20px; margin-bottom:24px;'>
        <div style='font-size:14px; font-weight:800; color:#a78bfa;
        letter-spacing:2px; margin-bottom:14px;'>📦 MODULE OVERVIEW</div>
    """, unsafe_allow_html=True)

    modules = [
        ("Module 1", "Resume Upload & Parsing",           "Md Furhan Pasha & Rakshith Krishna Murthy"),
        ("Module 2", "Job Description Processing",        "Md Furhan Pasha & Rakshith Krishna Murthy"),
        ("Module 3", "Skill Extraction & Matching",       "Md Furhan Pasha & Rakshith Krishna Murthy"),
        ("Module 4", "NLP Processing",                    "Ajith B & Seema N C"),
        ("Module 5", "Feature Engineering",               "Ajith B & Seema N C"),
        ("Module 6", "Similarity & Candidate Ranking",    "Gokul Adithya"),
        ("Module 7", "Suitability Prediction Model",      "Diya Dadheech"),
        ("Module 8", "Analytics Dashboard",               "Disha S Reddy"),
        ("Module 9", "Report Generation",                 "Disha S Reddy"),
    ]

    for mod_num, mod_name, assignee in modules:
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center;
        background:rgba(15,12,41,0.6); border:1px solid rgba(167,139,250,0.15);
        border-radius:8px; padding:10px 16px; margin-bottom:8px;'>
            <div style='display:flex; align-items:center; gap:12px;'>
                <span style='background:#7c3aed; color:white; font-size:10px;
                font-weight:800; padding:3px 8px; border-radius:4px;'>{mod_num}</span>
                <span style='color:#e0deff; font-size:13px; font-weight:600;'>{mod_name}</span>
            </div>
            <span style='color:#9ca3af; font-size:11px;'>👤 {assignee}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── TEAM MEMBERS ─────────────────────────────────────────
    st.markdown("""
    <div style='font-size:14px; font-weight:800; color:#a78bfa;
    letter-spacing:2px; margin-bottom:14px;'>👤 TEAM MEMBERS</div>
    """, unsafe_allow_html=True)

    team = [
        {
            "name":    "Md Furhan Pasha",
            "role":    "Co-Lead — Modules 1, 2 & 3",
            "phone":   "+91 9731959289",
            "email":   "mdfurhanpasha@gmail.com",
            "work":    "Resume Upload & Parsing, Job Description Processing, Skill Extraction & Matching",
            "modules": "Module 1, 2 & 3",
            "icon":    "🧑‍💻",
        },
        {
            "name":    "Rakshith Krishna Murthy",
            "role":    "Co-Lead — Modules 1, 2 & 3",
            "phone":   "+91 9972515793",
            "email":   "rakr22aiml@cmrit.ac.in",
            "work":    "Resume Upload & Parsing, Job Description Processing, Skill Extraction & Matching",
            "modules": "Module 1, 2 & 3",
            "icon":    "🧑‍💻",
        },
        {
            "name":    "Ajith B",
            "role":    "C0-Lead — Modules 4 & 5",
            "phone":   "+91 8088113521",
            "email":   "ajithbalachandran911@gmail.com",
            "work":    "NLP Processing & Feature Engineering",
            "modules": "Module 4 & 5",
            "icon":    "🤖",
        },
        {
            "name":    "Seema N C",
            "role":    "Co-Lead — Modules 4 & 5",
            "phone":   "+91 9611533161",
            "email":   "ncseema5@@example.com",
            "work":    "NLP Processing & Feature Engineering",
            "modules": "Module 4 & 5",
            "icon":    "🤖",
        },
        {
            "name":    "Gokul Adithya",
            "role":    "Lead — Module 6",
            "phone":   "+91 6363317030",
            "email":   "gokuladithya71745@gmail.com",
            "work":    "Similarity Scoring & Candidate Ranking",
            "modules": "Module 6",
            "icon":    "📊",
        },
        {
            "name":    "Diya Dadheech",
            "role":    "Lead — Module 7",
            "phone":   "+91 9610760019",
            "email":   "diya05dadheech@gmail.com",
            "work":    "Suitability Prediction Model",
            "modules": "Module 7",
            "icon":    "🎯",
        },
        {
            "name":    "Disha S Reddy",
            "role":    "Lead - Dashboard & Reports — Modules 8 & 9",
            "phone":   "+91 9535131242",
            "email":   "dishareddy3704@gmail.com",
            "work":    "Analytics Dashboard & Report Generation",
            "modules": "Module 8 & 9",
            "icon":    "📈",
        },
    ]

    # Display in 2 columns
    for i in range(0, len(team), 2):
        col1, col2 = st.columns(2)
        with col1:
             st.markdown(f"""
             <div style='background:rgba(15,12,41,0.7);border:1px solid rgba(167,139,250,0.2);border-radius:12px;padding:16px;margin-bottom:14px;'>
            <div style='color:#ffffff;font-size:14px;font-weight:800;'>{team[i]['icon']} {team[i]['name']}</div>
            <div style='color:#7c3aed;font-size:11px;'>{team[i]['role']}</div>
            <div style='color:#d1d5db;font-size:11px;margin-top:8px;'>📞 {team[i]['phone']}</div>
            <div style='color:#d1d5db;font-size:11px;'>✉️ {team[i]['email']}</div>
            <div style='color:#c4b5fd;font-size:11px;margin-top:8px;'>{team[i]['work']}</div>
            </div>
            """, unsafe_allow_html=True)
        if i + 1 < len(team):
            with col2:
                st.markdown(f"""
            <div style='background:rgba(15,12,41,0.7);border:1px solid rgba(167,139,250,0.2);border-radius:12px;padding:16px;margin-bottom:14px;'>
            <div style='color:#ffffff;font-size:14px;font-weight:800;'>{team[i+1]['icon']} {team[i+1]['name']}</div>
            <div style='color:#7c3aed;font-size:11px;'>{team[i+1]['role']}</div>
            <div style='color:#d1d5db;font-size:11px;margin-top:8px;'>📞 {team[i+1]['phone']}</div>
            <div style='color:#d1d5db;font-size:11px;'>✉️ {team[i+1]['email']}</div>
            <div style='color:#c4b5fd;font-size:11px;margin-top:8px;'>{team[i+1]['work']}</div>
             </div>
               """, unsafe_allow_html=True)