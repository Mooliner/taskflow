# backend/models/comment.py

from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    author: str
    content: str
    created_at: datetime
