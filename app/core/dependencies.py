from fastapi import Depends
from sqlalchemy.orm import Session
from infrastructure.database.database import get_db
from infrastructure.repositories.category_repository import CategoryRepository
from infrastructure.repositories.ticket_repository import TicketRepository
from infrastructure.repositories.comment_repository import CommentRepository

def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)

def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    return TicketRepository(db)

def get_comment_repository(db: Session = Depends(get_db)) -> CommentRepository:
    return CommentRepository(db)