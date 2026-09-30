from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AssignmentCreate(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    deadline: datetime
    max_marks: float = 100.0

class AssignmentResponse(BaseModel):
    assignment_id: int
    course_id: int
    title: str
    description: Optional[str]
    deadline: datetime
    max_marks: float
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
