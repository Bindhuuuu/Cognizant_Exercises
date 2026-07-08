"""
SkillGap AI - Skill Database
Contains curated skill lists for all supported job roles.
Loads from data/skills_db.json and provides lookup utilities.
"""

import json
import os
from typing import Dict, List, Set
from utils.logger import setup_logger

logger = setup_logger("skill_database")

# Path to the skills JSON database
_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "skills_db.json")

# Cache for loaded data
_skills_cache: Dict = {}


def load_skills_db() -> Dict:
    """
    Load the skills database from JSON file.
    
    Returns:
        Dictionary mapping job role → {technical: [...], soft: [...]}
    """
    global _skills_cache
    if _skills_cache:
        return _skills_cache
    
    try:
        with open(_DB_PATH, "r", encoding="utf-8") as f:
            _skills_cache = json.load(f)
        logger.info(f"Loaded skills for {len(_skills_cache)} job roles")
        return _skills_cache
    except FileNotFoundError:
        logger.error(f"Skills database not found at: {_DB_PATH}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in skills database: {e}")
        return {}


def get_all_job_roles() -> List[str]:
    """Return list of all supported job roles."""
    db = load_skills_db()
    return list(db.keys())


def get_skills_for_role(role: str) -> Dict[str, List[str]]:
    """
    Get technical and soft skills for a specific job role.
    
    Args:
        role: Job role name (must match keys in skills_db.json)
    
    Returns:
        Dictionary with 'technical' and 'soft' skill lists
    """
    db = load_skills_db()
    return db.get(role, {"technical": [], "soft": []})


def get_all_technical_skills() -> Set[str]:
    """Return a set of all technical skills across all roles."""
    db = load_skills_db()
    all_tech = set()
    for role_data in db.values():
        all_tech.update(role_data.get("technical", []))
    return all_tech


def get_all_soft_skills() -> Set[str]:
    """Return a set of all soft skills across all roles."""
    db = load_skills_db()
    all_soft = set()
    for role_data in db.values():
        all_soft.update(role_data.get("soft", []))
    return all_soft


def get_role_skill_vector(role: str, all_skills: List[str]) -> List[int]:
    """
    Create a binary skill presence vector for a given role.
    Used for ML model training.
    
    Args:
        role: Job role name
        all_skills: Master list of all skills (defines vector dimensions)
    
    Returns:
        Binary list (1 if skill required for role, 0 otherwise)
    """
    role_data = get_skills_for_role(role)
    role_skills = set(role_data.get("technical", []) + role_data.get("soft", []))
    return [1 if skill in role_skills else 0 for skill in all_skills]
