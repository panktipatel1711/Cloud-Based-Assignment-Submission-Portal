import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.assignment import Assignment
from backend.models.submission import Submission
from backend.models.user import User
from backend.schemas.submission import SubmissionResponse, GradePayload
from backend.middleware.auth_guard import get_current_user, require_role
from backend.cloud.storage_service import storage_service

router = APIRouter(prefix="/api", tags=["Submissions"])

ALLOWED_EXTENSIONS = {"pdf", "docx", "zip", "png", "jpg"}
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB

@router.post("/assignments/{id}/submit", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_assignment(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["student"]))
):
    assignment = db.query(Assignment).filter(Assignment.assignment_id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")

    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type .{ext}. Permitted formats: {list(ALLOWED_EXTENSIONS)}"
        )

    contents = await file.read()
    file_size = len(contents)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 15 MB limit.")
    await file.seek(0)

    now = datetime.utcnow()
    submission_status = "LATE" if now > assignment.deadline else "SUBMITTED"

    unique_key = f"assignments/course_{assignment.course_id}/assign_{id}/std_{current_user.user_id}_{int(now.timestamp())}_{uuid.uuid4().hex[:6]}.{ext}"
    storage_path = storage_service.upload_file(file, unique_key)

    submission = db.query(Submission).filter(
        Submission.assignment_id == id,
        Submission.student_id == current_user.user_id
    ).first()

    if submission:
        submission.file_name = file.filename
        submission.storage_path = storage_path
        submission.file_size_bytes = file_size
        submission.submitted_at = now
        submission.status = submission_status
    else:
        submission = Submission(
            assignment_id=id,
            student_id=current_user.user_id,
            file_name=file.filename,
            storage_path=storage_path,
            file_size_bytes=file_size,
            submitted_at=now,
            status=submission_status
        )
        db.add(submission)

    db.commit()
    db.refresh(submission)
    return submission

@router.get("/submissions/me", response_model=List[SubmissionResponse])
def get_my_submissions(db: Session = Depends(get_db), current_user: User = Depends(require_role(["student"]))):
    return db.query(Submission).filter(Submission.student_id == current_user.user_id).all()

@router.get("/assignments/{id}/submissions", response_model=List[SubmissionResponse])
def get_assignment_submissions(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["teacher"]))
):
    return db.query(Submission).filter(Submission.assignment_id == id).all()

@router.get("/submissions/{id}/download")
def download_submission(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    submission = db.query(Submission).filter(Submission.submission_id == id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission record not found.")

    if current_user.role == "student" and submission.student_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to another student's file.")

    physical_path = storage_service.get_file_path(submission.storage_path)
    return FileResponse(
        path=physical_path,
        filename=submission.file_name,
        media_type="application/octet-stream"
    )

@router.post("/submissions/{id}/grade", response_model=SubmissionResponse)
def grade_submission(
    id: int,
    payload: GradePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["teacher"]))
):
    submission = db.query(Submission).filter(Submission.submission_id == id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found.")

    assignment = db.query(Assignment).filter(Assignment.assignment_id == submission.assignment_id).first()
    if payload.marks < 0 or payload.marks > assignment.max_marks:
        raise HTTPException(
            status_code=400,
            detail=f"Marks must be between 0 and maximum permitted ({assignment.max_marks})."
        )

    submission.marks = payload.marks
    submission.feedback = payload.feedback
    submission.graded_at = datetime.utcnow()
    submission.status = "GRADED"

    db.commit()
    db.refresh(submission)
    return submission
