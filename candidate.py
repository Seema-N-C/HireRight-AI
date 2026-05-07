# ============================================================
# pages/candidate.py — Candidate Detail page
# ============================================================

import streamlit as st


def render():
    if "results2" not in st.session_state:
        st.warning("⚠️ No results. Go to Upload & Analyze first.")
        st.stop()

    data          = st.session_state["results2"]
    final_results = data["final_results"]

    st.markdown("<div class='section-header'>👤 Candidate Detail View</div>", unsafe_allow_html=True)

    names    = [r["parsed"]["Name"] for r in final_results]
    selected = st.selectbox("Select Candidate", names)
    r = next(x for x in final_results if x["parsed"]["Name"] == selected)
    p = r["parsed"]; score = r["final_score"]

    if score >= 75:
        status_txt, score_color, card_class = "✅ Shortlisted",   "#4ade80", "shortlisted"
    elif score >= 50:
        status_txt, score_color, card_class = "⚠️ Under Review",  "#fbbf24", "under-review"
    else:
        status_txt, score_color, card_class = "❌ Rejected",      "#f87171", "rejected"

    st.markdown(f"""<div class='glass-card {card_class}'>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <div>
                <div style='font-size:26px;font-weight:800;color:#ccc;'>{p['Name']}</div>
                <div style='font-size:13px;color:#444;margin-top:4px;'>📧 {p['Email']} &nbsp;|&nbsp; 📞 {p['Phone']}</div>
                <div style='font-size:13px;color:#444;margin-top:4px;'>🔗 {p['LinkedIn']} &nbsp;|&nbsp; 🐙 {p['GitHub']}</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:44px;font-weight:800;color:{score_color};'>{score}%</div>
                <div style='font-size:14px;font-weight:700;color:{score_color};'>{status_txt}</div>
            </div>
        </div></div>""", unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3)
    for col, val, label in zip(
        [sc1, sc2, sc3],
        [f"{round(r['similarity_score']*100,2)}%", f"{round(r['prediction_prob']*100,2)}%", f"{score}%"],
        ["🤖 RoBERTa Similarity", "🧠 LR Prediction", "🎯 Final Score"]
    ):
        with col:
            st.markdown(
                f"<div class='stat-card'>"
                f"<div style='font-size:11px;color:#555;text-transform:uppercase;letter-spacing:1px;'>{label}</div>"
                f"<div class='stat-val'>{val}</div></div>",
                unsafe_allow_html=True)

    # ── Skills Analysis ───────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🛠 Skills Analysis</div>", unsafe_allow_html=True)

    possessed = r.get("possessed_skills", [])
    missing   = r.get("missing_skills", [])
    poss_html = "".join([f"<span class='skill-tag-expected'>{s}</span>" for s in possessed]) \
                if possessed else "<span style='color:#555;font-size:12px;'>None matched JD</span>"
    miss_html = "".join([f"<span class='skill-tag-missing'>{s}</span>"  for s in missing]) \
                if missing   else "<span style='color:#4ade80;font-size:12px;'>✅ All skills present</span>"
    det_html  = "".join([f"<span class='skill-tag'>{s}</span>" for s in p["Skills"]])

    st.markdown(f"""
    <div style='background:rgba(102,126,234,0.04);border-radius:8px;padding:12px;border:1px solid rgba(102,126,234,0.15);margin-bottom:10px;'>
        <div style='color:#a78bfa;font-weight:700;font-size:12px;margin-bottom:8px;'>🔍 ALL DETECTED SKILLS ({len(p["Skills"])})</div>
        <div>{det_html}</div>
    </div>
    <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
        <div style='background:rgba(74,222,128,0.04);border-radius:8px;padding:12px;border:1px solid rgba(74,222,128,0.2);'>
            <div style='color:#4ade80;font-weight:700;font-size:12px;margin-bottom:8px;'>✅ POSSESSED SKILLS (JD Match)</div>
            <div>{poss_html}</div>
        </div>
        <div style='background:rgba(248,113,113,0.04);border-radius:8px;padding:12px;border:1px solid rgba(248,113,113,0.2);'>
            <div style='color:#f87171;font-weight:700;font-size:12px;margin-bottom:8px;'>❌ MISSING SKILLS (from JD)</div>
            <div>{miss_html}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Expandable Sections ───────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    def _section(label, items, bg, border):
        with st.expander(label):
            for item in items:
                st.markdown(
                    f"<div style='background:{bg};border-left:3px solid {border};"
                    f"border-radius:6px;padding:8px 14px;margin:4px 0;font-size:13px;color:#888;'>• {item}</div>",
                    unsafe_allow_html=True)

    _section("🎓 Education",      p["Education"],      "rgba(102,126,234,0.05)", "#667eea")
    _section("💼 Experience",     p["Experience"],     "rgba(251,191,36,0.05)",  "#fbbf24")
    _section("💻 Projects",       p["Projects"],       "rgba(240,147,251,0.05)", "#f093fb")
    _section("📜 Certifications", p["Certifications"], "rgba(96,165,250,0.05)",  "#60a5fa")
    _section("🏆 Achievements",   p["Achievements"],   "rgba(74,222,128,0.05)",  "#4ade80")

    # ── Role Suggestions (Rejected only) ─────────────────────
    if score < 50 and r.get("role_suggestions"):
        st.markdown("<div class='section-header'>💡 Suggested Job Roles</div>", unsafe_allow_html=True)
        for role, info in r["role_suggestions"]:
            m_html = "".join([f"<span class='skill-tag-expected'>{s}</span>" for s in info['matched_skills']])
            g_html = "".join([f"<span class='skill-tag-missing'>{s}</span>"  for s in info['missing_skills'][:5]])
            st.markdown(f"""<div class='role-suggest-card'>
                <div style='font-size:15px;font-weight:700;color:#a78bfa;'>🎯 {role}
                    <span style='color:#4ade80;font-size:13px;margin-left:8px;'>{info['match_pct']}% skill match</span>
                </div>
                <div style='margin-top:8px;font-size:12px;color:#555;'>✅ Matched: {m_html}</div>
                <div style='margin-top:4px;font-size:12px;color:#555;'>📚 Skills to Develop: {g_html}</div>
            </div>""", unsafe_allow_html=True)
