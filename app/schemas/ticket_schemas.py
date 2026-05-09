from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TicketBase(BaseModel):
    title: str
    description: str
    category_id: int = Field(gt=0, description="ID da categoria do ticket")
    priority: Literal["baixa", "media", "alta"]
    status: Literal["aberto", "em_andamento", "fechado"]

    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("category_id deve ser maior que 0")
        return v


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category_id: int | None = None
    priority: Literal["baixa", "media", "alta"] | None = None
    status: Literal["aberto", "em_andamento", "fechado"] | None = None


class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
