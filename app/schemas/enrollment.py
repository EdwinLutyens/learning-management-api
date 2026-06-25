from pydantic import BaseModel
from typing import Optional
import datetime
from app.schemas.student import StudentResponse
from app.schemas.course import CourseResponse


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime.datetime

    model_config = {"from_attributes": True}


class EnrollmentDetailResponse(EnrollmentResponse):
    student: StudentResponse
    course: CourseResponse
