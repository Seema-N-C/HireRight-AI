# ============================================================
# pages/dashboard.py — Analytics Dashboard page
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from collections import Counter

from config import PURPLE, PINK, GREEN, YELLOW, RED
from model import set_dark_chart
from pipeline import fetch_live_jobs


def render():
    if "results2" not in st.session_state:
        st.warning("⚠️ No results. Go to Upload & Analyze first.")
        st.stop()

    data          = st.session_state["results2"]
    final_results = data["final_results"]
    metrics       = data["metrics"]

    st.markdown("<div class='section-header'>📊 Analytics Dashboard</div>", unsafe_allow_html=True)

    shortlisted  = sum(1 for r in final_results if r["final_score"] >= 75)
    under_review = sum(1 for r in final_results if 50 <= r["final_score"] < 75)
    rejected     = sum(1 for r in final_results if r["final_score"] < 50)
    top_score    = max(r["final_score"] for r in final_results)

    m1, m2, m3, m4, m5 = st.columns(5)
    for col, val, label, sub in zip(
        [m1, m2, m3, m4, m5],
        [len(final_results), shortlisted, under_review, rejected, f"{top_score}%"],
        ["👥 Total", "✅ Shortlisted", "⚠️ Review", "❌ Rejected", "🏆 Top Score"],
        ["Candidates", "Score ≥75%", "50–75%", "<50%", "Best Match"]
    ):
        with col:
            st.markdown(
                f"<div class='stat-card'>"
                f"<div style='font-size:11px;color:#555;text-transform:uppercase;letter-spacing:1px;'>{label}</div>"
                f"<div class='stat-val'>{val}</div>"
                f"<div class='stat-sub'>{sub}</div></div>",
                unsafe_allow_html=True)

    # ── Candidate Rankings ────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🏅 Candidate Rankings</div>", unsafe_allow_html=True)

    for rank, r in enumerate(final_results, 1):
        p     = r["parsed"]
        score = r["final_score"]
        if score >= 75:
            card_class, badge_cls, status_txt, score_color = "shortlisted", "badge-green",  "✅ Shortlisted", "#4ade80"
        elif score >= 50:
            card_class, badge_cls, status_txt, score_color = "under-review", "badge-orange", "⚠️ Under Review", "#fbbf24"
        else:
            card_class, badge_cls, status_txt, score_color = "rejected",     "badge-red",    "❌ Rejected",    "#f87171"

        skills_html = "".join([f"<span class='skill-tag'>{s}</span>" for s in p["Skills"][:8]])
        possessed   = r.get("possessed_skills", [])
        missing     = r.get("missing_skills", [])
        poss_html   = "".join([f"<span class='skill-tag-expected'>{s}</span>" for s in possessed]) \
                      if possessed else "<span style='color:#555;font-size:12px;'>None matched</span>"
        miss_html   = "".join([f"<span class='skill-tag-missing'>{s}</span>"  for s in missing]) \
                      if missing   else "<span style='color:#4ade80;font-size:12px;'>✅ All present</span>"

        st.markdown(f"""<div class='glass-card {card_class}'>
            <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;'>
                <div><span style='font-size:18px;font-weight:800;color:#ccc;'>#{rank} {p['Name']}</span>
                <span class='badge {badge_cls}' style='margin-left:10px;'>{status_txt}</span></div>
                <div style='text-align:right;'><span style='font-size:28px;font-weight:800;color:{score_color};'>{score}%</span>
                <div style='font-size:11px;color:#444;'>Final Score</div></div>
            </div>
            <div style='margin:8px 0;font-size:12px;color:#444;'>
                📧 {p['Email']} &nbsp;|&nbsp; 📞 {p['Phone']} &nbsp;|&nbsp;
                🤖 Sim: {round(r['similarity_score']*100,1)}% &nbsp;|&nbsp;
                🧠 Pred: {round(r['prediction_prob']*100,1)}%
            </div>
            <div style='margin-top:6px;'>{skills_html}</div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px;'>
                <div style='background:rgba(74,222,128,0.04);border-radius:8px;padding:10px;border:1px solid rgba(74,222,128,0.15);'>
                    <div style='color:#4ade80;font-weight:700;font-size:11px;margin-bottom:6px;'>✅ POSSESSED SKILLS</div>
                    <div>{poss_html}</div>
                </div>
                <div style='background:rgba(248,113,113,0.04);border-radius:8px;padding:10px;border:1px solid rgba(248,113,113,0.15);'>
                    <div style='color:#f87171;font-weight:700;font-size:11px;margin-bottom:6px;'>❌ MISSING SKILLS</div>
                    <div>{miss_html}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Role suggestions + live jobs for rejected candidates
        if  r.get("role_suggestions"):
            st.markdown(
                "<div style='margin:10px 0 6px 0;background:rgba(102,126,234,0.08);"
                "border:1px solid rgba(102,126,234,0.3);border-radius:10px;padding:10px 18px;"
                "font-size:13px;font-weight:700;color:#a78bfa;'>💡 Suggested Job Roles + Live Openings</div>",
                unsafe_allow_html=True)

            for role, info in r["role_suggestions"]:
                m_html = "".join([f"<span class='skill-tag-expected'>{s}</span>" for s in info['matched_skills']])
                g_html = "".join([f"<span class='skill-tag-missing'>{s}</span>"  for s in info['missing_skills'][:5]])
                st.markdown(f"""<div class='role-suggest-card' style='margin-left:16px;'>
                    <div style='font-size:14px;font-weight:700;color:#a78bfa;'>
                        🎯 {role} — <span style='color:#4ade80;'>{info['match_pct']}% match</span></div>
                    <div style='margin-top:6px;font-size:12px;color:#555;'>Matched: {m_html}</div>
                    <div style='margin-top:4px;font-size:12px;color:#555;'>To Improve: {g_html}</div>
                </div>""", unsafe_allow_html=True)

                with st.spinner(f"🌐 Finding live {role} jobs..."):
                    live_jobs = fetch_live_jobs(role)

                if live_jobs:
                    for job in live_jobs:
                        st.markdown(f"""
                        <div style='margin-left:32px;margin-top:6px;background:rgba(74,222,128,0.04);
                                    border:1px solid rgba(74,222,128,0.2);border-radius:10px;padding:12px 16px;'>
                            <div style='font-size:13px;font-weight:700;color:#ccc;'>
                                💼 {job.get('job_title') or job.get('job_occupation') or role }
                                <span style='font-size:11px;color:#667eea;margin-left:8px;'>{job.get('employer_name') or ' '}</span>
                            </div>
                            <div style='font-size:11px;color:#555;margin-top:4px;'>
                                📍 {', '.join(filter(None, [job.get('job_city'), job.get('job_state'), job.get('job_country')])) or 'Location not listed'};
                                📅 {job.get('job_posted_at') or'Recently posted'} &nbsp;|&nbsp; 💰 {job.get('job_salary_string')or 'Not disclosed'}
                            </div>
                            <a href="{job.get('job_apply_link','#')}" target="_blank"
                               style='display:inline-block;margin-top:8px;background:linear-gradient(135deg,#667eea,#764ba2);
                                      color:white;padding:4px 14px;border-radius:20px;font-size:11px;
                                      font-weight:700;text-decoration:none;'>🔗 Apply Now</a>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(
                        "<div style='margin-left:32px;font-size:12px;color:#444;padding:6px 0;'>"
                        "⚠️ No live jobs found right now — try again later.</div>",
                        unsafe_allow_html=True)

    # ── Visual Analytics ──────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📈 Visual Analytics</div>", unsafe_allow_html=True)

    names        = [r["parsed"]["Name"].split()[0] for r in final_results]
    final_scores = [r["final_score"]                for r in final_results]
    sim_scores   = [r["similarity_score"] * 100     for r in final_results]
    pred_scores  = [r["prediction_prob"]  * 100     for r in final_results]
    bar_colors   = [GREEN if s >= 75 else YELLOW if s >= 50 else RED for s in final_scores]
    all_skills   = []
    for r in final_results:
        all_skills.extend(r["parsed"]["Skills"])

    ch1, ch2 = st.columns(2)
    with ch1:
        fig, ax = plt.subplots(figsize=(7, 4)); set_dark_chart(fig, ax)
        bars = ax.barh(names, final_scores, color=bar_colors, edgecolor="#0f0c29", height=0.5)
        ax.set_xlim(0, 115); ax.set_xlabel("Final Score (%)", color="#555")
        ax.set_title("🎯 Candidate Final Scores", color="#a78bfa", fontweight="bold")
        for bar, score in zip(bars, final_scores):
            ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
                    f"{score}%", va="center", fontsize=9, fontweight="bold", color="#ccc")
        ax.grid(axis="x", alpha=0.1, color="#667eea"); st.pyplot(fig); plt.close()

    with ch2:
        fig, ax = plt.subplots(figsize=(7, 4)); set_dark_chart(fig, ax)
        x = np.arange(len(names)); width = 0.35
        ax.bar(x-width/2, sim_scores,  width, label="Similarity", color=PURPLE, alpha=0.85, edgecolor="#0f0c29")
        ax.bar(x+width/2, pred_scores, width, label="Prediction", color=PINK,   alpha=0.85, edgecolor="#0f0c29")
        ax.set_xticks(x); ax.set_xticklabels(names, fontsize=9, color="#555")
        ax.set_ylabel("Score (%)", color="#555")
        ax.set_title("🤖 Similarity vs Prediction", color="#a78bfa", fontweight="bold")
        ax.legend(fontsize=9, facecolor="#0f0c29", labelcolor="#aaa", edgecolor="#333")
        ax.grid(axis="y", alpha=0.1, color="#667eea"); st.pyplot(fig); plt.close()

    ch3, ch4 = st.columns(2)
    with ch3:
        fig, ax = plt.subplots(figsize=(7, 4)); set_dark_chart(fig, ax)
        pie_vals   = [v for v in [shortlisted, under_review, rejected] if v > 0]
        pie_labels = [l for l, v in zip(
            [f"Shortlisted\n({shortlisted})", f"Under Review\n({under_review})", f"Rejected\n({rejected})"],
            [shortlisted, under_review, rejected]) if v > 0]
        pie_colors = [c for c, v in zip([GREEN, YELLOW, RED], [shortlisted, under_review, rejected]) if v > 0]
        wedges, texts, autotexts = ax.pie(pie_vals, labels=pie_labels, colors=pie_colors,
                                           autopct="%1.0f%%", startangle=90,
                                           wedgeprops={"edgecolor": "#0f0c29", "linewidth": 2})
        for t in texts:     t.set_color("#555")
        for t in autotexts: t.set_color("white"); t.set_fontweight("bold")
        ax.set_title("📊 Status Distribution", color="#a78bfa", fontweight="bold"); st.pyplot(fig); plt.close()

    with ch4:
        fig, ax = plt.subplots(figsize=(7, 4)); set_dark_chart(fig, ax)
        top_skills  = Counter(all_skills).most_common(10)
        snames      = [s[0] for s in top_skills]
        svals       = [s[1] for s in top_skills]
        colors_bar  = [plt.cm.cool(i/len(snames)) for i in range(len(snames))]
        ax.barh(snames[::-1], svals[::-1], color=colors_bar[::-1], edgecolor="#0f0c29")
        ax.set_xlabel("Count", color="#555")
        ax.set_title("🛠 Top Skills", color="#a78bfa", fontweight="bold")
        ax.grid(axis="x", alpha=0.1, color="#667eea"); st.pyplot(fig); plt.close()

    # ── Skill Gap Heatmap ─────────────────────────────────────
    st.markdown("<div class='section-header'>🔥 Skill Gap Analysis</div>", unsafe_allow_html=True)
    expected_skills = data.get("expected_skills",
                               ["Python","Machine Learning","Deep Learning","Nlp","Tensorflow",
                                "Scikit-Learn","Pandas","Sql","Data Science","Docker"])
    heatmap_data   = []
    cnames_short   = []
    for r in final_results:
        cskills = [s.lower() for s in r["parsed"]["Skills"]]
        heatmap_data.append([1 if s.lower() in cskills else 0 for s in expected_skills])
        cnames_short.append(r["parsed"]["Name"].split()[0])

    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor("#0f0c29"); ax.set_facecolor("#0f0c29")
    sns.heatmap(np.array(heatmap_data), annot=True, fmt="d",
                xticklabels=expected_skills, yticklabels=cnames_short,
                cmap="PuBu", linewidths=0.5, linecolor="#0f0c29", cbar=False, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10, color="#555")
    ax.set_yticklabels(ax.get_yticklabels(), color="#aaa")
    ax.set_title("Skill Gap (1=Has, 0=Missing)", color="#a78bfa", fontweight="bold", pad=10)
    st.pyplot(fig); plt.close()

    # ── ROC Curve ─────────────────────────────────────────────
    st.markdown("<div class='section-header'>📈 ROC Curve</div>", unsafe_allow_html=True)
    fpr = data["fpr"]; tpr = data["tpr"]
    fig, ax = plt.subplots(figsize=(8, 4)); set_dark_chart(fig, ax)
    ax.plot(fpr, tpr, color=PURPLE, lw=2, label=f"ROC Curve (AUC={data['metrics']['roc_auc']})")
    ax.plot([0,1], [0,1], color="#333", lw=1, linestyle="--")
    ax.fill_between(fpr, tpr, alpha=0.1, color=PURPLE)
    ax.set_xlabel("False Positive Rate", color="#555")
    ax.set_ylabel("True Positive Rate",  color="#555")
    ax.set_title("ROC Curve — Suitability Prediction", color="#a78bfa", fontweight="bold")
    ax.legend(loc="lower right", facecolor="#0f0c29", labelcolor="#aaa", edgecolor="#333")
    st.pyplot(fig); plt.close()
