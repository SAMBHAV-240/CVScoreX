from flask import Flask, render_template, request
from app.resume_matcher import score_resume
from app.utils import extract_text_from_file
import docx2txt
import spacy
import os


app = Flask(__name__)

# Ensure 'uploads' directory exists
os.makedirs("uploads", exist_ok=True)

# Load SpaCy model once globally
nlp = spacy.load("en_core_web_sm")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            resume_file = request.files.get('resume')
            jd_text = request.form.get('jd', '')

            if not resume_file or not jd_text.strip():
                return render_template("index.html", error="Please upload a resume and enter a job description.")

            resume_path = os.path.join("uploads", resume_file.filename)
            resume_file.save(resume_path)
            resume_text = extract_text_from_file(resume_path)

            score, suggestions = score_resume(resume_text, jd_text)

            return render_template("index.html", score=round(score, 2), suggestions=suggestions, resume_text=resume_text)

        except Exception as e:
            return render_template("index.html", error=f"Error: {str(e)}")

    return render_template("index.html")

@app.route('/quality', methods=['GET', 'POST'])
def quality():
    if request.method == 'POST':
        try:
            resume_file = request.files.get('resume')

            if not resume_file:
                return render_template("quality.html", error="Please upload a resume.")

            resume_path = os.path.join("uploads", resume_file.filename)
            resume_file.save(resume_path)
            resume_text = extract_text_from_file(resume_path)

            word_count = len(resume_text.split())
            base_score = min((word_count / 300) * 100, 100)
            deduction = 0
            feedback = []

            if word_count < 150:
                feedback.append("Your resume is too short. Add more details on experience, projects, or skills.")
                deduction += 15
            elif word_count > 600:
                feedback.append("Your resume is too long. Try to keep it within 1-2 pages.")
                deduction += 10

            improvements = []

            def check_and_deduct(keyword, message, penalty):
                nonlocal deduction
                if keyword not in resume_text.lower():
                    improvements.append(message)
                    deduction += penalty

            check_and_deduct("objective", "Include a brief objective or summary.", 5)
            check_and_deduct("experience", "Include a section on internships, jobs, or work experience.", 7)
            check_and_deduct("education", "Mention your academic qualifications clearly.", 5)
            check_and_deduct("skills", "Add a 'Skills' section with technical and soft skills.", 5)
            check_and_deduct("project", "List 2-3 key projects and what you worked on.", 7)
            check_and_deduct("certification", "Mention any relevant certifications.", 3)

            # Cap score after deductions
            final_score = max(100 - deduction, 20)

            return render_template(
                "quality.html",
                score=round(final_score, 2),
                feedback=feedback,
                improvements=improvements
            )

        except Exception as e:
            return render_template("quality.html", error=f"Error: {str(e)}")

    return render_template("quality.html")

if __name__ == '__main__':
    app.run(debug=True)
