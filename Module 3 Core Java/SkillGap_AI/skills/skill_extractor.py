"""
SkillGap AI - Skill Extractor
Extracts technical and soft skills from resume text using keyword matching
and spaCy NLP. Compares against the curated skill database.
"""

import re
from typing import Dict, List, Set, Tuple
from skills.skill_database import get_all_technical_skills, get_all_soft_skills
from utils.logger import setup_logger

logger = setup_logger("skill_extractor")

# Additional common technical skills not in the DB (catch-all)
EXTRA_TECHNICAL_SKILLS = {
    "c", "c++", "c#", "java", "kotlin", "swift", "rust", "golang", "go",
    "scala", "perl", "ruby", "php", "matlab", "bash", "powershell",
    "mysql", "postgresql", "sqlite", "oracle", "cassandra", "dynamodb",
    "redis", "elasticsearch", "kafka", "rabbitmq", "celery",
    "flask", "django", "fastapi", "spring", "springboot", ".net",
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "selenium", "pytest", "junit", "mockito", "jest", "cypress",
    "opencv", "sklearn", "scipy", "statsmodels",
    "tableau", "power bi", "looker", "qlik",
    "excel", "word", "powerpoint", "google sheets",
    "html", "css", "sass", "less", "bootstrap",
    "tensorflow", "pytorch", "keras", "hugging face", "langchain",
    "linux", "ubuntu", "centos", "windows server",
    "rest api", "graphql", "soap", "grpc", "websockets",
    "oauth", "jwt", "ssl", "tls", "vpn",
    "terraform", "ansible", "chef", "puppet",
    "azure devops", "aws lambda", "s3", "ec2", "rds",
    "flutter", "react native", "ionic",
    "agile", "scrum", "kanban", "waterfall",
    "jira", "trello", "asana", "notion",
    "data mining", "etl", "data warehouse", "spark", "hadoop", "hive",
    "tableau", "d3.js", "bokeh", "altair", "streamlit",
    "time series", "forecasting", "clustering", "classification",
    "neural network", "cnn", "rnn", "lstm", "gan", "transformer",
    "bert", "gpt", "llm", "rag", "vector database", "pinecone",
    "penetration testing", "ethical hacking", "nmap", "metasploit",
    "splunk", "wireshark", "kali linux", "owasp"
}


def extract_skills_from_text(text: str) -> Dict[str, List[str]]:
    """
    Extract technical and soft skills from resume text.
    
    Args:
        text: Raw or preprocessed resume text
    
    Returns:
        Dictionary with 'technical' and 'soft' skill lists
    """
    text_lower = text.lower()
    
    # Get all skills from DB + extras
    tech_skills_db = get_all_technical_skills()
    soft_skills_db = get_all_soft_skills()
    all_tech = tech_skills_db | EXTRA_TECHNICAL_SKILLS
    
    found_tech = _find_skills_in_text(text_lower, all_tech)
    found_soft = _find_skills_in_text(text_lower, soft_skills_db)
    
    logger.info(f"Extracted {len(found_tech)} technical skills, {len(found_soft)} soft skills")
    
    return {
        "technical": sorted(list(found_tech)),
        "soft": sorted(list(found_soft)),
        "all": sorted(list(found_tech | found_soft))
    }


def _find_skills_in_text(text: str, skill_set: Set[str]) -> Set[str]:
    """
    Find which skills from a set appear in the given text.
    Uses word boundary matching for accuracy.
    
    Args:
        text: Lowercased text to search in
        skill_set: Set of skill keywords to look for
    
    Returns:
        Set of found skills
    """
    found = set()
    for skill in skill_set:
        # Escape special regex characters in skill names
        escaped = re.escape(skill.lower())
        # Use word boundary or punctuation boundary
        pattern = r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])"
        if re.search(pattern, text):
            found.add(skill)
    return found


def compare_skills(
    resume_skills: List[str],
    job_skills: List[str]
) -> Tuple[List[str], List[str], float]:
    """
    Compare resume skills against job description required skills.
    
    Args:
        resume_skills: Skills extracted from the resume
        job_skills: Skills extracted from the job description
    
    Returns:
        Tuple of (matching_skills, missing_skills, match_percentage)
    """
    resume_set = {s.lower().strip() for s in resume_skills}
    job_set = {s.lower().strip() for s in job_skills}
    
    matching = sorted(list(resume_set & job_set))
    missing = sorted(list(job_set - resume_set))
    
    match_pct = (len(matching) / len(job_set) * 100) if job_set else 0.0
    
    logger.info(f"Skill comparison: {len(matching)} matching, {len(missing)} missing, {match_pct:.1f}%")
    return matching, missing, match_pct


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """
    Categorize a list of skills into technical vs. soft.
    
    Args:
        skills: List of skill strings
    
    Returns:
        Dictionary with 'technical' and 'soft' lists
    """
    tech_db = get_all_technical_skills() | EXTRA_TECHNICAL_SKILLS
    soft_db = get_all_soft_skills()
    
    technical = []
    soft = []
    
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in tech_db:
            technical.append(skill)
        elif skill_lower in soft_db:
            soft.append(skill)
        else:
            technical.append(skill)  # Default to technical
    
    return {"technical": technical, "soft": soft}
