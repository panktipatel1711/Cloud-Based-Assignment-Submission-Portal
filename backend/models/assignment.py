from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from backend.database import Base

class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=False)
    max_marks = Column(Float, default=100.0)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")
