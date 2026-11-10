import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.resume import SKILLS

def _find_skills(text):
    low = text.lower()
    return sorted({s for s in SKILLS if re.search(r"(?<![a-z0-9])"+re.escape(s)+r"(?![a-z0-9])", low)})

def match_resume_to_job(resume, jd):
    resume_skills, job_skills = set(_find_skills(resume)), set(_find_skills(jd))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    skill_score = round(100 * len(matched) / len(job_skills)) if job_skills else 0
    try:
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=5000).fit_transform([resume, jd])
        similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        similarity_score = round(similarity * 100)
    except ValueError:
        similarity_score = 0
    score = round(0.7 * skill_score + 0.3 * similarity_score)
    recs = []
    if missing:
        recs.append("Prioritize learning or demonstrating these role requirements: " + ", ".join(missing[:8]) + ".")
        recs.append("If you have used any missing skill, add a truthful project or experience bullet showing how you applied it.")
    if similarity_score < 35:
        recs.append("Tailor your summary and project descriptions using relevant wording from the job description, without keyword stuffing.")
    if not matched:
        recs.append("Add a clearly labelled technical-skills section and describe relevant projects with tools, actions and outcomes.")
    if len(resume.split()) < 180:
        recs.append("Consider adding concise project, internship and achievement details if they are relevant and verifiable.")
    if not recs:
        recs.append("Your detected skill coverage is strong. Improve impact by adding measurable outcomes and role-specific project evidence.")
    return {"score":score,"skill_score":skill_score,"similarity_score":similarity_score,
            "matched_skills":matched,"missing_skills":missing,"required_skills":sorted(job_skills),
            "recommendations":recs}
