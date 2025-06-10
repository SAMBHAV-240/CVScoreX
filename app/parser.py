#For extracting keywords from resume/JD

# app/parser.py

import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ"] and not token.is_stop]
    return list(set(keywords))
