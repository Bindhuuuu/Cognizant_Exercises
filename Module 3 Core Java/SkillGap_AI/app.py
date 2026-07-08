"""
╔══════════════════════════════════════════════════════════════════════╗
║          SkillGap AI — Intelligent Resume Analysis Platform          ║
║       AI-Powered Career Intelligence | NLP + Machine Learning        ║
╚══════════════════════════════════════════════════════════════════════╝

Main Streamlit application entry point.
Run with: streamlit run app.py

Modules:
  - resume_parser  : PDF/DOCX parsing and information extraction
  - skills         : Skill extraction and database lookup
  - analysis       : TF-IDF, cosine similarity, ATS scoring, gap analysis
  - ml             : Job role prediction (RandomForest)
  - recommendation : Personalized course and learning recommendations
  - visualization  : Plotly interactive charts
  - utils          : Text preprocessing, logging, PDF report generation
"""

import os
import sys
import time
import streamlit as st

# ── Add project root to path ─────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkillGap AI – Career Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "About": "SkillGap AI – AI-Powered Resume Analysis & Career Intelligence Platform v1.0"
    }
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ── Sidebar navigation font fix (inline override) ─────────────────────────────
st.markdown("""
<style>
/* Force sidebar radio labels to be fully visible */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stRadio label > div,
section[data-testid="stSidebar"] .stRadio label > div > p {
    color: #E2E8F0 !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    opacity: 1 !important;
    visibility: visible !important;
}
section[data-testid="stSidebar"] .stRadio label:hover,
section[data-testid="stSidebar"] .stRadio label:hover p {
    color: #FFFFFF !important;
    background: rgba(102,126,234,0.18) !important;
    border-radius: 10px !important;
}
/* Selected item highlight */
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label,
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}
/* Sidebar general text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: #CBD5E1 !important;
    font-family: 'Inter', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ── Lazy imports (avoid loading unused heavy modules) ─────────────────────────
@st.cache_resource(show_spinner=False)
def get_imports():
    """Cache heavy imports to speed up navigation."""
    from resume_parser.pdf_parser import extract_text_from_pdf
    from resume_parser.docx_parser import extract_text_from_docx
    from resume_parser.extractor import extract_resume_info
    from skills.skill_extractor import extract_skills_from_text, compare_skills
    from analysis.tfidf_analyzer import compute_similarity
    from analysis.ats_scorer import calculate_ats_score
    from analysis.gap_analyzer import analyze_skill_gap, get_readiness_score
    from ml.job_predictor import predict_job_roles
    from recommendation.recommender import (
        recommend_courses, get_learning_roadmap, get_practice_platforms
    )
    from utils.report_generator import generate_pdf_report
    import visualization.charts as charts
    return {
        "extract_text_from_pdf": extract_text_from_pdf,
        "extract_text_from_docx": extract_text_from_docx,
        "extract_resume_info": extract_resume_info,
        "extract_skills_from_text": extract_skills_from_text,
        "compare_skills": compare_skills,
        "compute_similarity": compute_similarity,
        "calculate_ats_score": calculate_ats_score,
        "analyze_skill_gap": analyze_skill_gap,
        "get_readiness_score": get_readiness_score,
        "predict_job_roles": predict_job_roles,
        "recommend_courses": recommend_courses,
        "get_learning_roadmap": get_learning_roadmap,
        "get_practice_platforms": get_practice_platforms,
        "generate_pdf_report": generate_pdf_report,
        "charts": charts,
    }


# ── Session State Initialization ─────────────────────────────────────────────
def init_session():
    defaults = {
        "resume_text": "",
        "jd_text": "",
        "extracted_info": {},
        "resume_skills": [],
        "jd_skills": [],
        "gap_analysis": {},
        "ats_result": {},
        "job_prediction": {},
        "recommendations": [],
        "roadmap": [],
        "analysis_done": False,
        "candidate_name": "",
        "analysis_history": [],
        "dark_mode": True,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 2rem;">
            <div style="font-size:3rem; margin-bottom:0.3rem;">🎯</div>
            <div style="font-size:1.6rem; font-weight:800;
                background: linear-gradient(135deg, #667EEA, #764BA2);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                SkillGap AI
            </div>
            <div style="font-size:0.75rem; color:#94A3B8; margin-top:0.2rem;">
                Career Intelligence Platform
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        pages = {
            "🏠 Home": "Home",
            "📄 Resume Upload": "Resume Upload",
            "📋 Job Description": "Job Description",
            "🔍 Skill Analysis": "Skill Analysis",
            "🎯 ATS Score": "ATS Score",
            "🤖 Job Prediction": "Job Prediction",
            "📚 Learning Recommendations": "Learning Recommendations",
            "📊 Dashboard": "Dashboard",
        }

        selected = st.radio(
            "Navigate",
            list(pages.keys()),
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Analysis Status Indicator
        if st.session_state.analysis_done:
            st.markdown("""
            <div style="background:rgba(0,204,136,0.1); border:1px solid rgba(0,204,136,0.3);
                border-radius:10px; padding:0.8rem; text-align:center;">
                <div style="color:#00CC88; font-weight:600; font-size:0.85rem;">
                    ✅ Analysis Ready
                </div>
                <div style="color:#94A3B8; font-size:0.75rem; margin-top:0.2rem;">
                    Navigate to any page
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,165,0,0.1); border:1px solid rgba(255,165,0,0.3);
                border-radius:10px; padding:0.8rem; text-align:center;">
                <div style="color:#FFA500; font-weight:600; font-size:0.85rem;">
                    ⚠️ Upload Resume First
                </div>
                <div style="color:#94A3B8; font-size:0.75rem; margin-top:0.2rem;">
                    Start at Resume Upload
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Reset button
        if st.button("🔄 Reset Analysis", use_container_width=True):
            for key in ["resume_text", "jd_text", "extracted_info", "resume_skills",
                        "jd_skills", "gap_analysis", "ats_result", "job_prediction",
                        "recommendations", "roadmap", "analysis_done", "candidate_name"]:
                st.session_state[key] = {} if key in ["extracted_info", "gap_analysis",
                                                        "ats_result", "job_prediction"] else \
                                        [] if key in ["resume_skills", "jd_skills",
                                                       "recommendations", "roadmap"] else \
                                        False if key == "analysis_done" else ""
            st.success("Analysis reset!")
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; color:#475569; font-size:0.7rem;">
            SkillGap AI v1.0<br>Built with ❤️ using Python + Streamlit
        </div>
        """, unsafe_allow_html=True)

    return pages[selected]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    # Hero Banner
    st.markdown("""
    <div class="hero-banner fade-in">
        <div style="font-size:4rem; margin-bottom:1rem;">🎯</div>
        <h1 style="font-size:3rem; margin:0; font-weight:900;
            background:linear-gradient(135deg,#667EEA,#764BA2,#F093FB);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            SkillGap AI
        </h1>
        <p style="font-size:1.2rem; color:#94A3B8; margin-top:0.8rem; max-width:600px; margin:0.8rem auto;">
            Intelligent Resume Analysis & Personalized Career Intelligence Platform
        </p>
        <p style="color:#64748B; font-size:0.9rem; margin-top:0.5rem;">
            Powered by NLP · Machine Learning · TF-IDF · Cosine Similarity · RandomForest
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Statistics row
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("11", "Job Roles", "🎯"),
        ("100+", "Skills Tracked", "⚡"),
        ("7", "Analysis Criteria", "📊"),
        ("50+", "Learning Resources", "📚"),
    ]
    for col, (val, label, icon) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:2rem; margin-bottom:0.3rem;">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Features Grid
    st.markdown("### 🚀 Key Features")
    fc1, fc2, fc3 = st.columns(3)
    features = [
        ("📄", "Smart Resume Parsing", "Extract name, email, skills, education, experience from PDF/DOCX with NLP"),
        ("🔍", "Skill Gap Analysis", "TF-IDF + Cosine Similarity to precisely identify matching and missing skills"),
        ("🤖", "ML Job Prediction", "RandomForest classifier predicts your best-fit job roles with confidence scores"),
        ("🎯", "ATS Score", "Get your ATS compatibility score out of 100 with actionable improvement tips"),
        ("📚", "Smart Recommendations", "Personalized courses from Coursera, Udemy, Kaggle based on your gaps"),
        ("📊", "Interactive Dashboard", "Plotly-powered radar charts, gauge meters, and visual analytics"),
    ]
    for i, (icon, title, desc) in enumerate(features):
        with [fc1, fc2, fc3][i % 3]:
            st.markdown(f"""
            <div class="metric-card" style="text-align:left; margin-bottom:1rem;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:700; color:#E2E8F0; margin-bottom:0.3rem;">{title}</div>
                <div style="font-size:0.85rem; color:#94A3B8;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Workflow
    st.markdown("### 🔄 How It Works")
    steps = [
        ("1", "Upload Resume", "PDF or DOCX", "📄"),
        ("2", "Paste Job Description", "Target role JD", "📋"),
        ("3", "AI Analysis", "NLP + ML processing", "🤖"),
        ("4", "Get Results", "Scores, gaps, predictions", "📊"),
        ("5", "Learn & Improve", "Personalized roadmap", "🚀"),
    ]
    cols = st.columns(len(steps))
    for col, (num, title, sub, icon) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:1rem;">
                <div style="width:50px;height:50px;border-radius:50%;
                    background:linear-gradient(135deg,#667EEA,#764BA2);
                    display:flex;align-items:center;justify-content:center;
                    margin:0 auto 0.5rem; font-weight:800; color:white; font-size:1.1rem;">
                    {num}
                </div>
                <div style="font-size:1.5rem; margin-bottom:0.3rem;">{icon}</div>
                <div style="font-weight:700; color:#E2E8F0; font-size:0.9rem;">{title}</div>
                <div style="color:#94A3B8; font-size:0.75rem;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tech Stack
    st.markdown("### 🛠️ Technology Stack")
    tc1, tc2, tc3, tc4 = st.columns(4)
    tech = [
        ("🐍 Python", "Core Language"),
        ("⚡ Streamlit", "Web Framework"),
        ("🤖 scikit-learn", "Machine Learning"),
        ("📝 spaCy / NLTK", "NLP Processing"),
        ("📊 Plotly", "Visualizations"),
        ("📄 pdfplumber", "PDF Parsing"),
        ("🔢 TF-IDF", "Text Similarity"),
        ("🌲 RandomForest", "Job Prediction"),
    ]
    for i, (name, cat) in enumerate(tech):
        with [tc1, tc2, tc3, tc4][i % 4]:
            st.markdown(f"""
            <div style="background:rgba(42,42,62,0.8); border:1px solid rgba(102,126,234,0.2);
                border-radius:10px; padding:0.8rem; text-align:center; margin-bottom:0.8rem;">
                <div style="font-size:0.9rem; font-weight:600; color:#E2E8F0;">{name}</div>
                <div style="font-size:0.75rem; color:#94A3B8;">{cat}</div>
            </div>
            """, unsafe_allow_html=True)

    # CTA
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 **Get Started**: Click **Resume Upload** in the sidebar to begin your career analysis!")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: RESUME UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
def page_resume_upload():
    mods = get_imports()
    
    st.markdown("## 📄 Resume Upload & Parsing")
    st.markdown("Upload your resume in PDF or DOCX format to extract structured information.")

    col_upload, col_preview = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown("### 📂 Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Choose a PDF or DOCX file",
            type=["pdf", "docx"],
            help="Upload your resume in PDF or DOCX format (max 200MB)"
        )

        if uploaded_file:
            file_size_kb = uploaded_file.size / 1024
            st.markdown(f"""
            <div style="background:rgba(0,204,136,0.1);border:1px solid rgba(0,204,136,0.3);
                border-radius:10px; padding:0.8rem; margin:0.5rem 0;">
                <strong style="color:#00CC88;">✅ File uploaded successfully!</strong><br>
                <span style="color:#94A3B8; font-size:0.85rem;">
                    {uploaded_file.name} · {file_size_kb:.1f} KB · {uploaded_file.type}
                </span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Parse Resume", use_container_width=True):
                with st.spinner("🔍 Analyzing your resume with NLP..."):
                    file_bytes = uploaded_file.read()
                    
                    # Extract text based on file type
                    if uploaded_file.type == "application/pdf" or uploaded_file.name.endswith(".pdf"):
                        raw_text = mods["extract_text_from_pdf"](file_bytes)
                    else:
                        raw_text = mods["extract_text_from_docx"](file_bytes)
                    
                    if not raw_text.strip():
                        st.error("❌ Could not extract text from the file. Please try a different file.")
                        return
                    
                    # Extract structured info
                    extracted = mods["extract_resume_info"](raw_text)
                    
                    # Extract skills
                    skill_data = mods["extract_skills_from_text"](raw_text)
                    
                    # Save to session state
                    st.session_state.resume_text = raw_text
                    st.session_state.extracted_info = extracted
                    st.session_state.resume_skills = skill_data["all"]
                    st.session_state.candidate_name = extracted.get("name", "Candidate")
                    
                    time.sleep(0.5)
                    st.success(f"✅ Resume parsed! Found {len(skill_data['all'])} skills.")
                    st.rerun()

        # Manual text input option
        st.markdown("#### Or Paste Resume Text")
        manual_text = st.text_area(
            "Paste your resume content here",
            height=200,
            placeholder="Paste your resume text here if you don't have a PDF/DOCX file...",
            label_visibility="collapsed"
        )
        if manual_text and st.button("📝 Process Text", use_container_width=True):
            with st.spinner("Processing..."):
                extracted = mods["extract_resume_info"](manual_text)
                skill_data = mods["extract_skills_from_text"](manual_text)
                st.session_state.resume_text = manual_text
                st.session_state.extracted_info = extracted
                st.session_state.resume_skills = skill_data["all"]
                st.session_state.candidate_name = extracted.get("name", "Candidate")
                st.success("✅ Resume text processed!")
                st.rerun()

    with col_preview:
        if st.session_state.extracted_info:
            info = st.session_state.extracted_info
            
            st.markdown("### 👤 Extracted Information")
            
            # Contact card
            st.markdown(f"""
            <div class="metric-card" style="text-align:left;">
                <div style="font-size:1.2rem; font-weight:800; color:#E2E8F0; margin-bottom:1rem;">
                    👤 {info.get('name', 'Candidate')}
                </div>
                <div style="color:#94A3B8; font-size:0.85rem; line-height:1.8;">
                    📧 {info.get('email', 'Not found')}<br>
                    📱 {info.get('phone', 'Not found')}<br>
                    🔗 {info.get('linkedin', 'Not found')}<br>
                    🐙 {info.get('github', 'Not found')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Skills found
            tech_skills = mods["extract_skills_from_text"](st.session_state.resume_text)["technical"][:20]
            soft_skills = mods["extract_skills_from_text"](st.session_state.resume_text)["soft"][:10]
            
            if tech_skills:
                st.markdown("**⚡ Technical Skills Found:**")
                tags_html = "".join([f'<span class="skill-tag skill-tag-tech">{s}</span>' for s in tech_skills])
                st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
            
            if soft_skills:
                st.markdown("**🤝 Soft Skills Found:**")
                tags_html = "".join([f'<span class="skill-tag skill-tag-soft">{s}</span>' for s in soft_skills])
                st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Education
            education = info.get("education", [])
            if education and education != ["Not found"]:
                with st.expander("🎓 Education", expanded=False):
                    for edu in education[:6]:
                        if edu:
                            st.markdown(f"• {edu}")
            
            # Experience
            experience = info.get("experience", [])
            if experience and experience != ["Not found"]:
                with st.expander("💼 Experience", expanded=False):
                    for exp in experience[:8]:
                        if exp:
                            st.markdown(f"• {exp}")
            
            # Projects
            projects = info.get("projects", [])
            if projects and projects != ["Not found"]:
                with st.expander("🛠️ Projects", expanded=False):
                    for proj in projects[:5]:
                        if proj:
                            st.markdown(f"• {proj}")
            
            # Certifications
            certs = info.get("certifications", [])
            if certs and certs != ["Not found"]:
                with st.expander("🏅 Certifications", expanded=False):
                    for cert in certs[:5]:
                        if cert:
                            st.markdown(f"• {cert}")
        else:
            st.markdown("""
            <div style="text-align:center; padding:3rem; color:#475569;">
                <div style="font-size:4rem; margin-bottom:1rem;">📄</div>
                <div style="font-size:1rem;">Upload a resume to see extracted information here</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: JOB DESCRIPTION
# ══════════════════════════════════════════════════════════════════════════════
def page_job_description():
    mods = get_imports()
    
    st.markdown("## 📋 Job Description Input")
    st.markdown("Paste or upload the job description to compare against your resume.")

    tab1, tab2 = st.tabs(["📝 Paste JD Text", "📂 Upload JD File"])

    with tab1:
        jd_text = st.text_area(
            "Job Description",
            value=st.session_state.jd_text,
            height=350,
            placeholder="""Paste the full job description here...

Example:
We are looking for a Data Scientist to join our team.

Requirements:
- 3+ years experience with Python, R
- Strong knowledge of machine learning algorithms
- Experience with TensorFlow, PyTorch, scikit-learn
- Proficiency in SQL and data visualization
- Experience with cloud platforms (AWS/GCP)
- Strong statistics and mathematics background
...""",
            label_visibility="collapsed"
        )
        
        if jd_text and st.button("✅ Confirm Job Description", use_container_width=True):
            with st.spinner("Extracting JD skills..."):
                jd_skill_data = mods["extract_skills_from_text"](jd_text)
                st.session_state.jd_text = jd_text
                st.session_state.jd_skills = jd_skill_data["all"]
                st.success(f"✅ JD processed! Found {len(jd_skill_data['all'])} required skills.")
                
                # Run full analysis if resume is also uploaded
                if st.session_state.resume_text:
                    _run_full_analysis(mods)
                st.rerun()

    with tab2:
        jd_file = st.file_uploader(
            "Upload JD File",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed"
        )
        if jd_file:
            if jd_file.name.endswith(".txt"):
                jd_text_file = jd_file.read().decode("utf-8", errors="ignore")
            elif jd_file.name.endswith(".pdf"):
                jd_text_file = mods["extract_text_from_pdf"](jd_file.read())
            else:
                jd_text_file = mods["extract_text_from_docx"](jd_file.read())
            
            if st.button("🚀 Process JD File", use_container_width=True):
                with st.spinner("Processing JD file..."):
                    jd_skill_data = mods["extract_skills_from_text"](jd_text_file)
                    st.session_state.jd_text = jd_text_file
                    st.session_state.jd_skills = jd_skill_data["all"]
                    if st.session_state.resume_text:
                        _run_full_analysis(mods)
                    st.success("✅ JD file processed!")
                    st.rerun()

    # JD preview panel
    if st.session_state.jd_text:
        st.markdown("---")
        st.markdown("### 📊 JD Skill Analysis Preview")
        
        c1, c2 = st.columns(2)
        with c1:
            jd_skill_data = mods["extract_skills_from_text"](st.session_state.jd_text)
            tech = jd_skill_data["technical"][:15]
            if tech:
                st.markdown("**⚡ Technical Skills Required:**")
                tags = "".join([f'<span class="skill-tag skill-tag-tech">{s}</span>' for s in tech])
                st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)
        
        with c2:
            soft = jd_skill_data["soft"][:10]
            if soft:
                st.markdown("**🤝 Soft Skills Required:**")
                tags = "".join([f'<span class="skill-tag skill-tag-soft">{s}</span>' for s in soft])
                st.markdown(f"<div>{tags}</div>", unsafe_allow_html=True)

        if not st.session_state.resume_text:
            st.warning("⚠️ Please upload your resume first to run the comparison analysis!")
        elif st.session_state.analysis_done:
            st.success("✅ Full analysis completed! Navigate to **Skill Analysis** or **Dashboard** to see results.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SKILL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
def page_skill_analysis():
    mods = get_imports()
    charts = mods["charts"]

    st.markdown("## 🔍 Skill Gap Analysis")

    if not st.session_state.analysis_done:
        if not st.session_state.resume_text:
            st.warning("⚠️ Please upload your resume first!")
            return
        if not st.session_state.jd_text:
            st.warning("⚠️ Please enter a Job Description first!")
            return
        with st.spinner("Running skill gap analysis..."):
            _run_full_analysis(mods)
        st.rerun()

    gap = st.session_state.gap_analysis
    
    # Key metrics row
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        (f"{gap.get('match_percentage', 0):.1f}%", "Skill Match", "🎯"),
        (str(gap.get("matching_count", 0)), "Matching Skills", "✅"),
        (str(gap.get("missing_count", 0)), "Missing Skills", "❌"),
        (f"{gap.get('tfidf_similarity', 0):.1f}%", "TF-IDF Similarity", "📊"),
    ]
    for col, (val, label, icon) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.8rem;">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row
    ch1, ch2 = st.columns(2)
    
    with ch1:
        # Skill match gauge
        fig_gauge = charts.gauge_chart(
            gap.get("match_percentage", 0),
            "Skill Match Percentage",
            suffix="%"
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with ch2:
        # Skills comparison pie
        matching = gap.get("matching_skills", [])
        missing = gap.get("missing_skills", [])
        if matching or missing:
            fig_pie = charts.skills_comparison_chart(matching, missing)
            st.plotly_chart(fig_pie, use_container_width=True)

    # Skill Tags
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.markdown("### ✅ Matching Skills")
        if matching:
            tags = "".join([f'<span class="skill-tag skill-tag-match">{s}</span>' for s in matching[:20]])
            st.markdown(f"<div style='line-height:2.5;'>{tags}</div>", unsafe_allow_html=True)
        else:
            st.info("No matching skills found.")
    
    with col_r:
        st.markdown("### ❌ Missing Skills")
        if missing:
            tags = "".join([f'<span class="skill-tag skill-tag-missing">{s}</span>' for s in missing[:20]])
            st.markdown(f"<div style='line-height:2.5;'>{tags}</div>", unsafe_allow_html=True)
        else:
            st.success("🎉 Great! You have all the required skills!")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technical vs Soft skills breakdown
    col_tech, col_soft = st.columns(2)
    
    with col_tech:
        st.markdown("### ⚡ Your Technical Skills")
        tech_skills = gap.get("resume_technical_skills", [])[:20]
        if tech_skills:
            tags = "".join([f'<span class="skill-tag skill-tag-tech">{s}</span>' for s in tech_skills])
            st.markdown(f"<div style='line-height:2.5;'>{tags}</div>", unsafe_allow_html=True)
        else:
            st.info("No technical skills extracted.")
    
    with col_soft:
        st.markdown("### 🤝 Your Soft Skills")
        soft_skills = gap.get("resume_soft_skills", [])[:15]
        if soft_skills:
            tags = "".join([f'<span class="skill-tag skill-tag-soft">{s}</span>' for s in soft_skills])
            st.markdown(f"<div style='line-height:2.5;'>{tags}</div>", unsafe_allow_html=True)
        else:
            st.info("No soft skills extracted.")

    # Radar chart for skill coverage
    st.markdown("---")
    st.markdown("### 📡 Skill Coverage Radar")
    
    from skills.skill_database import get_all_job_roles, get_skills_for_role
    resume_set = set(st.session_state.resume_skills)
    
    categories = []
    coverages = []
    for role in get_all_job_roles()[:8]:
        role_data = get_skills_for_role(role)
        role_skills = set(role_data.get("technical", []) + role_data.get("soft", []))
        if role_skills:
            cov = len(resume_set & role_skills) / len(role_skills) * 100
            categories.append(role.replace(" Engineer", " Eng.").replace(" Developer", " Dev."))
            coverages.append(round(cov, 1))
    
    if categories and coverages:
        fig_radar = charts.radar_chart(categories, coverages, "Skill Coverage Across Roles")
        st.plotly_chart(fig_radar, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ATS SCORE
# ══════════════════════════════════════════════════════════════════════════════
def page_ats_score():
    mods = get_imports()
    charts = mods["charts"]

    st.markdown("## 🎯 ATS Resume Score")
    st.markdown("Your ATS compatibility score measures how well your resume performs with Applicant Tracking Systems.")

    if not st.session_state.analysis_done:
        if not st.session_state.resume_text:
            st.warning("⚠️ Please upload your resume first!")
            return
        with st.spinner("Calculating ATS score..."):
            _run_full_analysis(mods)

    ats = st.session_state.ats_result
    total = ats.get("total_score", 0)
    grade = ats.get("grade", "N/A")
    category_scores = ats.get("category_scores", {})
    suggestions = ats.get("suggestions", [])

    # Score display
    col_score, col_detail = st.columns([1, 2], gap="large")
    
    with col_score:
        # Animated score ring
        color = "#00CC88" if total >= 70 else "#FFA500" if total >= 50 else "#FF6B6B"
        st.markdown(f"""
        <div class="metric-card" style="padding:2rem;">
            <div style="font-size:5rem; font-weight:900; text-align:center;
                background:linear-gradient(135deg, {color}, #764BA2);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                {total}
            </div>
            <div style="text-align:center; color:#94A3B8; font-size:1rem; margin-top:-0.5rem;">/100</div>
            <div style="text-align:center; margin-top:1rem;">
                <span style="background:rgba({','.join(str(int(color.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.15);
                    border:1px solid {color}; color:{color};
                    padding:0.3rem 1rem; border-radius:20px; font-weight:700; font-size:1.2rem;">
                    Grade: {grade}
                </span>
            </div>
            <div style="text-align:center; margin-top:1rem; color:#94A3B8;">
                {'🚀 Excellent ATS compatibility!' if total >= 80 else
                 '✅ Good score! Few improvements needed.' if total >= 60 else
                 '⚠️ Moderate score. Work on suggestions below.' if total >= 40 else
                 '🔴 Low score. Significant improvements needed.'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gauge chart
        fig_ats = charts.gauge_chart(total, "ATS Score", suffix="/100")
        st.plotly_chart(fig_ats, use_container_width=True)
    
    with col_detail:
        # Category scores
        st.markdown("### 📊 Score Breakdown")
        
        weights = ats.get("weights", {})
        for cat, score in category_scores.items():
            weight = weights.get(cat, 0)
            contrib = int(score * weight / 100)
            bar_color = "#00CC88" if score >= 70 else "#FFA500" if score >= 40 else "#FF6B6B"
            
            st.markdown(f"""
            <div style="margin-bottom:0.8rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
                    <span style="color:#E2E8F0; font-weight:600; text-transform:capitalize;">{cat}</span>
                    <span style="color:{bar_color}; font-weight:700;">{score}/100 · Contributes {contrib}pts</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(score / 100, 1.0))
        
        # ATS breakdown chart
        if category_scores:
            fig_breakdown = charts.ats_breakdown_chart(category_scores, weights)
            st.plotly_chart(fig_breakdown, use_container_width=True)

    # Improvement suggestions
    st.markdown("---")
    st.markdown("### 💡 Improvement Suggestions")
    
    if suggestions:
        cols = st.columns(2)
        for i, suggestion in enumerate(suggestions):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background:rgba(102,126,234,0.08); border-left:3px solid #667EEA;
                    border-radius:0 10px 10px 0; padding:0.8rem 1rem; margin-bottom:0.6rem;">
                    <span style="color:#E2E8F0; font-size:0.88rem;">{suggestion}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("🎉 Your resume looks great! Keep up the excellent work.")
    
    # Interview tips
    st.markdown("---")
    st.markdown("### 🎤 Interview Preparation Tips")
    tips = [
        "🔍 Research the company's tech stack and products thoroughly",
        "💬 Prepare the STAR method stories for behavioral questions",
        "🧠 Review your listed skills and be ready for technical questions",
        "📝 Prepare 2-3 questions to ask the interviewer",
        "🎯 Practice coding challenges on LeetCode for technical roles",
        "📊 Review your project metrics and be ready to discuss impact",
    ]
    t1, t2 = st.columns(2)
    for i, tip in enumerate(tips):
        with [t1, t2][i % 2]:
            st.markdown(f"<div style='color:#94A3B8; padding:0.3rem 0;'>• {tip}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: JOB PREDICTION
# ══════════════════════════════════════════════════════════════════════════════
def page_job_prediction():
    mods = get_imports()
    charts = mods["charts"]

    st.markdown("## 🤖 Job Role Prediction")
    st.markdown("Machine Learning (RandomForest) predicts the most suitable job roles based on your skills.")

    if not st.session_state.resume_skills:
        st.warning("⚠️ Please upload your resume first to get job predictions!")
        return

    # Run prediction if not done
    if not st.session_state.job_prediction:
        with st.spinner("🤖 Running ML job role prediction..."):
            prediction = mods["predict_job_roles"](st.session_state.resume_skills)
            st.session_state.job_prediction = prediction

    pred = st.session_state.job_prediction
    top_role = pred.get("predicted_role", "N/A")
    confidence = pred.get("confidence", 0)
    all_preds = pred.get("top_predictions", [])

    # Top prediction card
    conf_color = "#00CC88" if confidence >= 70 else "#FFA500" if confidence >= 40 else "#FF6B6B"
    
    st.markdown(f"""
    <div class="hero-banner" style="padding:2rem;">
        <div style="font-size:3rem; margin-bottom:0.5rem;">🎯</div>
        <div style="font-size:0.9rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.1em;">
            Best Match Job Role
        </div>
        <div style="font-size:2.5rem; font-weight:900; color:#E2E8F0; margin:0.5rem 0;">
            {top_role}
        </div>
        <div style="font-size:1rem; margin-top:0.5rem;">
            <span style="background:rgba({','.join(str(int(conf_color.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.15);
                border:1px solid {conf_color}; color:{conf_color};
                padding:0.4rem 1.2rem; border-radius:25px; font-weight:700;">
                {confidence:.1f}% Confidence
            </span>
        </div>
        <div style="color:#64748B; font-size:0.85rem; margin-top:0.8rem;">
            Based on {pred.get('total_skills_used', 0)} skills analyzed via RandomForest ML
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Top 5 predictions chart
    col_chart, col_list = st.columns([3, 2], gap="large")
    
    with col_chart:
        if all_preds:
            fig_roles = charts.job_role_bar_chart(all_preds)
            st.plotly_chart(fig_roles, use_container_width=True)
    
    with col_list:
        st.markdown("### 🏆 Top 5 Role Matches")
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        for i, pred_item in enumerate(all_preds[:5]):
            role = pred_item.get("role", "")
            conf = pred_item.get("confidence", 0)
            bar_color = "#667EEA" if i == 0 else "#94A3B8"
            
            st.markdown(f"""
            <div style="background:rgba(42,42,62,0.8); border:1px solid rgba(102,126,234,0.2);
                border-radius:12px; padding:1rem; margin-bottom:0.6rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:1.2rem; margin-right:0.5rem;">{medals[i]}</span>
                        <span style="font-weight:600; color:#E2E8F0;">{role}</span>
                    </div>
                    <span style="color:{bar_color}; font-weight:700;">{conf:.1f}%</span>
                </div>
                <div style="margin-top:0.4rem; background:rgba(255,255,255,0.1); border-radius:5px; height:4px;">
                    <div style="width:{min(conf,100)}%; background:linear-gradient(90deg,#667EEA,#764BA2); 
                        border-radius:5px; height:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Skills for top role
    if all_preds:
        top_matched = all_preds[0].get("matched_skills", [])
        if top_matched:
            st.markdown("---")
            st.markdown(f"### ✅ Your Skills Matching **{top_role}**")
            tags = "".join([f'<span class="skill-tag skill-tag-match">{s}</span>' for s in top_matched])
            st.markdown(f"<div style='line-height:2.5;'>{tags}</div>", unsafe_allow_html=True)
    
    # SHAP-style explanation (rule-based)
    with st.expander("🔬 Prediction Explanation (Explainable AI)", expanded=False):
        st.markdown(f"""
        **How was `{top_role}` predicted?**
        
        The RandomForest model analyzed your skill vector across **{pred.get('total_skills_used', 0)} 
        matched skills** from a feature space of 150+ skills. The model was trained on 
        synthetic skill-role mappings derived from industry standards.
        
        **Key factors driving this prediction:**
        - Your skill profile best matches the technical requirements of **{top_role}**
        - Confidence score of **{confidence:.1f}%** reflects ensemble agreement across 200 decision trees
        - The model uses stratified training data across **11 job roles** for balanced predictions
        
        **Model Architecture:** `RandomForestClassifier(n_estimators=200, max_depth=15, class_weight='balanced')`
        """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LEARNING RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
def page_recommendations():
    mods = get_imports()
    charts = mods["charts"]

    st.markdown("## 📚 Personalized Learning Recommendations")
    st.markdown("Curated courses, certifications, and a learning roadmap based on your skill gaps.")

    if not st.session_state.analysis_done:
        if not st.session_state.resume_text:
            st.warning("⚠️ Please upload your resume first!")
            return
        with st.spinner("Generating recommendations..."):
            _run_full_analysis(mods)

    missing_skills = st.session_state.gap_analysis.get("missing_skills", [])
    predicted_role = st.session_state.job_prediction.get("predicted_role", "Software Engineer") \
        if st.session_state.job_prediction else "Software Engineer"
    
    # Run recommendations if not cached
    if not st.session_state.recommendations:
        recommendations = mods["recommend_courses"](missing_skills)
        roadmap = mods["get_learning_roadmap"](predicted_role)
        st.session_state.recommendations = recommendations
        st.session_state.roadmap = roadmap

    recommendations = st.session_state.recommendations
    roadmap = st.session_state.roadmap

    tab1, tab2, tab3 = st.tabs(["🎓 Courses", "🗺️ Learning Roadmap", "⚡ Practice Platforms"])

    with tab1:
        st.markdown(f"### Recommended for your top missing skills: **{', '.join(missing_skills[:3])}...**")
        
        if not recommendations:
            st.info("Upload a job description to see targeted course recommendations!")
        else:
            # Filter controls
            platforms = list(set(r.get("platform", "") for r in recommendations))
            selected_platforms = st.multiselect("Filter by Platform", platforms, default=platforms)
            
            filtered = [r for r in recommendations if r.get("platform") in selected_platforms]
            
            cols = st.columns(2)
            for i, course in enumerate(filtered[:12]):
                with cols[i % 2]:
                    free_badge = '<span style="background:#00CC88;color:white;padding:2px 8px;border-radius:10px;font-size:0.7rem;font-weight:700;">FREE</span>' if course.get("free") else '<span style="background:#764BA2;color:white;padding:2px 8px;border-radius:10px;font-size:0.7rem;font-weight:700;">PAID</span>'
                    rating = course.get("rating", 0)
                    stars = "⭐" * int(rating) + f" ({rating})"
                    
                    st.markdown(f"""
                    <div class="course-card">
                        <div style="display:flex; justify-content:space-between; align-items:start;">
                            <div style="font-size:1.5rem;">{course.get('icon','📚')}</div>
                            {free_badge}
                        </div>
                        <div style="font-weight:700; color:#E2E8F0; margin:0.5rem 0; font-size:0.95rem;">
                            {course.get('title','')[:50]}
                        </div>
                        <div style="color:#94A3B8; font-size:0.8rem; margin-bottom:0.5rem;">
                            🏛️ {course.get('platform','')} · ⏱️ {course.get('duration','')} · {stars}
                        </div>
                        <div style="font-size:0.75rem; color:#667EEA;">
                            Skill: {course.get('skill','').title()} · Level: {course.get('level','')}
                        </div>
                        <a href="{course.get('url','#')}" target="_blank"
                           style="display:inline-block; margin-top:0.6rem; padding:0.3rem 0.8rem;
                           background:rgba(102,126,234,0.2); border:1px solid #667EEA;
                           color:#667EEA; border-radius:6px; text-decoration:none; font-size:0.8rem;
                           font-weight:600;">
                           View Course →
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"### 🗺️ Learning Roadmap for **{predicted_role}**")
        
        if roadmap:
            for i, step in enumerate(roadmap):
                progress_pct = (i / len(roadmap)) * 100
                st.markdown(f"""
                <div style="display:flex; align-items:center; margin-bottom:1rem;
                    background:rgba(42,42,62,0.8); border:1px solid rgba(102,126,234,0.2);
                    border-radius:12px; padding:1rem; transition:all 0.3s;">
                    <div style="width:36px; height:36px; border-radius:50%;
                        background:linear-gradient(135deg,#667EEA,#764BA2);
                        display:flex; align-items:center; justify-content:center;
                        font-weight:800; color:white; font-size:0.85rem; margin-right:1rem; flex-shrink:0;">
                        {i+1}
                    </div>
                    <div style="flex:1;">
                        <div style="color:#E2E8F0; font-weight:500; font-size:0.92rem;">{step}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Run the analysis to get a personalized learning roadmap!")

    with tab3:
        st.markdown("### ⚡ Practice Platforms")
        platforms_data = mods["get_practice_platforms"]()
        
        pl_cols = st.columns(2)
        for i, platform in enumerate(platforms_data):
            with pl_cols[i % 2]:
                st.markdown(f"""
                <div class="course-card">
                    <div style="display:flex; align-items:center; gap:0.8rem;">
                        <div style="font-size:2rem;">{platform['icon']}</div>
                        <div>
                            <div style="font-weight:700; color:#E2E8F0;">{platform['name']}</div>
                            <div style="color:#94A3B8; font-size:0.82rem;">{platform['desc']}</div>
                        </div>
                    </div>
                    <a href="{platform['url']}" target="_blank"
                       style="display:inline-block; margin-top:0.6rem; padding:0.3rem 0.8rem;
                       background:rgba(102,126,234,0.2); border:1px solid #667EEA;
                       color:#667EEA; border-radius:6px; text-decoration:none; font-size:0.8rem;
                       font-weight:600;">
                       Visit Platform →
                    </a>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    mods = get_imports()
    charts = mods["charts"]

    st.markdown("## 📊 Analytics Dashboard")

    if not st.session_state.analysis_done:
        if not st.session_state.resume_text:
            st.warning("⚠️ Please upload your resume first to see the dashboard!")
            return
        with st.spinner("Loading dashboard..."):
            _run_full_analysis(mods)

    gap = st.session_state.gap_analysis
    ats = st.session_state.ats_result
    pred = st.session_state.job_prediction
    
    candidate = st.session_state.candidate_name or "Your Profile"
    
    # Header
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(102,126,234,0.15),rgba(118,75,162,0.15));
        border:1px solid rgba(102,126,234,0.25); border-radius:16px; padding:1.5rem; margin-bottom:1.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:0.85rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.08em;">
                    Career Analysis Report
                </div>
                <div style="font-size:1.8rem; font-weight:800; color:#E2E8F0; margin-top:0.2rem;">
                    👤 {candidate}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.8rem; color:#94A3B8;">Predicted Role</div>
                <div style="font-size:1.2rem; font-weight:700; color:#667EEA;">
                    {pred.get('predicted_role', 'N/A')}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpis = [
        (f"{ats.get('total_score', 0)}", "ATS Score", "/100", "🎯"),
        (f"{gap.get('match_percentage', 0):.0f}%", "Skill Match", "", "🔍"),
        (str(gap.get("matching_count", 0)), "Matched Skills", "", "✅"),
        (str(gap.get("missing_count", 0)), "Missing Skills", "", "❌"),
        (f"{pred.get('confidence', 0):.0f}%", "ML Confidence", "", "🤖"),
    ]
    for col, (val, label, suffix, icon) in zip([kpi1, kpi2, kpi3, kpi4, kpi5], kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.5rem;">{icon}</div>
                <div class="metric-value" style="font-size:1.8rem;">{val}{suffix}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row 1
    c1, c2 = st.columns(2)
    
    with c1:
        fig_ats_gauge = charts.gauge_chart(ats.get("total_score", 0), "ATS Score", suffix="/100")
        st.plotly_chart(fig_ats_gauge, use_container_width=True)
    
    with c2:
        fig_match_gauge = charts.gauge_chart(gap.get("match_percentage", 0), "Skill Match %", suffix="%")
        st.plotly_chart(fig_match_gauge, use_container_width=True)

    # Charts row 2
    c3, c4 = st.columns(2)
    
    with c3:
        matching = gap.get("matching_skills", [])
        missing = gap.get("missing_skills", [])
        if matching or missing:
            fig_skills_pie = charts.skills_comparison_chart(matching, missing)
            st.plotly_chart(fig_skills_pie, use_container_width=True)
    
    with c4:
        all_preds = pred.get("top_predictions", [])
        if all_preds:
            fig_roles = charts.job_role_bar_chart(all_preds)
            st.plotly_chart(fig_roles, use_container_width=True)

    # Radar chart
    from skills.skill_database import get_all_job_roles, get_skills_for_role
    resume_set = set(st.session_state.resume_skills)
    categories = []
    coverages = []
    for role in get_all_job_roles():
        role_data = get_skills_for_role(role)
        role_skills = set(role_data.get("technical", []) + role_data.get("soft", []))
        if role_skills:
            cov = len(resume_set & role_skills) / len(role_skills) * 100
            categories.append(role.replace(" Engineer", " Eng.").replace(" Developer", " Dev."))
            coverages.append(round(cov, 1))
    
    if categories:
        fig_radar = charts.radar_chart(categories, coverages, "Skill Coverage Across All Roles")
        st.plotly_chart(fig_radar, use_container_width=True)

    # ATS breakdown
    cat_scores = ats.get("category_scores", {})
    weights = ats.get("weights", {})
    if cat_scores:
        fig_breakdown = charts.ats_breakdown_chart(cat_scores, weights)
        st.plotly_chart(fig_breakdown, use_container_width=True)

    # Download report
    st.markdown("---")
    st.markdown("### 📥 Download Report")
    
    col_dl, col_info = st.columns([1, 2])
    with col_dl:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            with st.spinner("Generating PDF report..."):
                analysis_data = {
                    "ats_score": ats.get("total_score", 0),
                    "match_percentage": gap.get("match_percentage", 0),
                    "predicted_role": pred.get("predicted_role", "N/A"),
                    "confidence": pred.get("confidence", 0),
                    "extracted_info": {
                        "Email": st.session_state.extracted_info.get("email", "N/A"),
                        "Phone": st.session_state.extracted_info.get("phone", "N/A"),
                        "Education": st.session_state.extracted_info.get("education", []),
                        "Skills": st.session_state.resume_skills[:15],
                    },
                    "matching_skills": gap.get("matching_skills", []),
                    "missing_skills": gap.get("missing_skills", []),
                    "ats_suggestions": ats.get("suggestions", []),
                    "recommendations": st.session_state.recommendations[:8],
                }
                pdf_bytes = mods["generate_pdf_report"](
                    st.session_state.candidate_name or "Candidate",
                    analysis_data
                )
                
                if pdf_bytes:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_bytes,
                        file_name=f"SkillGapAI_Report_{st.session_state.candidate_name.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.error("PDF generation failed. Please install: pip install reportlab")
    
    with col_info:
        st.markdown("""
        <div style="background:rgba(102,126,234,0.08); border-left:3px solid #667EEA;
            border-radius:0 10px 10px 0; padding:1rem; color:#94A3B8; font-size:0.85rem;">
            📄 The PDF report includes your ATS score, skill analysis, job prediction,
            improvement suggestions, and top course recommendations. 
            Perfect for tracking your career progress!
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: Run Full Analysis Pipeline
# ══════════════════════════════════════════════════════════════════════════════
def _run_full_analysis(mods):
    """Run the complete analysis pipeline and store results in session state."""
    if not st.session_state.resume_text:
        return
    
    # 1. Skill gap analysis (requires JD)
    if st.session_state.jd_text:
        gap_analysis = mods["analyze_skill_gap"](
            st.session_state.resume_text,
            st.session_state.jd_text,
            st.session_state.extracted_info
        )
        st.session_state.gap_analysis = gap_analysis
        st.session_state.jd_skills = gap_analysis.get("jd_all_skills", [])
        st.session_state.resume_skills = gap_analysis.get("resume_all_skills", st.session_state.resume_skills)
    else:
        # Even without JD, extract skills from resume
        skill_data = mods["extract_skills_from_text"](st.session_state.resume_text)
        st.session_state.resume_skills = skill_data["all"]
        st.session_state.gap_analysis = {
            "resume_technical_skills": skill_data["technical"],
            "resume_soft_skills": skill_data["soft"],
            "resume_all_skills": skill_data["all"],
            "matching_skills": [],
            "missing_skills": [],
            "match_percentage": 0.0,
            "tfidf_similarity": 0.0,
            "overall_match": 0.0,
            "matching_count": 0,
            "missing_count": 0,
            "jd_all_skills": [],
        }
    
    # 2. ATS Score
    ats_result = mods["calculate_ats_score"](
        st.session_state.resume_text,
        st.session_state.extracted_info,
        st.session_state.jd_text,
        st.session_state.resume_skills,
        st.session_state.jd_skills,
        st.session_state.gap_analysis.get("match_percentage", 0.0)
    )
    st.session_state.ats_result = ats_result
    
    # 3. Job role prediction
    if st.session_state.resume_skills:
        prediction = mods["predict_job_roles"](st.session_state.resume_skills)
        st.session_state.job_prediction = prediction
    
    # 4. Learning recommendations
    missing = st.session_state.gap_analysis.get("missing_skills", [])
    predicted_role = st.session_state.job_prediction.get("predicted_role", "Software Engineer") \
        if st.session_state.job_prediction else "Software Engineer"
    
    st.session_state.recommendations = mods["recommend_courses"](missing)
    st.session_state.roadmap = mods["get_learning_roadmap"](predicted_role)
    
    # 5. Update history
    import datetime
    st.session_state.analysis_history.append({
        "timestamp": datetime.datetime.now().strftime("%H:%M"),
        "match_pct": st.session_state.gap_analysis.get("match_percentage", 0),
        "ats_score": ats_result.get("total_score", 0),
    })
    
    st.session_state.analysis_done = True


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main():
    page = render_sidebar()
    
    page_map = {
        "Home": page_home,
        "Resume Upload": page_resume_upload,
        "Job Description": page_job_description,
        "Skill Analysis": page_skill_analysis,
        "ATS Score": page_ats_score,
        "Job Prediction": page_job_prediction,
        "Learning Recommendations": page_recommendations,
        "Dashboard": page_dashboard,
    }
    
    page_fn = page_map.get(page, page_home)
    page_fn()


if __name__ == "__main__":
    main()
