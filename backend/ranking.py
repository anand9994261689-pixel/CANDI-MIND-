import numpy as np
import spacy
from model import get_embedding

# Load spaCy model for entity extraction
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def compute_cosine_similarity(vec1, vec2):
    """
    Computes the cosine similarity between two vectors.
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot_product / (norm1 * norm2))

def get_eligibility_status(score: float) -> str:
    """
    Returns eligibility status based on the score.
    """
    if score >= 0.75:
        return "Strong Match"
    elif score >= 0.5:
        return "Moderate Match"
    else:
        return "Low Match"

def extract_entities_and_skills(text: str, skills_list: list):
    """
    Extracts skills, experience, education, and summary using spaCy and heuristics.
    """
    doc = nlp(text)
    
    # Extract matching skills
    text_lower = text.lower()
    matched_skills = [skill for skill in skills_list if skill.lower() in text_lower]
    
    # Extract entities for mock experience/education
    orgs = list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"]))
    dates = list(set([ent.text for ent in doc.ents if ent.label_ == "DATE"]))
    
    # Basic heuristics
    education_orgs = [org for org in orgs if "univ" in org.lower() or "college" in org.lower() or "institute" in org.lower()]
    education = education_orgs[0] if education_orgs else "Not specified"
    
    experience = ", ".join(dates[:2]) if dates else "Not specified"
    summary = text[:150].replace('\n', ' ') + "..." if len(text) > 150 else text.replace('\n', ' ')
    
    return matched_skills, experience, education, summary

def rank_candidates(job_description: str, skills_list: list, resumes: list):
    """
    Ranks a list of resumes against a job description and required skills.
    resumes: list of dicts {"name": filename, "text": parsed_text}
    """
    target_embedding = get_embedding(job_description)

    results = []
    for resume in resumes:
        if not resume["text"].strip():
            results.append({
                "name": resume["name"],
                "semantic_score": 0.0,
                "skill_score": 0.0,
                "final_score": 0.0,
                "classification": "Low Match",
                "skills": [],
                "experience": "Not specified",
                "education": "Not specified",
                "summary": "Empty resume."
            })
            continue
            
        resume_embedding = get_embedding(resume["text"])
        semantic_score = compute_cosine_similarity(target_embedding, resume_embedding)
        
        matched_skills, experience, education, summary = extract_entities_and_skills(resume["text"], skills_list)
        
        skill_score = len(matched_skills) / len(skills_list) if skills_list else 0.0
        final_score = (semantic_score + skill_score) / 2
        
        results.append({
            "name": resume["name"],
            "semantic_score": round(semantic_score, 2),
            "skill_score": round(skill_score, 2),
            "final_score": round(final_score, 2),
            "classification": get_eligibility_status(final_score),
            "skills": matched_skills,
            "experience": experience,
            "education": education,
            "summary": summary
        })

    # Sort results in descending order by final_score
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results
