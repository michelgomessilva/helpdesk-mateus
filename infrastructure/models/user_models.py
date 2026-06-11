from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="employee")

    # Relacionamentos usando strings
    tickets = relationship("Ticket", foreign_keys="Ticket.user_id", back_populates="user")
    assigned_tickets = relationship("Ticket", foreign_keys="Ticket.assigned_to", back_populates="assignee")
    history = relationship("TicketHistory", back_populates="user")