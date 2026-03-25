# 🤖 AI-Based Interview Preparation System

## 📌 Overview

The AI-Based Interview Preparation System is a lightweight, NLP-powered web application designed to help students prepare for technical interviews.
It simulates a mock interview environment by generating questions, evaluating user responses, and providing structured feedback.

---

## 🎯 Objectives

* Simulate real interview scenarios
* Evaluate candidate answers using NLP techniques
* Identify weak areas and suggest improvements
* Provide a performance dashboard

---

## 🧠 Key Features

### 1. User Module

* Basic registration and login (email & password)
* Tracks user progress and performance

### 2. Resume Analyzer

* Upload PDF resume
* Extracts text using PyMuPDF
* Identifies key skills (e.g., Python, React)
* Generates role-specific interview questions

### 3. Question Generator

* Uses a predefined question bank (JSON)
* Filters questions based on extracted skills
* Optional LLM-based question generation (upgrade)

### 4. Answer Input

* Text-based answer submission
* (Optional) Voice input for enhanced interaction

### 5. Answer Evaluation Engine

Evaluates answers using:

* Cosine Similarity (relevance)
* Keyword Matching (coverage)
* Sentiment Analysis (confidence)

Generates:

* Score (0–100)
* Feedback message

### 6. Feedback Dashboard

* Displays scores per question
* Shows performance trends
* Identifies weak topics

### 7. Mock Interview Flow

* Role selection
* Question sequence
* Answer submission
* Evaluation and final report

---

## 🏗️ System Architecture

Frontend (HTML/CSS/JS)
↓
Backend (FastAPI)
↓
NLP Engine (TextBlob, Scikit-learn)
↓
Database (MongoDB / JSON)

---

## 🔄 Data Flow

1. User uploads resume
2. System extracts skills
3. Questions are generated based on skills
4. User submits answers
5. NLP engine evaluates responses
6. Scores and feedback are generated
7. Results are displayed in dashboard

---

## 🧰 Tech Stack

### Frontend

* HTML, CSS, JavaScript
* Chart.js (for dashboard)

### Backend

* FastAPI
* Uvicorn

### NLP & Processing

* TextBlob
* Scikit-learn

### Database

* MongoDB (optional)
* JSON (for lightweight storage)

---

## ⚙️ Installation & Setup

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn pymongo textblob scikit-learn python-multipart pymupdf
uvicorn main:app --reload
```

### Frontend Setup

* Open `index.html` in browser
* Ensure backend is running

---

## 📊 Evaluation Methodology

The system evaluates answers using a weighted scoring approach:

* Relevance (Cosine Similarity) → 50%
* Keyword Coverage → 30%
* Sentiment Confidence → 20%

Final Score:

```
Score = (Similarity × 50) + (Keywords × 30) + (Sentiment × 20)
```

---

## 🚀 Future Enhancements

* Voice-based interview (speech-to-text)
* AI-generated questions using LLM APIs
* Advanced resume parsing using ML
* Real-time feedback with suggestions
* Deployment as a mobile app (React Native)

---

## ⚠️ Limitations

* Evaluation is heuristic-based (not true AI reasoning)
* Limited dataset for questions
* Basic authentication (no security layers)
* Sentiment ≠ actual confidence (approximation)

---

## 🧠 Conclusion

This system provides a practical and scalable approach to interview preparation using NLP techniques.
It balances simplicity, usability, and intelligent feedback while remaining fully cost-free and deployable.

---

## 👨‍💻 Author

Developed as a college project for AI & Data Science.
