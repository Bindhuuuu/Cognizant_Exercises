"""
SkillGap AI - Text Preprocessor
Handles text cleaning, tokenization, and NLP preprocessing using NLTK.
"""

import re
import string
from typing import List, Set
from utils.logger import setup_logger

logger = setup_logger("text_preprocessor")

# Lazy-load NLTK resources
_nltk_ready = False


def _init_nltk():
    """Download required NLTK data if not already present."""
    global _nltk_ready
    if _nltk_ready:
        return
    try:
        import nltk
        for resource in ["stopwords", "punkt", "wordnet", "omw-1.4", "punkt_tab"]:
            try:
                nltk.data.find(f"tokenizers/{resource}" if resource.startswith("punkt") else f"corpora/{resource}")
            except LookupError:
                nltk.download(resource, quiet=True)
        _nltk_ready = True
    except Exception as e:
        logger.warning(f"NLTK initialization warning: {e}")


def clean_text(text: str) -> str:
    """
    Clean raw text by removing special characters, extra whitespace, and noise.
    
    Args:
        text: Raw input text
    
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)
    # Remove email addresses (keep for extraction, but clean for analysis)
    text = re.sub(r"\S+@\S+", " ", text)
    # Remove phone numbers
    text = re.sub(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", " ", text)
    # Remove special characters but keep alphanumeric and key punctuation
    text = re.sub(r"[^\w\s\.\,\-\/\+\#]", " ", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def tokenize(text: str) -> List[str]:
    """
    Tokenize text into individual words.
    
    Args:
        text: Input text string
    
    Returns:
        List of word tokens
    """
    _init_nltk()
    try:
        from nltk.tokenize import word_tokenize
        return word_tokenize(text.lower())
    except Exception:
        # Fallback simple tokenization
        return text.lower().split()


def remove_stopwords(tokens: List[str]) -> List[str]:
    """
    Remove common English stopwords from token list.
    
    Args:
        tokens: List of word tokens
    
    Returns:
        Filtered token list without stopwords
    """
    _init_nltk()
    try:
        from nltk.corpus import stopwords
        stop_words: Set[str] = set(stopwords.words("english"))
        return [t for t in tokens if t not in stop_words and len(t) > 1]
    except Exception:
        return tokens


def lemmatize(tokens: List[str]) -> List[str]:
    """
    Apply lemmatization to reduce words to base forms.
    
    Args:
        tokens: List of word tokens
    
    Returns:
        Lemmatized token list
    """
    _init_nltk()
    try:
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(t) for t in tokens]
    except Exception:
        return tokens


def preprocess_text(text: str, lemmatize_text: bool = True) -> str:
    """
    Full preprocessing pipeline: clean → tokenize → remove stopwords → lemmatize.
    
    Args:
        text: Raw input text
        lemmatize_text: Whether to apply lemmatization (default: True)
    
    Returns:
        Fully preprocessed text string
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    if lemmatize_text:
        tokens = lemmatize(tokens)
    # Remove punctuation tokens
    tokens = [t for t in tokens if t not in string.punctuation and not t.isdigit()]
    return " ".join(tokens)


def extract_keywords(text: str, top_n: int = 20) -> List[str]:
    """
    Extract top N meaningful keywords from text using TF-IDF-like frequency analysis.
    
    Args:
        text: Input text
        top_n: Number of keywords to return
    
    Returns:
        List of top keywords
    """
    preprocessed = preprocess_text(text)
    tokens = preprocessed.split()
    
    # Frequency count
    freq: dict = {}
    for token in tokens:
        if len(token) > 2:
            freq[token] = freq.get(token, 0) + 1
    
    # Sort by frequency
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [kw[0] for kw in sorted_keywords[:top_n]]
