from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.assignment import Assignment
from backend.models.submission import Submission
from backend.models.user import User
from backend.middleware.auth_guard import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/dashboard")
def get_dashboard_metrics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == "teacher":
        total_assignments = db.query(Assignment).count()
        total_students = db.query(User).filter(User.role == "student").count()
        total_submissions = db.query(Submission).count()
        pending_grading = db.query(Submission).filter(Submission.status.in_(["SUBMITTED", "LATE"])).count()
        graded_submissions = db.query(Submission).filter(Submission.status == "GRADED").count()
        
        return {
            "role": "teacher",
            "total_assignments": total_assignments,
            "total_students": total_students,
            "total_submissions": total_submissions,
            "pending_grading": pending_grading,
            "graded_submissions": graded_submissions
        }
    else:
        total_assignments = db.query(Assignment).count()
        my_submissions = db.query(Submission).filter(Submission.student_id == current_user.user_id).all()
        submitted_count = len(my_submissions)
        graded_count = sum(1 for s in my_submissions if s.status == "GRADED")
        late_count = sum(1 for s in my_submissions if s.status == "LATE")
        pending_assignments = max(0, total_assignments - submitted_count)

        return {
            "role": "student",
            "total_assignments": total_assignments,
            "submitted": submitted_count,
            "graded": graded_count,
            "late": late_count,
            "pending": pending_assignments
        }
