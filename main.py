from flask import Flask, render_template, request
from app.resume_matcher import score_resume
import docx2txt
import spacy
import os

app = Flask(__name__)

# Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Load NLP model once
nlp = spacy.load("en_core_web_sm")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            resume_file = request.files['resume']
            jd_text = request.form['jd']

            if not resume_file or not jd_text.strip():
                return render_template("index.html", error="Please provide both Resume and Job Description.")

            resume_path = os.path.join("uploads", resume_file.filename)
            resume_file.save(resume_path)
            resume_text = docx2txt.process(resume_path)

            score, suggestions = score_resume(resume_text, jd_text)

            return render_template("index.html", score=round(score, 2), suggestions=suggestions)
        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {str(e)}")
    return render_template("index.html")


@app.route('/quality', methods=['GET', 'POST'])
def quality():
    if request.method == 'POST':
        try:
            resume_file = request.files['resume']
            if not resume_file:
                return render_template("quality.html", error="Please upload a resume.")

            resume_path = os.path.join("uploads", resume_file.filename)
            resume_file.save(resume_path)
            resume_text = docx2txt.process(resume_path)

            word_count = len(resume_text.split())
            score = min((word_count / 300) * 100, 100)

            feedback = []
            improvements = []

            if word_count < 150:
                feedback.append("Your resume is too short. Add more details on experience, projects, or skills.")
            elif word_count > 600:
                feedback.append("Your resume is too long. Try to keep it within 1-2 pages.")

            if "objective" not in resume_text.lower():
                improvements.append("Add a short Objective or Summary section.")
            if "experience" not in resume_text.lower():
                improvements.append("Include a section on internships or jobs.")
            if "education" not in resume_text.lower():
                improvements.append("Mention your academic background.")
            if "skills" not in resume_text.lower():
                improvements.append("Include a 'Skills' section with technologies/tools.")
            if "project" not in resume_text.lower():
                improvements.append("List at least two major projects.")
            if "certification" not in resume_text.lower():
                improvements.append("Add relevant certifications if available.")

            return render_template("quality.html", score=round(score, 2), feedback=feedback, improvements=improvements)
        except Exception as e:
            return render_template("quality.html", error=f"An error occurred: {str(e)}")
    return render_template("quality.html")


if __name__ == '__main__':
    app.run(debug=True)
