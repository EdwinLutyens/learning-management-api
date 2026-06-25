from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


class StudentBase(BaseModel):
    name: str
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentResponse(StudentBase):
    id: int
    created_at: datetime.datetime

    model_config = {"from_attributes": True}
