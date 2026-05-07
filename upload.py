# ============================================================
# pages/upload.py — Upload & Analyze page
# ============================================================

import streamlit as st

from model import load_models
from parser import extract_text_from_pdf, extract_text_from_docx, parse_resume, extract_expected_skills
from pipeline import run_pipeline


def render():
    st.markdown("<div class='section-header'>📤 Upload Resumes & Analyze</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass-card'><h3>📄 Upload Resumes</h3>"
                    "<p style='color:#555;font-size:13px;'>Upload PDF or DOCX resumes for AI-powered analysis.</p></div>",
                    unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Drop resumes here", type=["pdf","docx"], accept_multiple_files=True)
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} resume(s) uploaded!")
            for f in uploaded_files:
                icon = "📕" if f.name.endswith(".pdf") else "📘"
                st.markdown(
                    f"<div style='background:rgba(102,126,234,0.08);border:1px solid rgba(102,126,234,0.2);"
                    f"border-radius:8px;padding:8px 14px;margin:4px 0;font-size:13px;color:#a78bfa;'>"
                    f"{icon} {f.name} — {round(f.size/(1024*1024),2)} MB</div>",
                    unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h3>📋 Job Description</h3>"
                    "<p style='color:#555;font-size:13px;'>Paste the job description to match against.</p></div>",
                    unsafe_allow_html=True)
        job_description = st.text_area("Paste Job Description", height=200,
                                        placeholder="We are looking for a Data Scientist with Python, ML, NLP...")
        if job_description:
            st.info(f"📝 {len(job_description.split())} words")
            exp_skills = extract_expected_skills(job_description)
            if exp_skills and exp_skills != ["Not Found"]:
                exp_html = "".join([f"<span class='skill-tag-expected'>{s}</span>" for s in exp_skills])
                st.markdown(
                    f"<div style='margin-top:8px;'>"
                    f"<div style='font-size:12px;color:#4ade80;font-weight:700;margin-bottom:4px;'>"
                    f"✅ Expected Skills from JD ({len(exp_skills)})</div>{exp_html}</div>",
                    unsafe_allow_html=True)

    # ── Parse Button ──────────────────────────────────────────
    if uploaded_files:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Parse Resumes — Show Extracted Data", use_container_width=True):
            with st.spinner("🤖 Loading AI model..."):
                nlp, tokenizer, roberta_model = load_models()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>📋 Resume Parsing Output</div>", unsafe_allow_html=True)
            jd_expected = extract_expected_skills(job_description) if job_description else []

            for uploaded_file in uploaded_files:
                uploaded_file.seek(0)
                if uploaded_file.name.endswith(".pdf"):
                    text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.name.endswith(".docx"):
                    text = extract_text_from_docx(uploaded_file)
                else:
                    continue
                if not text.strip():
                    st.warning(f"⚠️ Could not extract text from {uploaded_file.name}")
                    continue

                parsed = parse_resume(text, nlp)
                _render_parse_card(uploaded_file, parsed, jd_expected)

    # ── Analyze Button ────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if uploaded_files and job_description:
        if st.button("🤖 Analyze & Rank Candidates", use_container_width=True):
            for f in uploaded_files:
                f.seek(0)
            with st.spinner("Loading AI model..."):
                nlp, tokenizer, roberta_model = load_models()
            st.markdown("---")
            st.markdown("### ⚡ Processing Pipeline")
            result = run_pipeline(uploaded_files, job_description, nlp, tokenizer, roberta_model)
            if result:
                st.session_state["results2"]         = result
                st.session_state["job_description2"] = job_description
                st.success("✅ Done! Go to Dashboard.")
                st.balloons()
            else:
                st.error("❌ Could not process resumes.")
    else:
        if not uploaded_files:
            st.warning("⚠️ Please upload at least one resume.")
        if not job_description:
            st.warning("⚠️ Please enter a job description to rank candidates.")


# ── HELPERS ───────────────────────────────────────────────────

def _render_parse_card(uploaded_file, parsed, jd_expected):
    detected  = parsed['Skills']
    possessed = [s for s in detected if s.lower() in [e.lower() for e in jd_expected]]
    missing   = [s for s in jd_expected if s.lower() not in [d.lower() for d in detected]]

    det_html  = "".join([f"<span class='skill-tag'>{s}</span>" for s in detected])
    poss_html = "".join([f"<span class='skill-tag-expected'>{s}</span>" for s in possessed]) \
                if possessed else "<span style='color:#555;font-size:12px;'>None matched</span>"
    miss_html = "".join([f"<span class='skill-tag-missing'>{s}</span>" for s in missing]) \
                if missing else "<span style='color:#4ade80;font-size:12px;'>✅ All present</span>"

    st.markdown(f"""
    <div class='parse-card'>
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;'>
            <div>
                <div style='font-size:22px;font-weight:800;color:#ccc;'>👤 {parsed['Name']}</div>
                <div style='font-size:12px;color:#555;margin-top:4px;'>📁 {uploaded_file.name}</div>
            </div>
            <span style='background:rgba(102,126,234,0.2);color:#a78bfa;padding:6px 16px;
                         border-radius:20px;font-size:12px;font-weight:700;border:1px solid rgba(102,126,234,0.3);'>✅ PARSED</span>
        </div>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px;'>
            <div style='background:rgba(255,255,255,0.02);border-radius:8px;padding:10px;'>
                <span style='color:#667eea;font-size:11px;font-weight:700;'>📧 EMAIL</span><br/>
                <span style='color:#aaa;font-size:13px;'>{parsed['Email']}</span>
            </div>
            <div style='background:rgba(255,255,255,0.02);border-radius:8px;padding:10px;'>
                <span style='color:#667eea;font-size:11px;font-weight:700;'>📞 PHONE</span><br/>
                <span style='color:#aaa;font-size:13px;'>{parsed['Phone']}</span>
            </div>
            <div style='background:rgba(255,255,255,0.02);border-radius:8px;padding:10px;'>
                <span style='color:#667eea;font-size:11px;font-weight:700;'>🔗 LINKEDIN</span><br/>
                <span style='color:#aaa;font-size:13px;'>{parsed['LinkedIn']}</span>
            </div>
            <div style='background:rgba(255,255,255,0.02);border-radius:8px;padding:10px;'>
                <span style='color:#667eea;font-size:11px;font-weight:700;'>🐙 GITHUB</span><br/>
                <span style='color:#aaa;font-size:13px;'>{parsed['GitHub']}</span>
            </div>
        </div>
        <div style='margin-bottom:10px;'>
            <div style='color:#a78bfa;font-weight:700;font-size:13px;margin-bottom:6px;'>🛠 SKILLS DETECTED ({len(detected)})</div>
            <div>{det_html}</div>
        </div>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
            <div style='background:rgba(74,222,128,0.04);border-radius:8px;padding:10px;border:1px solid rgba(74,222,128,0.15);'>
                <div style='color:#4ade80;font-weight:700;font-size:12px;margin-bottom:6px;'>✅ POSSESSED SKILLS (JD Match)</div>
                <div>{poss_html}</div>
            </div>
            <div style='background:rgba(248,113,113,0.04);border-radius:8px;padding:10px;border:1px solid rgba(248,113,113,0.15);'>
                <div style='color:#f87171;font-weight:700;font-size:12px;margin-bottom:6px;'>❌ MISSING SKILLS (from JD)</div>
                <div>{miss_html}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    def _section_expander(label, items, bg, border):
        with st.expander(label):
            for item in items:
                st.markdown(
                    f"<div style='background:{bg};border-left:3px solid {border};"
                    f"border-radius:6px;padding:8px 14px;margin:4px 0;font-size:13px;color:#888;'>• {item}</div>",
                    unsafe_allow_html=True)

    _section_expander(f"🎓 Education — {parsed['Name']}",      parsed['Education'],      "rgba(102,126,234,0.05)", "#667eea")
    _section_expander(f"💼 Experience — {parsed['Name']}",     parsed['Experience'],     "rgba(251,191,36,0.05)",  "#fbbf24")
    _section_expander(f"💻 Projects — {parsed['Name']}",       parsed['Projects'],       "rgba(240,147,251,0.05)", "#f093fb")
    _section_expander(f"📜 Certifications — {parsed['Name']}", parsed['Certifications'], "rgba(96,165,250,0.05)",  "#60a5fa")
    _section_expander(f"🏆 Achievements — {parsed['Name']}",   parsed['Achievements'],   "rgba(74,222,128,0.05)",  "#4ade80")
