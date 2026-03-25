import fitz  # PyMuPDF
import re

# Simple list of common technical skills
SKILL_DICTIONARY = [
    "Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL", "MongoDB", 
    "FastAPI", "Docker", "AWS", "Machine Learning", "NLP", "Scikit-learn", 
    "TensorFlow", "HTML", "CSS", "Git", "GitHub", "Vite", "Chart.js"
]

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file path."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_skills(text):
    """Identifies skills from the extracted text based on SKILL_DICTIONARY."""
    if not text:
        return []
    
    found_skills = []
    # Use word boundary to avoid partial matches (e.g., 'C' matching 'React')
    for skill in SKILL_DICTIONARY:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)
            
    return sorted(list(set(found_skills)))

def analyze_resume(pdf_path):
    """Orchestrates the resume analysis and skill extraction."""
    text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(text)
    return {
        "text_preview": text[:500],  # Return preview for debugging
        "skills": skills
    }

if __name__ == "__main__":
    # Test (requires a sample PDF)
    # print(analyze_resume("sample_resume.pdf"))
    print("Resume Analyzer module ready.")
