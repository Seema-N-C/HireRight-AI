# ============================================================
# pipeline.py — ML scoring, ranking, job role suggestions
# ============================================================

import numpy as np
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, roc_curve, auc)

from config import JOB_ROLES
from model import get_embedding
from parser import (extract_text_from_pdf, extract_text_from_docx,
                             parse_resume, extract_expected_skills)


# ── JOB ROLE SUGGESTIONS ─────────────────────────────────────

def suggest_job_roles(candidate_skills: list, top_n: int = 3) -> list:
    cskills = set(s.lower() for s in candidate_skills)
    scores  = {}
    for role, required in JOB_ROLES.items():
        matched = cskills.intersection(set(r.lower() for r in required))
        if matched:
            scores[role] = {
                "match_pct":      round(len(matched) / len(required) * 100, 1),
                "matched_skills": [s.title() for s in matched],
                "missing_skills": [s.title() for s in set(r.lower() for r in required) - cskills],
            }
    return sorted(scores.items(), key=lambda x: x[1]["match_pct"], reverse=True)[:top_n]


# ── LIVE JOB FETCH ────────────────────────────────────────────

def fetch_live_jobs(role_title: str, num_results: int = 3) -> list:
    """Fetch live job listings from JSearch (Google for Jobs aggregator)."""
    import requests
    from config import JSEARCH_API_KEY, JSEARCH_HOST, JSEARCH_URL

    headers = {
        "X-RapidAPI-Key": "Your_api_key ",
        "X-RapidAPI-Host":"jsearch.p.rapidapi.com",
    }
    params = {
        "query":     f"{role_title} jobs",
        "page":      "1",
        "num_pages": "2",
        "country":   "us",
        "language":  "en",
    }

    try:
        response = requests.get(
            JSEARCH_URL,
            headers=headers,
            params=params,
            timeout=10,
        )

        if response.status_code == 403:
            return [{"_error": "API key invalid or quota exceeded (403)"}]
        if response.status_code == 429:
            return [{"_error": "Rate limit hit — too many requests (429)"}]
        if response.status_code != 200:
            return [{"_error": f"API returned status {response.status_code}"}]

        # ✅ CORRECT: data is a direct LIST, not a dict with "jobs" key
        jobs = response.json().get("data", [])

        if not jobs:
            return []

        return [
            {
                "title":    job.get("job_title",                       "N/A"),
                "company":  job.get("employer_name",                   "N/A"),
                "location": (job.get("job_city")    or "") + ", " +
                            (job.get("job_country") or ""),
                "type":     job.get("job_employment_type",             "N/A"),
                "posted":   (job.get("job_posted_at_datetime_utc") or "")[:10],
                "url":      job.get("job_apply_link") or
                            job.get("job_google_link", "#"),
                "salary":   (str(job.get("job_min_salary"))
                             if job.get("job_min_salary")
                             else job.get("job_salary_string") or "Not disclosed"),
            }
            for job in jobs[:num_results]
        ]

    except requests.exceptions.Timeout:
        return [{"_error": "Request timed out"}]
    except requests.exceptions.ConnectionError:
        return [{"_error": "No internet connection"}]
    except Exception as e:
        return [{"_error": f"Unexpected error: {str(e)}"}]


# ── MAIN ANALYSIS PIPELINE ───────────────────────────────────

def run_pipeline(uploaded_files, job_description, nlp, tokenizer, roberta_model) -> dict | None:
    total           = len(uploaded_files)
    expected_skills = extract_expected_skills(job_description)
    results         = []
    progress        = st.progress(0)
    status          = st.empty()
    STAGES          = total + 4

    # Step 1: Parse & embed each resume
    for i, uploaded_file in enumerate(uploaded_files):
        pct = int((i + 1) / STAGES * 100)
        status.markdown(
            f"<div style='background:rgba(102,126,234,0.07);border:1px solid rgba(102,126,234,0.2);"
            f"border-radius:10px;padding:12px 18px;margin:6px 0;'>"
            f"<div style='font-size:12px;color:#667eea;font-weight:700;margin-bottom:6px;'>🧠 RoBERTa Pipeline</div>"
            f"📄 Parsing & embedding <b style='color:#a78bfa;'>{uploaded_file.name}</b> "
            f"<span style='color:#555;font-size:11px;'>({pct}%)</span></div>",
            unsafe_allow_html=True)
        progress.progress((i + 1) / STAGES)

        if uploaded_file.name.endswith('.pdf'):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            text = extract_text_from_docx(uploaded_file)
        else:
            continue
        if not text.strip():
            continue

        parsed   = parse_resume(text, nlp)
        features = get_embedding(text, tokenizer, roberta_model)
        results.append({'file_name': uploaded_file.name, 'raw_text': text,
                        'parsed': parsed, 'roberta_features': features})

    if not results:
        return None

    # Step 2: JD embedding + cosine similarity
    status.markdown(
        "<div style='background:rgba(102,126,234,0.07);border:1px solid rgba(102,126,234,0.2);"
        "border-radius:10px;padding:12px 18px;margin:6px 0;'>"
        "<div style='font-size:12px;color:#667eea;font-weight:700;margin-bottom:6px;'>🧠 RoBERTa Pipeline</div>"
        "📋 Generating <b style='color:#a78bfa;'>Job Description embedding</b> "
        "<span style='color:#555;font-size:11px;'>(85%)</span></div>",
        unsafe_allow_html=True)
    progress.progress(0.85)

    jd_embedding = get_embedding(job_description, tokenizer, roberta_model)
    for r in results:
        sim = cosine_similarity(r['roberta_features'].reshape(1, -1),
                                jd_embedding.reshape(1, -1))[0][0]
        r['similarity_score'] = round(float(sim), 4)
    results = sorted(results, key=lambda x: x['similarity_score'], reverse=True)

    # Step 3: Logistic Regression classifier
    status.markdown(
        "<div style='background:rgba(102,126,234,0.07);border:1px solid rgba(102,126,234,0.2);"
        "border-radius:10px;padding:12px 18px;margin:6px 0;'>"
        "<div style='font-size:12px;color:#667eea;font-weight:700;margin-bottom:6px;'>🧠 RoBERTa Pipeline</div>"
        "🎯 Training <b style='color:#a78bfa;'>ML Classifier</b> on candidate features "
        "<span style='color:#555;font-size:11px;'>(92%)</span></div>",
        unsafe_allow_html=True)
    progress.progress(0.92)

    USE_LR = len(results) >= 5

    if USE_LR:
        X      = np.array([r["roberta_features"] for r in results])
        scores = [r["similarity_score"] for r in results]
        median = np.median(scores)
        y      = np.array([1 if r["similarity_score"] >= median else 0 for r in results])
        if len(set(y)) < 2:
            mid = len(y) // 2; y[:mid] = 1; y[mid:] = 0

        np.random.seed(42); X_aug, y_aug = [], []
        for i in range(len(X)):
            for _ in range(40): X_aug.append(X[i] + np.random.normal(0, 0.01, X[i].shape)); y_aug.append(y[i])
            for _ in range(10): X_aug.append(X[i] + np.random.normal(0, 0.05, X[i].shape)); y_aug.append(1 - y[i])
        X_aug = np.array(X_aug); y_aug = np.array(y_aug)

        X_train, X_test, y_train, y_test = train_test_split(
            X_aug, y_aug, test_size=0.2, random_state=42, stratify=y_aug)
        scaler   = StandardScaler()
        X_train  = scaler.fit_transform(X_train)
        X_test   = scaler.transform(X_test)
        lr_model = LogisticRegression(max_iter=1000, random_state=42)
        lr_model.fit(X_train, y_train)

        y_pred      = lr_model.predict(X_test)
        y_pred_prob = lr_model.predict_proba(X_test)[:, 1]
        accuracy    = round(accuracy_score(y_test, y_pred) * 100, 2)
        precision   = round(precision_score(y_test, y_pred, zero_division=0) * 100, 2)
        recall      = round(recall_score(y_test, y_pred, zero_division=0) * 100, 2)
        fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
        roc_auc     = round(auc(fpr, tpr), 4)
    else:
        accuracy = precision = recall = 0.0
        roc_auc  = 0.0
        fpr      = np.array([0.0, 1.0])
        tpr      = np.array([0.0, 1.0])
        scaler   = StandardScaler()
        X_all    = np.array([r["roberta_features"] for r in results])
        scaler.fit(X_all)

        class _DummyLR:
            def predict_proba(self, X):
                return np.array([[0.5, 0.5]] * len(X))
        lr_model = _DummyLR()

    # Step 4: Compute final blended scores
    final_results = []
    for r in results:
        sim       = r["similarity_score"]
        detected  = r["parsed"]["Skills"]
        possessed = [s for s in detected if s.lower() in [e.lower() for e in expected_skills]]
        missing   = [s for s in expected_skills if s.lower() not in [d.lower() for d in detected]]
        skill_score = len(possessed) / max(len(expected_skills), 1)

        feat_scaled = scaler.transform(r["roberta_features"].reshape(1, -1))
        prob        = lr_model.predict_proba(feat_scaled)[0][1]

        if USE_LR:
            final_score = round((sim * 0.5 + skill_score * 0.3 + float(prob) * 0.2) * 100, 2)
        else:
            final_score = round((sim * 0.6 + skill_score * 0.4) * 100, 2)

        role_suggestions = suggest_job_roles(detected) if final_score < 50 else []
        final_results.append({
            **r,
            "prediction_prob":  round(float(prob), 4),
            "skill_score":      round(skill_score * 100, 1),
            "final_score":      final_score,
            "possessed_skills": possessed,
            "missing_skills":   missing,
            "role_suggestions": role_suggestions,
        })

    final_results = sorted(final_results, key=lambda x: x["final_score"], reverse=True)

    progress.progress(1.0)
    status.markdown(
        "<div style='background:rgba(74,222,128,0.07);border:1px solid rgba(74,222,128,0.3);"
        "border-radius:10px;padding:12px 18px;margin:6px 0;'>"
        "✅ <b style='color:#4ade80;'>Analysis complete!</b> "
        "<span style='color:#555;font-size:12px;'>All candidates ranked successfully.</span></div>",
        unsafe_allow_html=True)

    return {
        "final_results":  final_results,
        "jd_embedding":   jd_embedding,
        "expected_skills": expected_skills,
        "fpr":            fpr,
        "tpr":            tpr,
        "metrics": {"accuracy": accuracy, "precision": precision,
                    "recall": recall, "roc_auc": roc_auc},
    }
