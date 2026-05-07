# ============================================================
# parser.py — Resume text extraction & structured parsing
# ============================================================

import re
import PyPDF2
import docx
from collections import defaultdict

from config import SKILLS_DB, SKIP_KEYWORDS, NAME_PREFIXES


# ── TEXT EXTRACTION ──────────────────────────────────────────

def extract_text_from_pdf(file) -> str:
    """Smart extractor — handles single-column and multi-column PDF layouts."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                words = page.extract_words()
                if not words:
                    continue
                width       = page.width
                left_words  = [w for w in words if w['x0'] < width * 0.45]
                right_words = [w for w in words if w['x0'] >= width * 0.45]
                left_ratio  = len(left_words) / max(len(words), 1)
                if 0.08 < left_ratio < 0.6 and len(left_words) > 5:
                    def col_to_text(word_list, tol=3):
                        rows = defaultdict(list)
                        for w in word_list:
                            top = round(w['top'] / tol) * tol
                            rows[top].append(w)
                        lines = []
                        for top in sorted(rows.keys()):
                            row_words = sorted(rows[top], key=lambda w: w['x0'])
                            lines.append(" ".join(w['text'] for w in row_words))
                        return "\n".join(lines)
                    page_text = col_to_text(right_words) + "\n" + col_to_text(left_words)
                else:
                    page_text = page.extract_text() or ""
                text += page_text + "\n"
        if text.strip():
            return text.strip()
    except Exception:
        pass
    try:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception:
        pass
    return text


def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


# ── NAME EXTRACTION ──────────────────────────────────────────

def is_valid_name(line: str):
    clean = line.strip()
    for pfx in NAME_PREFIXES:
        if clean.lower().startswith(pfx):
            clean = clean[len(pfx):].strip()
            break
    if re.match(r"(?i)^name\s*[:\-]\s*", clean):
        clean = re.sub(r"(?i)^name\s*[:\-]\s*", "", clean).strip()
    words = clean.split()
    return (
        2 <= len(words) <= 4
        and re.match(r"^[A-Za-z\s.\-]+$", clean)
        and not any(k in clean.lower() for k in SKIP_KEYWORDS)
        and all(w[0].isupper() for w in words if w)
        and not any(c in clean for c in ["|", "@", "/", ":", "+"])
    ), clean


def extract_name(raw_text: str, nlp) -> str:
    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
    if lines:
        valid, clean = is_valid_name(lines[0])
        if valid:
            return clean
    doc = nlp(raw_text[:800])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            valid, clean = is_valid_name(ent.text.strip())
            if valid:
                return clean
    for line in lines[1:8]:
        valid, clean = is_valid_name(line)
        if valid:
            return clean
    return "Not Found"


# ── CONTACT EXTRACTION ───────────────────────────────────────

def extract_email(text: str) -> str:
    m = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return m[0] if m else "Not Found"


def extract_phone(text: str) -> str:
    for p in [r"(\+91[\s\-]?)?[6-9]\d{9}", r"\+?[\d\s\-\(\)]{10,15}"]:
        m = re.findall(p, text)
        if m:
            number = ''.join(filter(str.isdigit, m[0]))
            if len(number) >= 10:
                return m[0] if isinstance(m[0], str) else ''.join(m[0])
    return "Not Found"


def extract_linkedin(text: str) -> str:
    m = re.findall(r"linkedin\.com/in/[a-zA-Z0-9\-]+", text)
    return m[0] if m else "Not Found"


def extract_github(text: str) -> str:
    m = re.findall(r"github\.com/[a-zA-Z0-9\-]+", text)
    return m[0] if m else "Not Found"


# ── SKILLS ───────────────────────────────────────────────────

def extract_skills(text: str) -> list:
    found      = []
    text_lower = text.lower()
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill.title())
    return list(dict.fromkeys(found)) if found else ["Not Found"]


def extract_expected_skills(jd_text: str) -> list:
    """Extract skills expected/required from the job description."""
    return extract_skills(jd_text)


# ── SECTION EXTRACTION ───────────────────────────────────────

def extract_section(text: str, section_headers: list, stop_headers: list) -> list:
    lines      = text.split('\n')
    collecting = False
    content    = []
    for line in lines:
        line_lower = line.lower().strip()
        if collecting and any(h in line_lower for h in stop_headers):
            break
        if any(h in line_lower for h in section_headers):
            collecting = True
            continue
        if collecting and line.strip() and len(line.strip()) > 2:
            content.append(line.strip())
    return content


# ── FULL RESUME PARSER ───────────────────────────────────────

def parse_resume(text: str, nlp) -> dict:
    name     = extract_name(text, nlp)
    raw_text = text
    text     = clean_text(text)

    def edu(_):
        degree_keywords = ["b.tech","b.e","b.sc","m.tech","m.sc","phd","bachelor",
                           "master","diploma","cgpa","gpa","university","college","institute"]
        lns = extract_section(raw_text, ["education","academic","qualification"],
                              ["experience","internship","skill","project","certification",
                               "achievement","objective","summary"])
        for tl in raw_text.split('\n'):
            tl = tl.strip()
            if (any(k in tl.lower() for k in degree_keywords)
                    and tl not in lns and 5 < len(tl) < 200
                    and not re.search(r'@|\+91|http|linkedin|github', tl, re.IGNORECASE)):
                lns.append(tl)
        return list(dict.fromkeys(lns))[:6] or ["Not Found"]

    def exp(_):
        lns = extract_section(raw_text, ["experience","internship","employment","work history"],
                              ["education","skill","project","certification",
                               "achievement","objective","summary","declaration"])
        for tl in raw_text.split('\n'):
            tl = tl.strip()
            if (re.search(r'(20\d{2})\s*[-–]\s*(20\d{2}|present)', tl, re.IGNORECASE)
                    and tl not in lns and len(tl) > 5):
                lns.append(tl)
        cleaned = [l for l in list(dict.fromkeys(lns)) if len(l.split()) <= 20]
        return cleaned[:6] or ["Not Found"]

    def proj(_):
        return extract_section(raw_text, ["project","projects"],
                               ["experience","education","skill","certification"])[:6] or ["Not Found"]

    def ach(_):
        lns = extract_section(raw_text, ["achievement","award","honor"],
                              ["education","skill","project","certification"])
        for tl in raw_text.split('\n'):
            tl = tl.strip()
            if (any(k in tl.lower() for k in ["award","winner","rank","1st","merit",
                                               "scholarship","gold","hackathon","published"])
                    and tl not in lns and len(tl) > 5):
                lns.append(tl)
        return list(dict.fromkeys(lns))[:5] or ["Not Found"]

    def cert(_):
        lns = extract_section(raw_text, ["certification","certificate","course"],
                              ["education","skill","project","achievement"])
        for tl in raw_text.split('\n'):
            tl = tl.strip()
            if (any(k in tl.lower() for k in ["udemy","coursera","nptel","google",
                                               "microsoft","aws","ibm","certified"])
                    and tl not in lns and len(tl) > 5):
                lns.append(tl)
        return list(dict.fromkeys(lns))[:5] or ["Not Found"]

    return {
        "Name":           name,
        "Email":          extract_email(text),
        "Phone":          extract_phone(text),
        "LinkedIn":       extract_linkedin(text),
        "GitHub":         extract_github(text),
        "Skills":         extract_skills(text),
        "Education":      edu(text),
        "Experience":     exp(text),
        "Projects":       proj(text),
        "Achievements":   ach(text),
        "Certifications": cert(text),
    }
