#	To compare and score resumes

# main.py

from app.resume_matcher import score_resume

if __name__ == "__main__":
    jd = input("Enter job description:\n")
    resume = input("\nEnter resume text:\n")
    score, matched = score_resume(jd, resume)

    print(f"\nMatch Score: {score}%")
    print(f"Matched Keywords: {matched}")
