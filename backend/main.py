from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import uuid
import shutil
from typing import List, Optional

# Import custom modules
from nlp_engine import evaluate_answer
from resume_analyzer import analyze_resume

app = FastAPI(title="AI-Based Interview Preparation System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
QUESTIONS_FILE = os.path.join(BASE_DIR, "data", "questions.json")
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({"users": []}, f)

# Helper function to load data
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Endpoints
@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Uploads a PDF resume and returns extracted skills."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    analysis_result = analyze_resume(file_path)
    return {**analysis_result, "file_id": file_id}

@app.get("/api/questions")
def get_questions(skills: str):
    """Returns questions based on a comma-separated list of skills."""
    skill_list = [s.strip().lower() for s in skills.split(",")]
    all_questions = load_json(QUESTIONS_FILE).get("questions", [])
    
    filtered_questions = [
        q for q in all_questions 
        if q["skill"].lower() in skill_list
    ]
    
    # If no matches, return a few random ones from all questions if available
    if not filtered_questions and all_questions:
        filtered_questions = all_questions[:5]
        
    return {"questions": filtered_questions}

@app.post("/api/evaluate")
def evaluate_user_answer(
    question_id: int, 
    answer: str = Form(...), 
    reference_answer: str = Form(...),
    keywords: str = Form(...)
):
    """Evaluates a single answer and returns the score and feedback."""
    keyword_list = [k.strip() for k in keywords.split(",")]
    result = evaluate_answer(answer, reference_answer, keyword_list)
    return result

@app.post("/api/register")
def register_user(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """Simple user registration (Mock for now)."""
    # Simply log the attempt or return success
    return {"status": "success", "message": f"User {username} registered."}

# Mount frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
