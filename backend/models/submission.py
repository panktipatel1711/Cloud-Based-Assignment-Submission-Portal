from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from backend.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    storage_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="SUBMITTED")
    marks = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    graded_at = Column(DateTime, nullable=True)

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", back_populates="submissions")
