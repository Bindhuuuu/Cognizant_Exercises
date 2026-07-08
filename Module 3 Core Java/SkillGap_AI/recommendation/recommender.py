"""
SkillGap AI - Learning Recommendation System
Recommends personalized courses, certifications, and learning resources
based on identified skill gaps.
"""

import json
import os
from typing import List, Dict, Any
from utils.logger import setup_logger

logger = setup_logger("recommender")

# Path to courses database
_COURSES_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "courses_db.json"
)

# Cache
_courses_cache = {}

# Skill aliases for flexible matching
SKILL_ALIASES = {
    "ml": "machine learning",
    "ai": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "js": "javascript",
    "ts": "javascript",
    "typescript": "javascript",
    "node": "javascript",
    "nodejs": "javascript",
    "py": "python",
    "tf": "tensorflow",
    "ds": "data structures",
    "algo": "data structures",
    "algorithms": "data structures",
    "k8s": "kubernetes",
    "db": "sql",
    "database": "sql",
    "nosql": "sql",
    "infosec": "network security",
    "cyber": "network security",
    "cybersecurity": "network security",
    "devops": "docker",
    "cloud": "aws",
    "data viz": "data visualization",
    "dataviz": "data visualization",
    "visualization": "data visualization",
}

# Platform icons
PLATFORM_ICONS = {
    "Coursera": "🎓",
    "Udemy": "🎯",
    "edX": "🏛️",
    "Kaggle": "🏆",
    "freeCodeCamp": "💻",
    "GeeksforGeeks": "🟢",
    "LeetCode": "⚡",
    "fast.ai": "🚀",
    "AWS Training": "☁️",
    "Linux Foundation": "🐧",
    "PyTorch Official": "🔥",
    "default": "📚"
}

# Role-specific roadmaps
LEARNING_ROADMAPS = {
    "Data Scientist": [
        "📊 Learn Python basics and data manipulation (pandas, numpy)",
        "📈 Master data visualization (matplotlib, seaborn, plotly)",
        "🧮 Study statistics and probability",
        "🤖 Learn machine learning fundamentals (scikit-learn)",
        "🧠 Explore deep learning (TensorFlow/PyTorch)",
        "📝 Practice on Kaggle competitions",
        "🚀 Build end-to-end ML projects",
        "☁️ Learn MLOps and model deployment"
    ],
    "Data Analyst": [
        "📊 Master Excel and Google Sheets",
        "🗃️ Learn SQL thoroughly",
        "🐍 Learn Python with pandas",
        "📉 Practice data visualization (Tableau/Power BI)",
        "📐 Study statistics and A/B testing",
        "🔍 Work on data cleaning projects",
        "📋 Build dashboards and reports",
        "🚀 Portfolio: 3 real-world analysis projects"
    ],
    "Machine Learning Engineer": [
        "🐍 Master Python and software engineering",
        "🤖 Deep dive into ML algorithms",
        "⚡ Learn MLOps tools (MLflow, Kubeflow)",
        "🐳 Master Docker and Kubernetes",
        "☁️ Learn cloud platforms (AWS/GCP/Azure)",
        "🔧 Practice model optimization",
        "🚀 Build ML pipelines",
        "📡 Learn model serving (TensorFlow Serving, FastAPI)"
    ],
    "Software Engineer": [
        "💻 Master one programming language deeply",
        "🏗️ Learn data structures and algorithms",
        "🎨 Study design patterns and OOP",
        "🌐 Learn web frameworks",
        "🗃️ Master databases (SQL + NoSQL)",
        "🐳 Learn Docker and basic DevOps",
        "⚙️ Practice system design",
        "🚀 Build and deploy 3 full projects"
    ],
    "Full Stack Developer": [
        "🌐 Master HTML, CSS, JavaScript",
        "⚛️ Learn a frontend framework (React/Vue)",
        "⚙️ Learn backend (Node.js/Python/Java)",
        "🗃️ Master SQL and NoSQL databases",
        "🔗 Practice REST API design",
        "🐳 Learn Docker basics",
        "☁️ Deploy on cloud (AWS/Heroku/Vercel)",
        "🚀 Build 2 complete full-stack projects"
    ],
    "DevOps Engineer": [
        "🐧 Master Linux fundamentals",
        "🐳 Learn Docker deeply",
        "☸️ Learn Kubernetes",
        "🔄 Master CI/CD (Jenkins/GitHub Actions)",
        "⚙️ Learn Infrastructure as Code (Terraform)",
        "📡 Study monitoring (Grafana/Prometheus)",
        "☁️ Get AWS/Azure certification",
        "🚀 Automate a complete deployment pipeline"
    ],
    "AI Engineer": [
        "🐍 Master Python for AI",
        "🤖 Deep learning with PyTorch/TensorFlow",
        "🗣️ NLP and LLM fundamentals",
        "🔧 Learn HuggingFace Transformers",
        "🚀 Prompt engineering and RAG",
        "☁️ Deploy AI models on cloud",
        "📡 Build LLM-powered applications",
        "🎯 Fine-tuning and model optimization"
    ],
    "Frontend Developer": [
        "🌐 Master HTML5 and CSS3",
        "⚡ Deep dive into JavaScript (ES6+)",
        "⚛️ Learn React.js",
        "🎨 Study UI/UX principles",
        "📱 Master responsive design",
        "🔧 Learn build tools (Webpack/Vite)",
        "♿ Practice web accessibility",
        "🚀 Build a professional portfolio"
    ],
    "Backend Developer": [
        "🐍 Master Python or Java/Node.js",
        "🗃️ Deep dive into SQL databases",
        "🔗 Master REST API design",
        "⚡ Learn NoSQL (MongoDB/Redis)",
        "🔐 Study authentication and security",
        "🐳 Learn Docker",
        "🏗️ Practice system design",
        "🚀 Build a scalable backend project"
    ],
    "Cloud Engineer": [
        "☁️ Start with AWS/Azure fundamentals",
        "🌐 Study networking basics",
        "🔒 Learn cloud security",
        "⚙️ Master Infrastructure as Code (Terraform)",
        "🐳 Learn containers (Docker/K8s)",
        "📡 Study cloud monitoring",
        "✅ Get a cloud certification (AWS SAA/Azure 900)",
        "🚀 Architect a multi-tier cloud project"
    ],
    "Cybersecurity Analyst": [
        "🌐 Study networking fundamentals",
        "🔐 Learn cryptography basics",
        "🐧 Master Linux",
        "🔍 Practice penetration testing (TryHackMe/HackTheBox)",
        "🛡️ Study SIEM tools (Splunk)",
        "⚠️ Learn vulnerability assessment",
        "✅ Get CompTIA Security+ certification",
        "🚀 Complete a CTF challenge"
    ]
}


def load_courses_db() -> Dict:
    """Load the courses database."""
    global _courses_cache
    if _courses_cache:
        return _courses_cache
    
    try:
        with open(_COURSES_DB_PATH, "r", encoding="utf-8") as f:
            _courses_cache = json.load(f)
        logger.info(f"Courses DB loaded: {len(_courses_cache)} skill categories")
        return _courses_cache
    except Exception as e:
        logger.error(f"Failed to load courses DB: {e}")
        return {}


def recommend_courses(
    missing_skills: List[str],
    max_per_skill: int = 2
) -> List[Dict[str, Any]]:
    """
    Recommend learning courses for a list of missing skills.
    
    Args:
        missing_skills: Skills the candidate is missing
        max_per_skill: Maximum courses to recommend per skill
    
    Returns:
        List of course recommendation dictionaries
    """
    db = load_courses_db()
    recommendations = []
    seen_titles = set()
    
    for skill in missing_skills[:12]:  # Limit to top 12 missing skills
        skill_lower = skill.lower().strip()
        
        # Check for alias
        lookup_key = SKILL_ALIASES.get(skill_lower, skill_lower)
        
        # Find courses for this skill
        courses = db.get(lookup_key, db.get("default", []))
        
        for course in courses[:max_per_skill]:
            title = course.get("title", "")
            if title not in seen_titles:
                seen_titles.add(title)
                recommendations.append({
                    **course,
                    "skill": skill,
                    "icon": PLATFORM_ICONS.get(course.get("platform", ""), "📚")
                })
    
    logger.info(f"Recommended {len(recommendations)} courses for {len(missing_skills)} missing skills")
    return recommendations


def get_learning_roadmap(predicted_role: str) -> List[str]:
    """
    Get the learning roadmap for a predicted job role.
    
    Args:
        predicted_role: The ML-predicted job role
    
    Returns:
        List of ordered learning steps
    """
    roadmap = LEARNING_ROADMAPS.get(
        predicted_role,
        LEARNING_ROADMAPS.get("Software Engineer")  # Default roadmap
    )
    logger.info(f"Roadmap for {predicted_role}: {len(roadmap)} steps")
    return roadmap


def get_practice_platforms() -> List[Dict[str, str]]:
    """Return curated list of practice platforms."""
    return [
        {"name": "LeetCode", "url": "https://leetcode.com", "desc": "Coding interview prep & DSA", "icon": "⚡"},
        {"name": "Kaggle", "url": "https://kaggle.com", "desc": "ML competitions & datasets", "icon": "🏆"},
        {"name": "HackerRank", "url": "https://hackerrank.com", "desc": "Programming challenges", "icon": "🟢"},
        {"name": "GitHub", "url": "https://github.com", "desc": "Portfolio & open source", "icon": "🐙"},
        {"name": "TryHackMe", "url": "https://tryhackme.com", "desc": "Cybersecurity practice", "icon": "🔐"},
        {"name": "HackTheBox", "url": "https://hackthebox.com", "desc": "Advanced security challenges", "icon": "🎯"},
        {"name": "GeeksforGeeks", "url": "https://geeksforgeeks.org", "desc": "CS fundamentals & interview prep", "icon": "📗"},
        {"name": "freeCodeCamp", "url": "https://freecodecamp.org", "desc": "Free full-stack curriculum", "icon": "🔥"},
    ]
