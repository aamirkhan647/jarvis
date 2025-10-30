from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def lightweight_score(jd_text: str, resume_text: str) -> float:
    """
    Calculates a fast, non-LLM relevance score using TF-IDF and Cosine Similarity.
    Score is normalized 0.0 to 1.0.
    """
    if not jd_text or not resume_text:
        return 0.0

    documents = [jd_text, resume_text]

    # Initialize TF-IDF Vectorizer (Can add stop words, n-grams, etc., for refinement)
    vectorizer = TfidfVectorizer()

    # Fit and transform
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)

        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        return float(similarity)
    except ValueError:
        # Handle cases where input is too short or empty after tokenization
        return 0.0
