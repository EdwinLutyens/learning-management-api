from pydantic import BaseModel, Field
from typing import Optional
import datetime


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    capacity: int = Field(..., gt=0, description="Max number of students allowed")
    instructor_id: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    capacity: Optional[int] = Field(default=None, gt=0)
    instructor_id: Optional[int] = None


class CourseResponse(CourseBase):
    id: int
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


class CourseWithEnrollmentCount(CourseResponse):
    enrolled_count: int
    seats_available: int
