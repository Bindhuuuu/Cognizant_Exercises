"""
SkillGap AI - Skill Gap Analyzer
Performs comprehensive skill gap analysis between resume and job description.
"""

from typing import Dict, List, Any, Tuple
from skills.skill_extractor import extract_skills_from_text, compare_skills
from analysis.tfidf_analyzer import compute_similarity, keyword_match_analysis
from utils.logger import setup_logger

logger = setup_logger("gap_analyzer")


def analyze_skill_gap(
    resume_text: str,
    jd_text: str,
    extracted_resume_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Perform full skill gap analysis comparing resume to job description.
    
    Args:
        resume_text: Full resume text
        jd_text: Job description text
        extracted_resume_info: Pre-extracted resume information
    
    Returns:
        Comprehensive gap analysis dictionary
    """
    logger.info("Starting skill gap analysis")
    
    # Extract skills from both texts
    resume_skill_data = extract_skills_from_text(resume_text)
    jd_skill_data = extract_skills_from_text(jd_text)
    
    # Include explicitly listed skills from parsed resume
    listed_skills = extracted_resume_info.get("skills", [])
    if listed_skills:
        all_resume_skills = list(set(
            resume_skill_data["all"] + [s.lower() for s in listed_skills]
        ))
    else:
        all_resume_skills = resume_skill_data["all"]
    
    # Get JD skills
    all_jd_skills = jd_skill_data["all"]
    
    # Compute matching and missing skills
    matching_skills, missing_skills, match_pct = compare_skills(all_resume_skills, all_jd_skills)
    
    # TF-IDF similarity
    tfidf_similarity = compute_similarity(resume_text, jd_text)
    
    # Keyword analysis
    keyword_data = keyword_match_analysis(resume_text, jd_text)
    
    # Overall score (weighted average)
    overall_match = (match_pct * 0.6 + tfidf_similarity * 0.4)
    
    logger.info(f"Gap analysis complete. Match: {match_pct:.1f}%, TF-IDF: {tfidf_similarity:.1f}%")
    
    return {
        # Skills
        "resume_technical_skills": resume_skill_data["technical"],
        "resume_soft_skills": resume_skill_data["soft"],
        "resume_all_skills": all_resume_skills,
        "jd_technical_skills": jd_skill_data["technical"],
        "jd_soft_skills": jd_skill_data["soft"],
        "jd_all_skills": all_jd_skills,
        # Gap analysis
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(match_pct, 1),
        "tfidf_similarity": round(tfidf_similarity, 1),
        "overall_match": round(overall_match, 1),
        # Keywords
        "matched_keywords": keyword_data["matched_keywords"],
        "missing_keywords": keyword_data["missing_keywords"],
        "keyword_match_pct": keyword_data["keyword_match_pct"],
        # Counts
        "resume_skill_count": len(all_resume_skills),
        "jd_skill_count": len(all_jd_skills),
        "matching_count": len(matching_skills),
        "missing_count": len(missing_skills),
    }


def get_readiness_score(
    match_percentage: float,
    ats_score: int,
    experience_years: int = 0
) -> Dict[str, Any]:
    """
    Calculate a career readiness score based on multiple factors.
    
    Args:
        match_percentage: Skill match percentage
        ats_score: ATS compatibility score
        experience_years: Years of experience (optional)
    
    Returns:
        Readiness score dictionary
    """
    # Weighted readiness score
    readiness = (match_percentage * 0.5 + ats_score * 0.4 + min(experience_years * 5, 10) * 0.1)
    readiness = round(min(readiness, 100), 1)
    
    if readiness >= 80:
        level = "Job Ready 🚀"
        color = "#00CC88"
        description = "Your profile is well-matched for this role!"
    elif readiness >= 60:
        level = "Nearly Ready 🎯"
        color = "#FFA500"
        description = "A few more skills and you're there!"
    elif readiness >= 40:
        level = "Developing 📈"
        color = "#FF6B6B"
        description = "Focus on bridging the key skill gaps."
    else:
        level = "Getting Started 🌱"
        color = "#9B59B6"
        description = "Build foundational skills with our recommendations."
    
    return {
        "score": readiness,
        "level": level,
        "color": color,
        "description": description
    }
