import datetime

from pydantic import BaseModel


class TicketRepository(BaseModel):
    def __init__(self):
        self._tickets = []
        self._next_id = 1

    def create(self, ticket_data: dict) -> dict:
        now = datetime.datetime.now()
        ticket = {
            "id": self._next_id,
            **ticket_data,
            "created_at": now,
            "updated_at": now
        }
        self._tickets.append(ticket)
        self._next_id += 1
        return ticket

    def get_all(self) -> list:
        return self._tickets

    def get_by_id(self, id: int) -> dict | None:
        for ticket in self._tickets:
            if ticket["id"] == id:
                return ticket
        return None

    def update(self, id: int, data: dict) -> dict | None:
        ticket = self.get_by_id(id)
        if ticket:
            ticket.update(data)
            ticket["updated_at"] = datetime.datetime.now()
            return ticket
        return None

    def delete(self, id: int) -> bool:
        ticket = self.get_by_id(id)
        if ticket:
            self._tickets.remove(ticket)
            return True
        return False
