const API_BASE = "/api";

// State Management
let currentStep = 1;
let selectedSkills = [];
let interviewQuestions = [];
let currentQuestionIndex = 0;
let interviewResults = [];
let timerInterval;

// DOM Elements
const heroSection = document.getElementById('hero');
const interviewContainer = document.getElementById('interview-container');
const resumeInput = document.getElementById('resume-input');
const dropZone = document.getElementById('drop-zone');
const proceedBtn = document.getElementById('proceed-to-skills');
const skillsList = document.getElementById('skills-list');
const startInterviewBtn = document.getElementById('start-interview-btn');
const questionText = document.getElementById('question-text');
const answerInput = document.getElementById('answer-input');
const submitAnsBtn = document.getElementById('submit-ans-btn');
const currentQNum = document.getElementById('current-q-num');
const totalQNum = document.getElementById('total-q-num');
const timerDisplay = document.getElementById('timer');
const feedbackList = document.getElementById('feedback-list');
const avgScoreElem = document.getElementById('avg-score');

// Navigation
document.getElementById('get-started-btn').addEventListener('click', () => {
    heroSection.classList.add('hidden');
    interviewContainer.classList.remove('hidden');
    showStep(1);
});

function showStep(step) {
    document.querySelectorAll('.step-card').forEach((card, idx) => {
        if (idx + 1 === step) card.classList.remove('hidden');
        else if (idx === 3 && step === 4) card.classList.remove('hidden'); // Final step
        else card.classList.add('hidden');
    });
    currentStep = step;
}

// Step 1: Resume Upload
dropZone.addEventListener('click', () => resumeInput.click());

resumeInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
});

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    document.getElementById('upload-status').innerText = "Analyzing resume... Please wait.";
    
    try {
        const response = await fetch(`${API_BASE}/upload-resume`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (data.skills && data.skills.length > 0) {
            selectedSkills = data.skills;
            renderSkills(data.skills);
            proceedBtn.classList.remove('hidden');
            document.getElementById('upload-status').innerText = `Successfully extracted ${data.skills.length} skills.`;
        } else {
            document.getElementById('upload-status').innerText = "No skills found. Please try another resume.";
        }
    } catch (err) {
        console.error(err);
        document.getElementById('upload-status').innerText = "Error analyzing resume. Is the backend running?";
    }
}

proceedBtn.addEventListener('click', () => showStep(2));

// Step 2: Skill Selection
function renderSkills(skills) {
    skillsList.innerHTML = '';
    skills.forEach(skill => {
        const tag = document.createElement('div');
        tag.className = 'skill-tag selected';
        tag.innerText = skill;
        tag.addEventListener('click', () => {
            tag.classList.toggle('selected');
        });
        skillsList.appendChild(tag);
    });
}

startInterviewBtn.addEventListener('click', async () => {
    const activeTags = document.querySelectorAll('.skill-tag.selected');
    const skills = Array.from(activeTags).map(t => t.innerText).join(',');
    
    try {
        const response = await fetch(`${API_BASE}/questions?skills=${skills}`);
        const data = await response.json();
        interviewQuestions = data.questions;
        
        if (interviewQuestions.length > 0) {
            totalQNum.innerText = interviewQuestions.length;
            startInterview();
        } else {
            alert("No questions found for selected skills.");
        }
    } catch (err) {
        alert("Failed to fetch questions.");
    }
});

// Step 3: Mock Interview
function startInterview() {
    showStep(3);
    currentQuestionIndex = 0;
    interviewResults = [];
    loadQuestion();
    startTimer();
}

function loadQuestion() {
    const q = interviewQuestions[currentQuestionIndex];
    questionText.innerText = q.question;
    currentQNum.innerText = currentQuestionIndex + 1;
    answerInput.value = '';
    answerInput.focus();
}

submitAnsBtn.addEventListener('click', async () => {
    const answer = answerInput.value.trim();
    if (!answer) return alert("Please type your answer.");

    const q = interviewQuestions[currentQuestionIndex];
    submitAnsBtn.disabled = true;
    submitAnsBtn.innerText = "Evaluating...";

    try {
        const formData = new FormData();
        formData.append('answer', answer);
        formData.append('reference_answer', q.reference_answer);
        formData.append('keywords', q.keywords.join(','));

        const response = await fetch(`${API_BASE}/evaluate?question_id=${q.id}`, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        interviewResults.push({
            question: q.question,
            answer: answer,
            ...result
        });

        nextQuestion();
    } catch (err) {
        alert("Evaluation failed.");
    } finally {
        submitAnsBtn.disabled = false;
        submitAnsBtn.innerText = "Submit Answer";
    }
});

function nextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < interviewQuestions.length) {
        loadQuestion();
    } else {
        finishInterview();
    }
}

function finishInterview() {
    clearInterval(timerInterval);
    showStep(4);
    renderDashboard();
}

// Step 4: Final Dashboard
function renderDashboard() {
    const totalScore = interviewResults.reduce((sum, r) => sum + r.score, 0);
    const avgScore = Math.round(totalScore / interviewResults.length);
    avgScoreElem.innerText = avgScore;

    // Render Chart
    const ctx = document.getElementById('scoreChart').getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: interviewResults.map((_, i) => `Q${i+1}`),
            datasets: [{
                label: 'Performance Score',
                data: interviewResults.map(r => r.score),
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(99, 102, 241, 1)'
            }]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { color: 'rgba(255,255,255,0.7)' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    // Render Feedback List
    feedbackList.innerHTML = '';
    interviewResults.forEach((res, i) => {
        const div = document.createElement('div');
        div.className = 'feedback-card';
        div.innerHTML = `
            <strong>Q${i+1}: ${res.question}</strong>
            <p style="font-size: 14px; margin-top: 8px;">Score: ${res.score}%</p>
            <p style="font-size: 14px; color: #a5b4fc; margin-top: 4px;">${res.feedback}</p>
        `;
        feedbackList.appendChild(div);
    });
}

// Utilities
function startTimer() {
    let seconds = 0;
    timerInterval = setInterval(() => {
        seconds++;
        const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
        const secs = (seconds % 60).toString().padStart(2, '0');
        timerDisplay.innerText = `${mins}:${secs}`;
    }, 1000);
}

document.getElementById('restart-btn').addEventListener('click', () => {
    location.reload();
});
