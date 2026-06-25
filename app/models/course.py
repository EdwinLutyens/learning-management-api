from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructors.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    instructor = relationship("Instructor", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
