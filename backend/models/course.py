from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(150), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("User", back_populates="taught_courses")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")
