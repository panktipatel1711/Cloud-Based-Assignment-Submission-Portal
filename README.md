# Cloud-Based Student Assignment Submission & Feedback Portal

A decoupled coursework management platform built with FastAPI, React, and S3-compatible Object Storage.

## Key Architectural Concepts
- **Stateless Authentication:** JSON Web Tokens (PyJWT) with bcrypt hashing.
- **Role-Based Access Control (RBAC):** Permissions for Students and Teachers.
- **Cloud Object Storage:** Decoupled storage engine for local buckets or AWS S3.
- **Server-Side Deadline Enforcement:** Uses trusted server UTC timestamps.

## Quickstart Guide

### 1. Backend
```bash
python -m venv venv
# Windows:
.\\venv\\Scripts\\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
python -m uvicorn backend.app:app --reload --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
