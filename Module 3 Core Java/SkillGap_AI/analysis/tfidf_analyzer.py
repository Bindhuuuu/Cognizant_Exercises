"""
SkillGap AI - TF-IDF Analyzer
Computes similarity between resume and job description using TF-IDF + Cosine Similarity.
"""

from typing import Tuple, List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.text_preprocessor import preprocess_text
from utils.logger import setup_logger

logger = setup_logger("tfidf_analyzer")


def compute_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute cosine similarity between resume and job description using TF-IDF.
    
    Args:
        resume_text: Full resume text
        jd_text: Full job description text
    
    Returns:
        Similarity score as a percentage (0-100)
    """
    if not resume_text or not jd_text:
        logger.warning("Empty text provided for similarity computation")
        return 0.0
    
    # Preprocess both texts
    processed_resume = preprocess_text(resume_text)
    processed_jd = preprocess_text(jd_text)
    
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),  # Unigrams and bigrams
        max_features=5000,
        min_df=1,
        stop_words="english"
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([processed_resume, processed_jd])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        similarity_pct = round(float(similarity) * 100, 2)
        logger.info(f"TF-IDF cosine similarity: {similarity_pct}%")
        return similarity_pct
    except Exception as e:
        logger.error(f"TF-IDF computation error: {e}")
        return 0.0


def get_tfidf_top_keywords(
    text: str,
    top_n: int = 15
) -> List[Tuple[str, float]]:
    """
    Extract top TF-IDF weighted keywords from a document.
    
    Args:
        text: Input text
        top_n: Number of top keywords to return
    
    Returns:
        List of (keyword, score) tuples sorted by score
    """
    if not text:
        return []
    
    processed = preprocess_text(text)
    
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=200,
        stop_words="english"
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform([processed])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Sort by score descending
        keyword_scores = sorted(
            zip(feature_names, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return keyword_scores[:top_n]
    except Exception as e:
        logger.error(f"TF-IDF keyword extraction error: {e}")
        return []


def keyword_match_analysis(
    resume_text: str,
    jd_text: str
) -> Dict:
    """
    Analyze keyword overlap between resume and JD.
    
    Args:
        resume_text: Resume text
        jd_text: Job description text
    
    Returns:
        Dictionary with overlap stats and keyword lists
    """
    jd_keywords = {kw for kw, _ in get_tfidf_top_keywords(jd_text, top_n=30)}
    resume_keywords = {kw for kw, _ in get_tfidf_top_keywords(resume_text, top_n=50)}
    
    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords
    
    return {
        "jd_keywords": list(jd_keywords),
        "resume_keywords": list(resume_keywords),
        "matched_keywords": list(matched),
        "missing_keywords": list(missing),
        "keyword_match_pct": round(len(matched) / len(jd_keywords) * 100, 1) if jd_keywords else 0.0
    }
