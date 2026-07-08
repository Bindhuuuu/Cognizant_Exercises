"""
SkillGap AI - Resume Information Extractor
Extracts structured information (name, email, phone, skills, education, experience)
from raw resume text using regex and spaCy NLP.
"""

import re
from typing import Dict, List, Any, Optional
from utils.logger import setup_logger

logger = setup_logger("extractor")

# ──────────────────────────────────────────────────────────────────────────────
# Regex Patterns
# ──────────────────────────────────────────────────────────────────────────────
EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)
PHONE_PATTERN = re.compile(
    r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]"
)
LINKEDIN_PATTERN = re.compile(
    r"linkedin\.com/in/[\w\-]+"
)
GITHUB_PATTERN = re.compile(
    r"github\.com/[\w\-]+"
)

# Section headers used to segment resume
SECTION_KEYWORDS = {
    "education": ["education", "academic", "qualification", "university", "college", "degree"],
    "experience": ["experience", "work history", "employment", "career", "internship", "job"],
    "skills": ["skills", "technical skills", "core competencies", "technologies", "proficiency"],
    "projects": ["projects", "project work", "personal projects", "academic projects"],
    "certifications": ["certifications", "certificates", "credentials", "courses completed"],
    "achievements": ["achievements", "awards", "honors", "accomplishments"],
}

# Degree keywords
DEGREE_PATTERNS = [
    "b.tech", "b.e.", "b.sc", "b.com", "bca", "bba", "m.tech", "m.sc", "mba",
    "m.e.", "mca", "phd", "ph.d", "bachelor", "master", "doctorate",
    "b.s.", "m.s.", "b.a.", "m.a.", "b.eng", "m.eng"
]


def extract_resume_info(text: str) -> Dict[str, Any]:
    """
    Extract all structured information from resume text.
    
    Args:
        text: Raw resume text
    
    Returns:
        Dictionary containing extracted fields
    """
    if not text:
        logger.warning("Empty text provided to extractor")
        return {}
    
    logger.info("Starting resume information extraction")
    
    result = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "skills": extract_skills_section(text),
        "projects": extract_projects(text),
        "certifications": extract_certifications(text),
        "summary": extract_summary(text),
        "raw_text": text
    }
    
    logger.info(f"Extraction complete. Name: {result['name']}, Email: {result['email']}")
    return result


def extract_name(text: str) -> str:
    """
    Extract candidate name from the top portion of the resume.
    Uses spaCy NER if available, falls back to heuristic.
    """
    # Try spaCy NER first
    try:
        import spacy
        nlp = _get_spacy_model()
        if nlp:
            # Only look at first 500 chars (name is usually at top)
            doc = nlp(text[:500])
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    name = ent.text.strip()
                    if 2 <= len(name.split()) <= 4:  # Reasonable name length
                        logger.debug(f"spaCy extracted name: {name}")
                        return name
    except Exception as e:
        logger.debug(f"spaCy name extraction failed: {e}")
    
    # Heuristic fallback: first non-empty line that looks like a name
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines[:5]:
        # A name is typically 2-4 words, all letters
        words = line.split()
        if 2 <= len(words) <= 4 and all(w.replace(".", "").isalpha() for w in words):
            # Skip if it looks like a section header
            if not any(kw in line.lower() for kw_list in SECTION_KEYWORDS.values() for kw in kw_list):
                logger.debug(f"Heuristic extracted name: {line}")
                return line
    
    return "Not found"


def extract_email(text: str) -> str:
    """Extract email address from text."""
    match = EMAIL_PATTERN.search(text)
    return match.group(0) if match else "Not found"


def extract_phone(text: str) -> str:
    """Extract phone number from text."""
    match = PHONE_PATTERN.search(text)
    return match.group(0).strip() if match else "Not found"


def extract_linkedin(text: str) -> str:
    """Extract LinkedIn profile URL."""
    match = LINKEDIN_PATTERN.search(text)
    return f"https://www.{match.group(0)}" if match else "Not found"


def extract_github(text: str) -> str:
    """Extract GitHub profile URL."""
    match = GITHUB_PATTERN.search(text)
    return f"https://www.{match.group(0)}" if match else "Not found"


def extract_education(text: str) -> List[str]:
    """Extract education details from resume text."""
    education = []
    lines = text.split("\n")
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Detect section start
        if any(kw in line_lower for kw in SECTION_KEYWORDS["education"]):
            in_section = True
            continue
        
        # Detect section end (next major section)
        if in_section and any(
            kw in line_lower for kw in 
            SECTION_KEYWORDS["experience"] + SECTION_KEYWORDS["skills"] + SECTION_KEYWORDS["projects"]
        ):
            break
        
        if in_section and line.strip():
            education.append(line.strip())
    
    # Fallback: detect degree keywords anywhere
    if not education:
        for line in lines:
            if any(deg in line.lower() for deg in DEGREE_PATTERNS):
                education.append(line.strip())
    
    return education[:8] if education else ["Not found"]


def extract_experience(text: str) -> List[str]:
    """Extract work experience entries from resume text."""
    experience = []
    lines = text.split("\n")
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        if any(kw in line_lower for kw in SECTION_KEYWORDS["experience"]):
            in_section = True
            continue
        
        if in_section and any(
            kw in line_lower for kw in 
            SECTION_KEYWORDS["education"] + SECTION_KEYWORDS["skills"] + SECTION_KEYWORDS["projects"]
        ):
            break
        
        if in_section and line.strip():
            experience.append(line.strip())
    
    return experience[:12] if experience else ["Not found"]


def extract_skills_section(text: str) -> List[str]:
    """Extract skills listed in the skills section of the resume."""
    skills = []
    lines = text.split("\n")
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        if any(kw in line_lower for kw in SECTION_KEYWORDS["skills"]):
            in_section = True
            continue
        
        if in_section and any(
            kw in line_lower for kw in 
            SECTION_KEYWORDS["experience"] + SECTION_KEYWORDS["education"] + SECTION_KEYWORDS["projects"]
        ):
            break
        
        if in_section and line.strip():
            # Split by common delimiters
            parts = re.split(r"[,|•·\|/]", line)
            for part in parts:
                part = part.strip()
                if part and 2 < len(part) < 40:
                    skills.append(part)
    
    return skills if skills else []


def extract_projects(text: str) -> List[str]:
    """Extract project descriptions from resume text."""
    projects = []
    lines = text.split("\n")
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        if any(kw in line_lower for kw in SECTION_KEYWORDS["projects"]):
            in_section = True
            continue
        
        if in_section and any(
            kw in line_lower for kw in 
            SECTION_KEYWORDS["certifications"] + SECTION_KEYWORDS["achievements"]
        ):
            break
        
        if in_section and line.strip():
            projects.append(line.strip())
    
    return projects[:10] if projects else ["Not found"]


def extract_certifications(text: str) -> List[str]:
    """Extract certifications from resume text."""
    certs = []
    lines = text.split("\n")
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        if any(kw in line_lower for kw in SECTION_KEYWORDS["certifications"]):
            in_section = True
            continue
        
        if in_section and any(
            kw in line_lower for kw in SECTION_KEYWORDS["achievements"]
        ):
            break
        
        if in_section and line.strip():
            certs.append(line.strip())
    
    # Fallback: look for cert keywords
    if not certs:
        cert_keywords = ["certified", "certification", "certificate", "aws", "azure", "google", "coursera", "udemy"]
        for line in lines:
            if any(kw in line.lower() for kw in cert_keywords) and len(line.strip()) > 5:
                certs.append(line.strip())
    
    return certs[:8] if certs else ["Not found"]


def extract_summary(text: str) -> str:
    """Extract the professional summary/objective from resume text."""
    lines = text.split("\n")
    summary_keywords = ["summary", "objective", "profile", "about", "overview", "career objective"]
    in_section = False
    summary_lines = []
    
    for line in lines:
        line_lower = line.lower().strip()
        
        if any(kw in line_lower for kw in summary_keywords):
            in_section = True
            continue
        
        if in_section and any(
            kw in line_lower for kw in 
            SECTION_KEYWORDS["experience"] + SECTION_KEYWORDS["education"] + SECTION_KEYWORDS["skills"]
        ):
            break
        
        if in_section and line.strip():
            summary_lines.append(line.strip())
            if len(summary_lines) >= 5:
                break
    
    return " ".join(summary_lines) if summary_lines else "Not found"


def _get_spacy_model():
    """Load spaCy English model, downloading if necessary."""
    try:
        import spacy
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            logger.info("Downloading spaCy en_core_web_sm model...")
            import subprocess
            import sys
            subprocess.run(
                [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
                capture_output=True
            )
            return spacy.load("en_core_web_sm")
    except Exception as e:
        logger.warning(f"spaCy not available: {e}")
        return None
