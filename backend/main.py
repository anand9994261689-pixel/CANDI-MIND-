from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from skills import SKILL_MAPPING
from parser import extract_text_from_pdf
from ranking import rank_candidates

app = FastAPI(title="AI Resume Screening API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Resume Screening API is running."}

@app.get("/api")
@app.get("/api/")
def read_api_root():
    return {"message": "AI Resume Screening API is running. Use /api/categories or /api/analyze endpoints."}

@app.get("/api/categories")
def get_categories():
    """
    Returns the categories and their associated roles.
    """
    return SKILL_MAPPING

@app.post("/api/analyze")
async def analyze_resumes(
    category: str = Form(...),
    role: str = Form(...),
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Receives category, role, job description, and a list of PDF resumes.
    Returns a ranked list of candidates.
    """
    # Validate category and role
    if category not in SKILL_MAPPING:
        raise HTTPException(status_code=400, detail="Invalid category selected.")
    if role not in SKILL_MAPPING[category]:
        raise HTTPException(status_code=400, detail="Invalid role selected for the given category.")

    skills_list = SKILL_MAPPING[category][role]

    resumes_data = []
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            continue # Skip non-PDF files
            
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)
        resumes_data.append({
            "name": file.filename,
            "text": text
        })

    if not resumes_data:
        raise HTTPException(status_code=400, detail="No valid PDF files provided.")

    ranked_candidates = rank_candidates(job_description, skills_list, resumes_data)

    return {"candidates": ranked_candidates}
