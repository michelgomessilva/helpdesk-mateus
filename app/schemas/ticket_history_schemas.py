from pydantic import BaseModel
from datetime import datetime

class TicketHistoryResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    field_name: str
    old_value: str | None
    new_value: str | None
    created_at: datetime

class TicketHistoryResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    field_name: str
    old_value: str | None
    new_value: str | None
    created_at: datetime