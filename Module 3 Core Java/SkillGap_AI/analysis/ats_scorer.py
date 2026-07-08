"""
SkillGap AI - ATS Score Calculator
Calculates an ATS (Applicant Tracking System) compatibility score for resumes.
Evaluates: skills, keywords, experience, education, formatting, projects, certifications.
"""

import re
from typing import Dict, List, Tuple, Any
from utils.logger import setup_logger

logger = setup_logger("ats_scorer")

# Weight of each ATS criterion (must sum to 100)
ATS_WEIGHTS = {
    "skills": 30,
    "keywords": 20,
    "experience": 20,
    "education": 15,
    "formatting": 5,
    "projects": 5,
    "certifications": 5,
}


def calculate_ats_score(
    resume_text: str,
    extracted_info: Dict[str, Any],
    jd_text: str = "",
    resume_skills: List[str] = None,
    jd_skills: List[str] = None,
    match_percentage: float = 0.0
) -> Dict[str, Any]:
    """
    Calculate comprehensive ATS score for a resume.
    
    Args:
        resume_text: Full resume text
        extracted_info: Extracted resume data dictionary
        jd_text: Optional job description text for keyword matching
        resume_skills: List of skills found in resume
        jd_skills: List of skills required in JD
        match_percentage: Pre-computed skill match percentage
    
    Returns:
        Dictionary with overall score, category scores, and suggestions
    """
    if resume_skills is None:
        resume_skills = []
    if jd_skills is None:
        jd_skills = []
    
    scores = {}
    suggestions = []
    
    # ── 1. Skills Score (30 pts) ───────────────────────────────────────────
    skill_score, skill_suggestions = _score_skills(resume_skills, jd_skills, match_percentage)
    scores["skills"] = skill_score
    suggestions.extend(skill_suggestions)
    
    # ── 2. Keyword Match Score (20 pts) ────────────────────────────────────
    keyword_score, kw_suggestions = _score_keywords(resume_text, jd_text)
    scores["keywords"] = keyword_score
    suggestions.extend(kw_suggestions)
    
    # ── 3. Experience Score (20 pts) ──────────────────────────────────────
    exp_score, exp_suggestions = _score_experience(extracted_info, resume_text)
    scores["experience"] = exp_score
    suggestions.extend(exp_suggestions)
    
    # ── 4. Education Score (15 pts) ────────────────────────────────────────
    edu_score, edu_suggestions = _score_education(extracted_info)
    scores["education"] = edu_score
    suggestions.extend(edu_suggestions)
    
    # ── 5. Formatting Score (5 pts) ────────────────────────────────────────
    fmt_score, fmt_suggestions = _score_formatting(extracted_info, resume_text)
    scores["formatting"] = fmt_score
    suggestions.extend(fmt_suggestions)
    
    # ── 6. Projects Score (5 pts) ──────────────────────────────────────────
    proj_score, proj_suggestions = _score_projects(extracted_info)
    scores["projects"] = proj_score
    suggestions.extend(proj_suggestions)
    
    # ── 7. Certifications Score (5 pts) ────────────────────────────────────
    cert_score, cert_suggestions = _score_certifications(extracted_info)
    scores["certifications"] = cert_score
    suggestions.extend(cert_suggestions)
    
    # Compute total weighted score
    total = sum(
        int(scores[k] * ATS_WEIGHTS[k] / 100)
        for k in ATS_WEIGHTS
    )
    # Cap at 100
    total = min(total, 100)
    
    logger.info(f"ATS Score: {total}/100 | Breakdown: {scores}")
    
    return {
        "total_score": total,
        "category_scores": scores,
        "weights": ATS_WEIGHTS,
        "suggestions": suggestions[:10],  # Top 10 suggestions
        "grade": _get_grade(total)
    }


def _score_skills(
    resume_skills: List[str],
    jd_skills: List[str],
    match_pct: float
) -> Tuple[int, List[str]]:
    """Score skills section out of 100."""
    suggestions = []
    
    if not resume_skills:
        suggestions.append("⚠️ Add a dedicated 'Skills' section with relevant technical skills")
        return 0, suggestions
    
    # Base score from skill count
    skill_count_score = min(len(resume_skills) / 20 * 50, 50)
    
    # Match score from JD alignment
    match_score = min(match_pct / 2, 50) if jd_skills else 50
    
    total = int(skill_count_score + match_score)
    
    if len(resume_skills) < 8:
        suggestions.append("📌 Add more skills (aim for 10-15 relevant skills)")
    if match_pct < 50 and jd_skills:
        missing_count = len(jd_skills) - int(match_pct / 100 * len(jd_skills))
        suggestions.append(f"🎯 Add {missing_count} more skills from the job description")
    
    return min(total, 100), suggestions


def _score_keywords(resume_text: str, jd_text: str) -> Tuple[int, List[str]]:
    """Score keyword density and JD alignment out of 100."""
    suggestions = []
    
    if not jd_text:
        # Generic keyword score based on resume content
        word_count = len(resume_text.split())
        score = min(word_count / 500 * 80, 80)
        if word_count < 300:
            suggestions.append("📝 Expand your resume content (aim for 400-600 words)")
        return int(score), suggestions
    
    # Check JD keyword presence in resume
    jd_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", jd_text.lower()))
    resume_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", resume_text.lower()))
    
    common = jd_words & resume_words
    match_ratio = len(common) / len(jd_words) if jd_words else 0
    score = int(match_ratio * 100)
    
    if match_ratio < 0.4:
        suggestions.append("🔑 Mirror more keywords from the job description naturally in your resume")
    if match_ratio < 0.6:
        suggestions.append("✏️ Tailor your resume to each specific job description")
    
    return min(score, 100), suggestions


def _score_experience(extracted_info: Dict, resume_text: str) -> Tuple[int, List[str]]:
    """Score experience section out of 100."""
    suggestions = []
    experience = extracted_info.get("experience", [])
    
    if experience == ["Not found"] or not experience:
        suggestions.append("💼 Add a detailed 'Work Experience' or 'Internship' section")
        return 20, suggestions  # Give some credit even without experience
    
    # Count experience entries
    num_entries = len([e for e in experience if len(e) > 20])
    
    # Check for quantified achievements (numbers/percentages)
    text_lower = resume_text.lower()
    has_metrics = bool(re.search(r"\d+[%+]|\d+x|\$\d+|increased|improved|reduced|achieved", text_lower))
    
    score = min(num_entries / 5 * 70, 70) + (30 if has_metrics else 10)
    
    if not has_metrics:
        suggestions.append("📊 Quantify achievements: use numbers, % improvements, and impact metrics")
    if num_entries < 2:
        suggestions.append("📋 Add more detail to your experience entries (job titles, responsibilities, impact)")
    
    return min(int(score), 100), suggestions


def _score_education(extracted_info: Dict) -> Tuple[int, List[str]]:
    """Score education section out of 100."""
    suggestions = []
    education = extracted_info.get("education", [])
    
    if education == ["Not found"] or not education:
        suggestions.append("🎓 Add an 'Education' section with your degree and institution")
        return 30, suggestions
    
    edu_text = " ".join(education).lower()
    
    # Check for degree keywords
    degree_keywords = ["b.tech", "b.e", "bachelor", "master", "m.tech", "mba", "phd", "b.sc", "m.sc", "bca", "mca"]
    has_degree = any(kw in edu_text for kw in degree_keywords)
    
    # Check for GPA/percentage
    has_gpa = bool(re.search(r"\d+\.?\d*\s*(gpa|cgpa|%|percent)", edu_text))
    
    score = 60 if has_degree else 30
    score += 20 if has_gpa else 0
    score += 20 if len(education) >= 2 else 10
    
    if not has_gpa:
        suggestions.append("🏆 Include your GPA/CGPA or percentage in the education section")
    if not has_degree:
        suggestions.append("🎓 Clearly state your degree name and specialization")
    
    return min(score, 100), suggestions


def _score_formatting(extracted_info: Dict, resume_text: str) -> Tuple[int, List[str]]:
    """Score resume formatting quality out of 100."""
    suggestions = []
    score = 60  # Base formatting score
    
    # Check for email
    if extracted_info.get("email", "Not found") != "Not found":
        score += 15
    else:
        suggestions.append("📧 Add your email address to the resume")
    
    # Check for phone
    if extracted_info.get("phone", "Not found") != "Not found":
        score += 15
    else:
        suggestions.append("📱 Include your phone number on the resume")
    
    # Check for LinkedIn
    if extracted_info.get("linkedin", "Not found") != "Not found":
        score += 10
    else:
        suggestions.append("🔗 Add your LinkedIn profile URL")
    
    return min(score, 100), suggestions


def _score_projects(extracted_info: Dict) -> Tuple[int, List[str]]:
    """Score projects section out of 100."""
    suggestions = []
    projects = extracted_info.get("projects", [])
    
    if projects == ["Not found"] or not projects:
        suggestions.append("🛠️ Add a 'Projects' section to showcase practical experience")
        return 20, suggestions
    
    num_projects = len([p for p in projects if len(p) > 20])
    score = min(num_projects / 3 * 100, 100)
    
    if num_projects < 2:
        suggestions.append("💡 Add 2-3 relevant projects with descriptions and tech stack used")
    
    return int(score), suggestions


def _score_certifications(extracted_info: Dict) -> Tuple[int, List[str]]:
    """Score certifications section out of 100."""
    suggestions = []
    certs = extracted_info.get("certifications", [])
    
    if certs == ["Not found"] or not certs:
        suggestions.append("🏅 Add relevant certifications (AWS, Google, Coursera, etc.) to boost your score")
        return 0, suggestions
    
    num_certs = len([c for c in certs if len(c) > 5])
    score = min(num_certs / 3 * 100, 100)
    
    return int(score), suggestions


def _get_grade(score: int) -> str:
    """Convert numeric score to letter grade."""
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B+"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C+"
    elif score >= 40:
        return "C"
    else:
        return "D"
