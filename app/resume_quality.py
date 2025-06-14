import re

def score_resume_quality(resume_text):
    score = 0
    feedback = []

    if re.search(r'\bexperience\b', resume_text, re.I):
        score += 20
    else:
        feedback.append("Add an 'Experience' section.")

    if re.search(r'\beducation\b', resume_text, re.I):
        score += 20
    else:
        feedback.append("Include your 'Education' background.")

    if re.search(r'\b(project|projects)\b', resume_text, re.I):
        score += 20
    else:
        feedback.append("Mention at least one project.")

    if re.search(r'\b(skill|skills)\b', resume_text, re.I):
        score += 20
    else:
        feedback.append("List relevant skills.")

    if re.search(r'\b(contact|email|phone|linkedin)\b', resume_text, re.I):
        score += 20
    else:
        feedback.append("Add your contact details.")

    return score, feedback
