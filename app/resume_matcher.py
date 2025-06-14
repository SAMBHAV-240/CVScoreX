import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def clean_and_tokenize(text):
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

def score_resume(resume_text, jd_text):
    resume_keywords = set(clean_and_tokenize(resume_text))
    jd_keywords = set(clean_and_tokenize(jd_text))

    matched_keywords = resume_keywords.intersection(jd_keywords)
    total_keywords = len(jd_keywords)
    score = (len(matched_keywords) / total_keywords) * 100 if total_keywords > 0 else 0

    # Only take top 5 missing keywords
    missing_keywords = list(jd_keywords - matched_keywords)[:5]

    # AI-like suggestions (static logic for now; you can later use real LLM APIs here)
    suggestions = []
    if "project" not in resume_text.lower():
        suggestions.append("Include a 'Projects' section showcasing relevant academic or personal work.")
    if "lead" not in resume_text.lower():
        suggestions.append("Try including leadership experiences or team coordination efforts.")
    if "intern" not in resume_text.lower():
        suggestions.append("Mention any internships or real-world experiences you’ve had.")
    if "skills" not in resume_text.lower():
        suggestions.append("List key tools, frameworks, and languages in a dedicated 'Skills' section.")
    if "achievement" not in resume_text.lower() and "award" not in resume_text.lower():
        suggestions.append("Mention notable achievements, awards, or recognitions.")

    return round(score, 2), suggestions
