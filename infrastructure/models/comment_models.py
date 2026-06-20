from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    author_name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    ticket = relationship("Ticket", back_populates="comments")