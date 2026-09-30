from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.assignment import Assignment
from backend.models.course import Course
from backend.models.user import User
from backend.schemas.assignment import AssignmentCreate, AssignmentResponse
from backend.middleware.auth_guard import get_current_user, require_role

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])

@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["teacher"]))
):
    course = db.query(Course).filter(Course.course_id == payload.course_id).first()
    if not course:
        course = Course(course_name="Cloud Computing", teacher_id=current_user.user_id)
        db.add(course)
        db.commit()
        db.refresh(course)
        payload.course_id = course.course_id

    assignment = Assignment(
        course_id=payload.course_id,
        title=payload.title,
        description=payload.description,
        deadline=payload.deadline,
        max_marks=payload.max_marks,
        created_by=current_user.user_id
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.get("", response_model=List[AssignmentResponse])
def list_assignments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Assignment).order_by(Assignment.deadline.asc()).all()

@router.get("/{id}", response_model=AssignmentResponse)
def get_assignment(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assignment = db.query(Assignment).filter(Assignment.assignment_id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    return assignment
