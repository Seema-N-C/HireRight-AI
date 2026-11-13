# HireRight AI

AI-powered recruitment and candidate analytics system. It parses resumes, matches them to a job description using semantic similarity, ranks candidates, and generates reports.



![Dashboard](screenshots/dashboard.jpg)



## Features

- Upload multiple resumes (PDF/DOCX) with a job description
- Resume parsing: name, email, phone, skills, education, experience
- Semantic matching using RoBERTa-based sentence embeddings and cosine similarity
- Suitability prediction (Shortlisted / Under Review / Rejected) with Logistic Regression
- Candidate ranking, skill gap analysis and interactive analytics dashboard
- Job role recommendations for rejected candidates (API-based)
- Automated PDF report and CSV export

## Tech Stack

- **Language:** Python
- **UI:** Streamlit
- **NLP:** spaCy, Sentence Transformers (RoBERTa/MPNet)
- **ML:** scikit-learn (cosine similarity, Logistic Regression)
- **Data:** Pandas, NumPy, CSV storage
- **Parsing:** PyPDF2, python-docx
- **Visualization and reports:** Plotly, Matplotlib, ReportLab

## How It Works

Upload → Resume Parsing → NLP Preprocessing → RoBERTa Embeddings → Cosine Similarity → Logistic Regression → Final Score → Ranking → Dashboard and Report



![Architecture](screenshots/architecture.jpg)



## Screenshots

### Candidate Rankings


![Rankings](screenshots/rankings.jpg)



### Visual Analytics


![Analytics](screenshots/visual-analytics.jpg)



### Skill Gap Analysis


![Skill Gap](screenshots/skill-gap.png)



### Job Recommendations


![Jobs](screenshots/job-recommendations.jpg)



### Model Performance (ROC AUC = 0.8425)


![ROC](screenshots/roc-curve.png)



## Project Structure

| File | Purpose |
|------|---------|
| `app.py` | Streamlit entry point |
| `home.py` | Home page |
| `upload.py` | Resume and job description upload |
| `parser.py` | Resume text and detail extraction |
| `model.py` | Embeddings, similarity and suitability model |
| `pipeline.py` | Connects all processing steps |
| `candidate.py` | Candidate detail view |
| `dashboard.py` | Rankings and analytics |
| `report.py` / `exports.py` | PDF report and CSV export |
| `team.py` | Team page |
| `styles.py` | UI styling |
| `config.py` | Settings |

## Installation

```bash
git clone https://github.com/Seema-N-C/HireRight-AI.git
cd HireRight-AI
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

## Usage

1. Open **Upload & Analyze** and upload resumes
2. Enter the job description
3. View rankings and skill gaps on the **Dashboard**
4. Open **Candidate Detail** for a single profile
5. Download the PDF report from **Report**

## Team

Built as a team project during the Python & AI Internship at Genplus Training & Consulting Services.

Md Furhan Pasha, Rakshith Krishna Murthy, Ajith B, **Seema N C**, Gokul Adithya, Diya Dadheech, Disha S Reddy

My contribution: NLP Processing , Feature Engineering modules and API handling

## Future Improvements

- Integrate LLMs for deeper semantic understanding
- Multi-language resume support
- Cloud deployment and LinkedIn integration

## Author

**Seema N C** · [GitHub](https://github.com/Seema-N-C) 
