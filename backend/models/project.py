from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    owner_email: EmailStr

class ProjectInDB(ProjectBase):
    id: str
    owner_email: EmailStr
    members: List[EmailStr] = []

    class Config:
        orm_mode = True
