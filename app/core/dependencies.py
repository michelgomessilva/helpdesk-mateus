from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from infrastructure.database.database import get_db
from infrastructure.repositories.category_repository import CategoryRepository
from infrastructure.repositories.ticket_repository import TicketRepository
from infrastructure.repositories.comment_repository import CommentRepository
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.ticket_history_repository import TicketHistoryRepository

def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)

def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    return TicketRepository(db)

def get_comment_repository(db: Session = Depends(get_db)) -> CommentRepository:
    return CommentRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_ticket_history_repository(db: Session = Depends(get_db)) -> TicketHistoryRepository:
    return TicketHistoryRepository(db)

def require_roles(*allowed_roles: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Permissão insuficiente")
        return current_user
    return role_checker