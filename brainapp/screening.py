import re
import PyPDF2
from sentence_transformers import SentenceTransformer, util
from pdf2image import convert_from_path
import pytesseract
import os

SKILL_KEYWORDS = [
    "python", "django", "flask", "html", "css", "javascript", "sql",
    "pandas", "numpy", "aws", "ai", "machine learning",
    "react", "node", "git", "api", "rest"
]

SECTION_WEIGHTS = {
    "skills": 0.4,
    "experience": 0.3,
    "projects": 0.3
}

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception:
        pass
    if text.strip():
        return text.strip()
    try:
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)
    except Exception:
        return ""

    return text.strip()

def extract_sections(text):
    sections = {
        "skills": "",
        "experience": "",
        "projects": ""
    }

    current_section = None
    for line in text.split("\n"):
        lower = line.lower()
        if "skill" in lower:
            current_section = "skills"
        elif "experience" in lower or "work history" in lower:
            current_section = "experience"
        elif "project" in lower:
            current_section = "projects"
        if current_section:
            sections[current_section] += line + " "
    return sections

def extract_skills(text):
    text = text.lower()
    found = set()
    for skill in SKILL_KEYWORDS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill)
    return sorted(found)

def extract_jd_skills(jd_text):
    jd_text = jd_text.lower()
    return [skill for skill in SKILL_KEYWORDS if skill in jd_text]

def semantic_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    return util.pytorch_cos_sim(emb1, emb2).item()

def generate_insights(candidate_skills, jd_skills, section_scores):
    insights = []
    matched = set(candidate_skills).intersection(jd_skills)
    missing = set(jd_skills) - set(candidate_skills)

    if matched:
        insights.append(f"Strong skill match in {', '.join(sorted(matched))}")
    if missing:
        insights.append(f"Missing preferred skills: {', '.join(sorted(missing))}")

    exp = section_scores.get("experience", 0)
    proj = section_scores.get("projects", 0)

    if exp > 0.6:
        insights.append("Relevant professional experience")
    elif exp > 0.3:
        insights.append("Moderate experience relevance")
    else:
        insights.append("Limited experience relevance")

    if proj > 0.5:
        insights.append("Strong project alignment with job role")

    return "; ".join(insights)

def run_ai_screening(job_description, applications):
    results = []
    jd_skills = extract_jd_skills(job_description)

    for application in applications:
        resume_text = extract_text_from_pdf(application.resume.path)

        if not resume_text:
            results.append({
                "application": application,
                "score": 0.0,
                "skills": [],
                "insights": "Resume text could not be extracted"
            })
            continue

        sections = extract_sections(resume_text)
        skills = extract_skills(resume_text)

        final_score = 0.0
        section_scores = {}

        for section, weight in SECTION_WEIGHTS.items():
            sec_score = semantic_similarity(
                job_description,
                sections.get(section, "")
            )
            section_scores[section] = sec_score
            final_score += sec_score * weight

        score = round(final_score * 100, 2)
        insights = generate_insights(skills, jd_skills, section_scores)

        results.append({
            "application": application,
            "score": score,
            "skills": skills,
            "insights": insights
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
