# ============================================================
# config.py — Global constants, API keys, model settings
# ============================================================

# ── MODEL ────────────────────────────────────────────────────
MODEL_NAME = "sentence-transformers/all-roberta-large-v1"

# ── JSEARCH API ──────────────────────────────────────────────
JSEARCH_API_KEY = "e9836e9a52msh0fdf4008c24066bp176d9cjsn9840da544df4"
JSEARCH_HOST    = "jsearch.p.rapidapi.com"
JSEARCH_URL     = "https://jsearch.p.rapidapi.com/search"

# ── SKILLS DATABASE ──────────────────────────────────────────
SKILLS_DB = [
    "python","java","c++","c#","c","r","scala","kotlin","swift","go",
    "javascript","typescript","matlab","bash","machine learning","deep learning",
    "artificial intelligence","neural networks","natural language processing","nlp",
    "computer vision","reinforcement learning","bert","gpt","transformers","llm",
    "tensorflow","pytorch","keras","scikit-learn","xgboost","huggingface",
    "spacy","nltk","opencv","pandas","numpy","scipy","matplotlib","seaborn","plotly",
    "data analysis","data science","data visualization","feature engineering",
    "sql","mysql","postgresql","mongodb","sqlite","redis",
    "flask","django","fastapi","streamlit","html","css","react","nodejs","rest api",
    "aws","gcp","azure","docker","kubernetes","git","github",
    "linux","power bi","tableau","excel","hadoop","spark","roberta","distilbert"
]

# ── JOB ROLES MAP ────────────────────────────────────────────
JOB_ROLES = {
    "Data Analyst":              ["python","sql","pandas","numpy","tableau","power bi","excel","data analysis","data visualization","matplotlib","seaborn"],
    "Web Developer":             ["html","css","javascript","react","nodejs","git","rest api","mongodb","flask","django"],
    "Machine Learning Engineer": ["python","machine learning","scikit-learn","tensorflow","pytorch","numpy","pandas","deep learning","keras","xgboost"],
    "Data Scientist":            ["python","machine learning","deep learning","nlp","data analysis","pandas","numpy","sql","tensorflow","pytorch","scikit-learn"],
    "DevOps Engineer":           ["docker","kubernetes","linux","aws","azure","gcp","git","bash"],
    "Backend Developer":         ["java","python","nodejs","flask","django","fastapi","sql","mongodb","redis","rest api","docker"],
    "NLP / AI Engineer":         ["nlp","natural language processing","python","transformers","bert","spacy","nltk","huggingface","pytorch","tensorflow"],
    "Cloud Engineer":            ["aws","azure","gcp","docker","kubernetes","linux","git","bash"],
    "Frontend Developer":        ["html","css","javascript","react","typescript","git","nodejs"],
    "Database Administrator":    ["sql","mysql","postgresql","mongodb","sqlite","redis","data analysis","excel"],
}

# ── NAME EXTRACTION HELPERS ──────────────────────────────────
SKIP_KEYWORDS = [
    "resume","curriculum","vitae","cv","profile","summary","objective",
    "contact","address","email","phone","mobile","linkedin","github",
    "http","www","career","about","declaration","name","details",
    "information","page","references","skills","projects","education",
    "experience","achievements","certifications","languages","hobbies",
    "developer","dev","engineer","designer","analyst","scientist",
    "manager","architect","consultant","specialist","intern","lead",
    "model","data","software","full stack","frontend","backend",
    "machine learning","ai","ml","web","mobile","cloud","devops",
    "spring","spring boot","java","python","react","node","angular",
    "django","flask","docker","kubernetes","aws","azure","gcp",
    "mongodb","mysql","postgresql","redis","tensorflow","pytorch",
    "hadoop","spark","tableau","power bi","excel","linux","git",
    "javascript","typescript","html","css","rest","api","sql"
]

NAME_PREFIXES = ["mr.","mrs.","ms.","dr.","prof."]

# ── CHART COLORS ─────────────────────────────────────────────
PURPLE = "#667eea"
PINK   = "#f093fb"
GREEN  = "#4ade80"
YELLOW = "#fbbf24"
RED    = "#f87171"
