"""
SkillGap AI - Job Role Predictor
Predicts suitable job roles from extracted resume skills using the trained ML model.
"""

import numpy as np
from typing import List, Dict, Any, Optional
from ml.model_trainer import load_model, train_model
from utils.logger import setup_logger

logger = setup_logger("job_predictor")

# Module-level model cache (loaded once per session)
_model = None
_all_skills = None
_encoder = None


def _ensure_model_loaded():
    """Ensure the ML model is loaded, training if necessary."""
    global _model, _all_skills, _encoder
    if _model is None:
        logger.info("Loading ML model...")
        train_model()  # Train if not already trained
        _model, _all_skills, _encoder = load_model()


def predict_job_roles(
    resume_skills: List[str],
    top_n: int = 5
) -> Dict[str, Any]:
    """
    Predict the most suitable job roles for a candidate based on their skills.
    
    Args:
        resume_skills: List of skills extracted from resume
        top_n: Number of top roles to return (default: 5)
    
    Returns:
        Dictionary with predicted roles and confidence scores
    """
    _ensure_model_loaded()
    
    if _model is None or _all_skills is None or _encoder is None:
        logger.error("Model not available. Using fallback prediction.")
        return _fallback_prediction(resume_skills)
    
    # Build feature vector
    skill_set = {s.lower().strip() for s in resume_skills}
    feature_vector = [1 if skill in skill_set else 0 for skill in _all_skills]
    
    # Handle empty skill vector
    if sum(feature_vector) == 0:
        logger.warning("No skills matched the model feature space. Using fallback.")
        return _fallback_prediction(resume_skills)
    
    X = np.array(feature_vector).reshape(1, -1)
    
    # Get prediction probabilities
    probabilities = _model.predict_proba(X)[0]
    
    # Get top N predictions
    top_indices = np.argsort(probabilities)[::-1][:top_n]
    
    predictions = []
    for idx in top_indices:
        role = _encoder.inverse_transform([idx])[0]
        confidence = round(float(probabilities[idx]) * 100, 1)
        predictions.append({
            "role": role,
            "confidence": confidence,
            "matched_skills": _get_role_matched_skills(skill_set, role)
        })
    
    top_prediction = predictions[0]
    logger.info(f"Top predicted role: {top_prediction['role']} ({top_prediction['confidence']}%)")
    
    return {
        "predicted_role": top_prediction["role"],
        "confidence": top_prediction["confidence"],
        "top_predictions": predictions,
        "total_skills_used": sum(feature_vector),
        "feature_coverage": round(sum(feature_vector) / len(_all_skills) * 100, 1)
    }


def _get_role_matched_skills(skill_set: set, role: str) -> List[str]:
    """Get skills that match the requirements for a specific role."""
    try:
        from skills.skill_database import get_skills_for_role
        role_data = get_skills_for_role(role)
        role_skills = set(role_data.get("technical", []) + role_data.get("soft", []))
        return sorted(list(skill_set & role_skills))[:8]
    except Exception:
        return []


def _fallback_prediction(resume_skills: List[str]) -> Dict[str, Any]:
    """
    Rule-based fallback prediction when ML model is unavailable.
    Counts skill overlap with each role's required skills.
    """
    try:
        from skills.skill_database import load_skills_db, get_all_job_roles
        db = load_skills_db()
        skill_set = {s.lower().strip() for s in resume_skills}
        
        scores = {}
        for role in get_all_job_roles():
            role_data = db.get(role, {})
            role_skills = set(
                role_data.get("technical", []) + role_data.get("soft", [])
            )
            overlap = len(skill_set & role_skills)
            scores[role] = overlap / max(len(role_skills), 1) * 100
        
        sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        predictions = [
            {"role": role, "confidence": round(score, 1), "matched_skills": []}
            for role, score in sorted_roles[:5]
        ]
        
        return {
            "predicted_role": predictions[0]["role"],
            "confidence": predictions[0]["confidence"],
            "top_predictions": predictions,
            "total_skills_used": len(skill_set),
            "feature_coverage": 0.0
        }
    except Exception as e:
        logger.error(f"Fallback prediction failed: {e}")
        return {
            "predicted_role": "Software Engineer",
            "confidence": 50.0,
            "top_predictions": [{"role": "Software Engineer", "confidence": 50.0, "matched_skills": []}],
            "total_skills_used": 0,
            "feature_coverage": 0.0
        }
