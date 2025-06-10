#To compare and score resumes

# app/resume_matcher.py

from app.parser import extract_keywords

def score_resume(jd_text, resume_text):
    jd_keywords = set(extract_keywords(jd_text))
    resume_keywords = set(extract_keywords(resume_text))
    matched_keywords = jd_keywords.intersection(resume_keywords)
    score = round((len(matched_keywords) / len(jd_keywords)) * 100, 2) if jd_keywords else 0
    return score, matched_keywords
