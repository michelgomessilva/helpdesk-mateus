from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    tickets = relationship("Ticket", back_populates="category")