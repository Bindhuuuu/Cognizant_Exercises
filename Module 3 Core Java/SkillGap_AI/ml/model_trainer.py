"""
SkillGap AI - ML Model Trainer
Trains a RandomForestClassifier to predict job roles from skill vectors.
Generates synthetic training data based on the skill database.
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from skills.skill_database import load_skills_db, get_all_job_roles
from utils.logger import setup_logger

logger = setup_logger("model_trainer")

# Model save paths
_MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
_MODEL_PATH = os.path.join(_MODEL_DIR, "job_role_model.pkl")
_SKILLS_LIST_PATH = os.path.join(_MODEL_DIR, "all_skills.pkl")
_ENCODER_PATH = os.path.join(_MODEL_DIR, "label_encoder.pkl")


def generate_training_data() -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Generate synthetic training data from the skill database.
    Each job role generates multiple samples with slight variations
    to simulate real-world resume diversity.
    
    Returns:
        Tuple of (X feature matrix, y labels, all_skills list)
    """
    db = load_skills_db()
    roles = get_all_job_roles()
    
    # Master skill list (defines feature dimensions)
    all_skills_set = set()
    for role_data in db.values():
        all_skills_set.update(role_data.get("technical", []))
        all_skills_set.update(role_data.get("soft", []))
    all_skills = sorted(list(all_skills_set))
    
    logger.info(f"Feature space: {len(all_skills)} unique skills across {len(roles)} roles")
    
    X_rows = []
    y_labels = []
    
    np.random.seed(42)
    
    for role in roles:
        role_data = db[role]
        tech_skills = role_data.get("technical", [])
        soft_skills = role_data.get("soft", [])
        required_skills = tech_skills + soft_skills
        required_set = set(required_skills)
        
        # Generate 50 samples per role with noise
        for _ in range(50):
            feature_vector = []
            for skill in all_skills:
                if skill in required_set:
                    # Core role skills: 70-100% chance of appearing
                    presence = 1 if np.random.random() > 0.25 else 0
                else:
                    # Non-role skills: 0-15% noise chance
                    presence = 1 if np.random.random() < 0.10 else 0
                feature_vector.append(presence)
            
            X_rows.append(feature_vector)
            y_labels.append(role)
    
    X = np.array(X_rows)
    y = np.array(y_labels)
    
    logger.info(f"Generated {len(X)} training samples")
    return X, y, all_skills


def train_model(force_retrain: bool = False) -> Dict:
    """
    Train the job role prediction model and save to disk.
    
    Args:
        force_retrain: If True, retrain even if model exists
    
    Returns:
        Dictionary with training results
    """
    # Check if model already exists
    if not force_retrain and _model_exists():
        logger.info("Pre-trained model found. Skipping training.")
        return {"status": "loaded", "message": "Model loaded from disk"}
    
    logger.info("Training job role prediction model...")
    
    # Generate data
    X, y, all_skills = generate_training_data()
    
    # Encode labels
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Train RandomForest model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    
    # Save model artifacts
    os.makedirs(_MODEL_DIR, exist_ok=True)
    
    with open(_MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    
    with open(_SKILLS_LIST_PATH, "wb") as f:
        pickle.dump(all_skills, f)
    
    with open(_ENCODER_PATH, "wb") as f:
        pickle.dump(encoder, f)
    
    logger.info(f"Model saved to {_MODEL_PATH}")
    
    return {
        "status": "trained",
        "accuracy": round(accuracy * 100, 1),
        "samples": len(X),
        "roles": len(encoder.classes_),
        "features": len(all_skills)
    }


def _model_exists() -> bool:
    """Check if trained model files exist."""
    return (
        os.path.exists(_MODEL_PATH) and
        os.path.exists(_SKILLS_LIST_PATH) and
        os.path.exists(_ENCODER_PATH)
    )


def load_model():
    """Load the trained model and associated artifacts from disk."""
    try:
        with open(_MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(_SKILLS_LIST_PATH, "rb") as f:
            all_skills = pickle.load(f)
        with open(_ENCODER_PATH, "rb") as f:
            encoder = pickle.load(f)
        logger.info("Model loaded successfully from disk")
        return model, all_skills, encoder
    except FileNotFoundError:
        logger.warning("Model files not found. Training now...")
        train_model()
        return load_model()
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None, None
