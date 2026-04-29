from pydantic import BaseModel
from datetime import datetime

class CommentBase (BaseModel):
    ticket_id: int
    author_name: str
    content: str

class CommentCreate (CommentBase):
   pass

class CommentResponse (CommentBase):
    id: int
    created_at: datetime
