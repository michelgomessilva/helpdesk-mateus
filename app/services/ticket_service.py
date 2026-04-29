from pydantic import BaseModel

from app.repositories import TicketRepository


class TicketService(BaseModel):
    repository: TicketRepository  # Injeção de dependência

    def create_ticket(self, ticket_data: dict) -> dict:
        return self.repository.create(ticket_data)

    def get_all_tickets(self) -> list:
        return self.repository.get_all()

    def get_ticket_by_id(self, id: int) -> dict | None:
        return self.repository.get_by_id(id)

    def update_ticket(self, id: int, data: dict) -> dict | None:
        return self.repository.update(id, data)

    def delete_ticket(self, id: int) -> bool:
        return self.repository.delete(id)

    def list_tickets(self, filters: dict, skip: int = 0, limit: int = 100) -> list:
        """Lista tickets com filtros, paginação (skip) e limite (limit)"""
        tickets = self.repository.get_all()

        # Aplicar filtros
        if "status" in filters and filters["status"]:
            tickets = [t for t in tickets if t.get("status") == filters["status"]]
        if "priority" in filters and filters["priority"]:
            tickets = [t for t in tickets if t.get("priority") == filters["priority"]]
        if "category_id" in filters and filters["category_id"]:
            tickets = [t for t in tickets if t.get("category_id") == filters["category_id"]]

        # Aplicar paginação
        return tickets[skip:skip + limit]