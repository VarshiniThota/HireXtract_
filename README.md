# HireXtract – AI-Powered Recruitment System 🚀

HireXtract is a monolithic, AI-driven recruitment web application designed to automate resume screening, candidate ranking, and interview communication for a single organization.  
The system leverages **semantic AI models (Sentence-BERT)** to intelligently match resumes with job descriptions, enabling HR teams to make faster, unbiased, and data-driven hiring decisions.

---

## 🔍 Problem Statement
Traditional recruitment processes require HR teams to manually screen hundreds of resumes, which is time-consuming, error-prone, and often biased.  
HireXtract addresses this challenge by introducing AI-based semantic resume analysis and automated candidate ranking.

---

## ✨ Key Features

### 👨‍💼 HR Module
- Create, manage, and close job openings
- View number of applications per job
- Run AI-based resume screening
- Automatically rank candidates based on AI scores
- Filter candidates using **Top-N ranking** (Top 5, Top 10, Top 20, etc.)
- Bulk shortlist candidates for interviews
- Automatically reject non-selected candidates
- Send interview invite and rejection emails
- Secure HR authentication and access control


## 🤖 AI Screening Engine
- Resume text extraction from PDFs
- OCR fallback using Tesseract for scanned resumes
- Semantic similarity scoring using **Sentence-BERT (SBERT)**
- Cosine similarity-based AI scoring
- AI-generated insights including:
  - Skill match analysis
  - Project relevance
  - Overall alignment with job description
- Rank-based candidate evaluation

---

## 🧠 Technologies Used

### Backend
- Django
- Python

### Frontend
- HTML
- CSS
- Bootstrap

### AI / ML
- Sentence-BERT (`all-MiniLM-L6-v2`)
- Natural Language Processing (NLP)
- Cosine Similarity


### Database
- SQLite

---

## 🏗️ System Architecture
HireXtract follows a **monolithic architecture**, where all modules (HR, Candidate, AI Screening, Email Service) are integrated into a single Django application, ensuring simplicity and ease of deployment for a single organization.

---

## 🔒 Security
- Role-based authentication (HR vs Candidate)
- Secure file handling for resume uploads
- Email communication through authenticated SMTP

---

## 🚀 Future Enhancements
- Support for multi-company (multi-tenant) architecture
- Domain-specific skill extraction (Finance, Marketing, Cloud, etc.)
- Integration with external job portals
- Interview scheduling and calendar integration
- Advanced analytics dashboard for HR

---

## 🎯 Outcome
HireXtract significantly reduces manual effort in recruitment, improves screening accuracy using AI, and ensures a structured, transparent, and efficient hiring workflow.

---

## 👨‍💻 Developed By
A student-driven project focused on applying **AI, NLP, and full-stack development** concepts to solve real-world recruitment challenges.
