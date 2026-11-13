# HireRight-AI

AI-powered resume screening tool that helps recruiters parse resumes, score candidates against a job description, and export ranked reports.

## Features

- Upload resumes (PDF/DOCX) and extract text automatically
- Parse key details: skills, education, experience
- Score and rank candidates against a job description
- Interactive dashboard to compare candidates
- Export results as reports (CSV/PDF)
- Team view for shared candidate review

## Tech Stack

- **Language:** Python
- **UI:** Streamlit
- **NLP/AI:** [spaCy / scikit-learn / LLM API: fill in]
- **Data:** [SQL / Pandas: fill in]
- **Version control:** Git, GitHub

## How It Works

Upload → Parse (`parser.py`) → Model (`model.py`) → Score (`pipeline.py`) → Dashboard & Report

## Project Structure

| File | Purpose |
|------|---------|
| `app.py` | Main entry point of the Streamlit app |
| `home.py` | Home page |
| `upload.py` | Resume upload handling |
| `parser.py` | Extracts text and details from resumes |
| `model.py` | Scoring / matching model |
| `pipeline.py` | Connects parsing, model and scoring steps |
| `candidate.py` | Candidate data handling |
| `dashboard.py` | Candidate comparison dashboard |
| `report.py` / `exports.py` | Report generation and export |
| `team.py` | Team collaboration view |
| `styles.py` | UI styling |
| `config.py` | App settings |

## Installation

```bash
git clone https://github.com/Seema-N-C/HireRight-AI.git
cd HireRight-AI
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Open the app and go to the upload page
2. Upload one or more resumes
3. Enter or paste the job description
4. View scores and rankings on the dashboard
5. Export the report

## Screenshots



![Dashboard](screenshots/dashboard.png)




![Results](screenshots/results.png)



## Future Improvements

- Support more resume formats and languages
- Add bias checks and explainable scoring
- Deploy online (Streamlit Cloud / Docker)

## Author

**Seema N C**
GitHub: [Seema-N-C](https://github.com/Seema-N-C)
LinkedIn: [add your link]
