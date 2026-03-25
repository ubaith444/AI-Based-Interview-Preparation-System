import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import re

def calculate_cosine_similarity(answer, reference_answer):
    """Calculates relevance score between user answer and reference answer."""
    if not answer.strip() or not reference_answer.strip():
        return 0.0
    
    vectorizer = TfidfVectorizer()
    try:
        tfidf = vectorizer.fit_transform([answer, reference_answer])
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
        return float(similarity[0][0])
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def calculate_keyword_coverage(answer, keywords):
    """Calculates keyword coverage percentage."""
    if not keywords or not answer:
        return 0.0
    
    answer_tokens = set(re.findall(r'\w+', answer.lower()))
    match_count = sum(1 for kw in keywords if kw.lower() in answer_tokens)
    return float(match_count / len(keywords))

def analyze_sentiment(answer):
    """Analyzes sentiment (confidence proxy). Maps -1 to 1 into 0 to 1."""
    blob = TextBlob(answer)
    polarity = blob.sentiment.polarity
    # Normalize polarity to 0-1 (originally -1 to 1)
    normalized = (polarity + 1) / 2
    return float(normalized)

def evaluate_answer(answer, reference_answer, keywords):
    """Generates the weighted final score and feedback."""
    similarity_score = calculate_cosine_similarity(answer, reference_answer)
    keyword_score = calculate_keyword_coverage(answer, keywords)
    sentiment_score = analyze_sentiment(answer)
    
    # Weights: Similarity (50%), Keywords (30%), Sentiment (20%)
    final_score = (similarity_score * 50) + (keyword_score * 30) + (sentiment_score * 20)
    
    feedback = ""
    if final_score >= 80:
        feedback = "Excellent! You covered all key points with high confidence."
    elif final_score >= 50:
        feedback = "Good job, but you could include more relevant keywords or refine your explanation."
    else:
        feedback = "Try to be more specific. Focus on using technical terms and structure your response better."

    return {
        "score": round(final_score, 2),
        "similarity": round(similarity_score * 100, 2),
        "keywords": round(keyword_score * 100, 2),
        "sentiment": round(sentiment_score * 100, 2),
        "feedback": feedback
    }

if __name__ == "__main__":
    # Test
    test_ans = "Python is a high-level programming language known for its readability and versatile libraries like NumPy and Pandas."
    ref_ans = "Python is an interpreted, high-level language with clear syntax and extensive libraries for data science."
    kws = ["Python", "high-level", "libraries", "readability"]
    
    print(evaluate_answer(test_ans, ref_ans, kws))
