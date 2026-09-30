from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class GradePayload(BaseModel):
    marks: float
    feedback: str

class SubmissionResponse(BaseModel):
    submission_id: int
    assignment_id: int
    student_id: int
    file_name: str
    storage_path: str
    file_size_bytes: int
    submitted_at: datetime
    status: str
    marks: Optional[float]
    feedback: Optional[str]
    graded_at: Optional[datetime]

    class Config:
        from_attributes = True
