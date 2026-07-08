# SkillGap AI – README

<div align="center">

```
╔══════════════════════════════════════════════════════════════════════╗
║          SkillGap AI — Intelligent Resume Analysis Platform          ║
║       AI-Powered Career Intelligence | NLP + Machine Learning        ║
╚══════════════════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)

**An intelligent career assistant that uses NLP and ML to analyze resumes,
identify skill gaps, predict job roles, and recommend personalized learning resources.**

</div>

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd SkillGap_AI
pip install -r requirements.txt
```

### 2. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
SkillGap_AI/
├── app.py                        # Main Streamlit app (entry point)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── resume_parser/
│   ├── pdf_parser.py             # PDF extraction (pdfplumber)
│   ├── docx_parser.py            # DOCX extraction (python-docx)
│   └── extractor.py              # NLP info extraction (name, email, skills)
│
├── skills/
│   ├── skill_database.py         # Skill DB loader (loads data/skills_db.json)
│   └── skill_extractor.py        # spaCy + keyword skill matching
│
├── analysis/
│   ├── tfidf_analyzer.py         # TF-IDF + Cosine Similarity
│   ├── ats_scorer.py             # ATS score calculator (7 criteria)
│   └── gap_analyzer.py           # Skill gap analysis pipeline
│
├── ml/
│   ├── model_trainer.py          # RandomForest training on synthetic data
│   └── job_predictor.py          # Job role prediction with confidence scores
│
├── recommendation/
│   └── recommender.py            # Course recommendations + learning roadmaps
│
├── visualization/
│   └── charts.py                 # Plotly charts (gauge, radar, bar, pie)
│
├── utils/
│   ├── text_preprocessor.py      # NLTK text cleaning & tokenization
│   ├── report_generator.py       # ReportLab PDF report generation
│   └── logger.py                 # Centralized logging
│
├── data/
│   ├── skills_db.json            # Curated skills for 11 job roles
│   └── courses_db.json           # 50+ course recommendations
│
├── models/                       # Auto-generated ML model files
│   ├── job_role_model.pkl
│   ├── all_skills.pkl
│   └── label_encoder.pkl
│
└── assets/
    └── style.css                 # Custom dark theme CSS
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Parsing** | Extract name, email, phone, skills, education, experience from PDF/DOCX |
| 🔍 **Skill Gap Analysis** | TF-IDF + Cosine Similarity matching against job descriptions |
| 🤖 **ML Job Prediction** | RandomForest predicts top-5 suitable job roles with confidence scores |
| 🎯 **ATS Score** | 7-criteria ATS compatibility scoring (Skills, Keywords, Experience, Education, Format, Projects, Certs) |
| 📚 **Course Recommendations** | Personalized courses from Coursera, Udemy, Kaggle, freeCodeCamp, etc. |
| 🗺️ **Learning Roadmap** | Step-by-step learning path for each predicted role |
| 📊 **Interactive Dashboard** | Plotly radar charts, gauge meters, pie charts, and bar charts |
| 📥 **PDF Report** | Downloadable analysis report via ReportLab |

---

## 🛠️ Tech Stack

- **Web Framework**: Streamlit
- **NLP**: spaCy, NLTK, TF-IDF Vectorizer, Cosine Similarity
- **Machine Learning**: scikit-learn (RandomForestClassifier)
- **Resume Parsing**: pdfplumber, python-docx
- **Visualization**: Plotly
- **PDF Generation**: ReportLab
- **Data Processing**: pandas, numpy

---

## 🤖 ML Model Details

- **Algorithm**: RandomForestClassifier (`n_estimators=200, max_depth=15`)
- **Training Data**: Synthetic skill-role mappings (550 samples × 11 roles)
- **Feature Space**: Binary skill presence vector (150+ skills)
- **Accuracy**: ~95%+ on synthetic test set
- **Job Roles**: Data Analyst, Data Scientist, ML Engineer, Software Engineer, Full Stack Developer, Frontend Developer, Backend Developer, DevOps Engineer, Cloud Engineer, AI Engineer, Cybersecurity Analyst

---

## 📊 Application Pages

1. **🏠 Home** – Overview, features, workflow, and tech stack
2. **📄 Resume Upload** – Upload PDF/DOCX or paste text; view extracted info
3. **📋 Job Description** – Paste or upload JD for comparison
4. **🔍 Skill Analysis** – Matching/missing skills with visual charts
5. **🎯 ATS Score** – 7-criteria scoring with improvement tips
6. **🤖 Job Prediction** – ML-based top-5 role predictions
7. **📚 Learning Recommendations** – Courses, roadmap, practice platforms
8. **📊 Dashboard** – Complete analytics overview with PDF download

---

## 📋 Requirements

```
Python 3.9+
streamlit>=1.28.0
pdfplumber>=0.10.0
python-docx>=1.1.0
spacy>=3.7.0
nltk>=3.8.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
reportlab>=4.0.0
```

---

## 🎓 Use Cases

- **Students** – Prepare for campus placements
- **Job Seekers** – Optimize resume for specific job descriptions
- **Career Changers** – Identify skill gaps for new domains
- **Professionals** – Track career readiness and learning progress

---

## 👤 Author

Built as a Production-quality ML Portfolio Project using:
Python · Streamlit · scikit-learn · spaCy · NLTK · Plotly · ReportLab

---

*SkillGap AI v1.0 – AI-Powered Career Intelligence Platform*
