import re
import PyPDF2
from sentence_transformers import SentenceTransformer, util

# Load SBERT once
model = SentenceTransformer("all-MiniLM-L6-v2")

SKILL_KEYWORDS = [
    "python", "django", "flask", "html", "css", "javascript", "sql",
    "pandas", "numpy", "aws", "machine learning", "ai",
    "react", "node", "git", "api", "rest", "docker", "linux"
]

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception:
        return ""
    return text.strip()

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.append(skill)
    return found

def generate_insights(similarity, resume_skills, jd_skills):
    insights = []

    matched_skills = set(resume_skills).intersection(jd_skills)
    missing_skills = set(jd_skills) - set(resume_skills)

    if similarity >= 0.7:
        insights.append("Strong project relevance to the job role")
    elif similarity >= 0.45:
        insights.append("Moderate project relevance based on past work")
    else:
        insights.append("Limited project relevance to the job requirements")

    if matched_skills:
        insights.append(
            f"Matches required skills such as {', '.join(sorted(list(matched_skills)))}"
        )

    if missing_skills:
        insights.append(
            f"Missing some preferred skills like {', '.join(sorted(list(missing_skills)))}"
        )

    return "; ".join(insights)


def run_ai_screening(job_description, applications):
    results = []
    jd_skills = extract_skills(job_description)

    for application in applications:
        resume_text = extract_text_from_pdf(application.resume.path)

        if not resume_text or not job_description:
            results.append({
                "application": application,
                "score": 0.0,
                "skills": [],
                "insights": "Insufficient data available for AI evaluation."
            })
            continue
        jd_embedding = model.encode(
            job_description,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        resume_embedding = model.encode(
            resume_text,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        similarity = util.cos_sim(jd_embedding, resume_embedding).item()

        if similarity < 0.01:
            similarity = 0.01

        score = round(similarity * 100, 2)
        resume_skills = extract_skills(resume_text)

        insight = generate_insights(
            similarity,
            resume_skills,
            jd_skills
        )

        results.append({
            "application": application,
            "score": score,
            "skills": resume_skills,
            "insights": insight
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
