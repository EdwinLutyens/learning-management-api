from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


class InstructorBase(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str] = None


class InstructorCreate(InstructorBase):
    pass


class InstructorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None


class InstructorResponse(InstructorBase):
    id: int
    created_at: datetime.datetime

    model_config = {"from_attributes": True}
