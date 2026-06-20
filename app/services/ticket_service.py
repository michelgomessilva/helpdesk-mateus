from infrastructure.repositories import TicketRepository
from infrastructure.repositories.ticket_history_repository import TicketHistoryRepository

class TicketService:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def create_ticket(self, ticket_data: dict) -> dict:
        return self.repository.create(ticket_data)

    def get_all_tickets(self) -> list:
        return self.repository.get_all()

    def get_ticket_by_id(self, id: int) -> dict | None:
        return self.repository.get_by_id(id)

    def delete_ticket(self, id: int) -> bool:
        return self.repository.delete(id)

    def list_tickets(self, filters: dict, skip: int = 0, limit: int = 100) -> list:
        tickets = self.repository.get_all()
        if filters.get("status"):
            tickets = [t for t in tickets if t.get("status") == filters["status"]]
        if filters.get("priority"):
            tickets = [t for t in tickets if t.get("priority") == filters["priority"]]
        if filters.get("category_id"):
            tickets = [t for t in tickets if t.get("category_id") == filters["category_id"]]
        return tickets[skip:skip + limit]

    # ========== REGRAS DE TRANSIÇÃO ==========
    def _can_transition(self, current_status: str, new_status: str) -> bool:
        allowed = {
            "aberto": ["em_andamento"],
            "em_andamento": ["fechado"],
            "fechado": ["aberto"]  # opcional
        }
        return new_status in allowed.get(current_status, [])

    # ========== REGISTRO DE HISTÓRICO ==========
    def _add_history(self, ticket_id: int, user_id: int, field_name: str, old_value, new_value):
        # Obtém a sessão do repositório (garantindo que existe)
        session = self.repository.session
        history_repo = TicketHistoryRepository(session)
        history_repo.create({
            "ticket_id": ticket_id,
            "user_id": user_id,
            "field_name": field_name,
            "old_value": str(old_value) if old_value else None,
            "new_value": str(new_value) if new_value else None
        })

    # ========== ATRIBUIR TICKET ==========
    def assign_ticket(self, ticket_id: int, assigned_to: int, user_id: int) -> dict | None:
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            return None
        old_assigned = ticket.get("assigned_to")
        if old_assigned == assigned_to:
            return ticket
        updated = self.repository.update(ticket_id, {"assigned_to": assigned_to})
        if updated and user_id:
            self._add_history(ticket_id, user_id, "assigned_to", old_assigned, assigned_to)
        return updated

    # ========== ATUALIZAR TICKET (COM VALIDAÇÃO DE STATUS) ==========
    def update_ticket(self, ticket_id: int, data: dict, user_id: int = None) -> dict | None:
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            return None

        if "status" in data:
            new_status = data["status"]
            old_status = ticket.get("status")
            if not self._can_transition(old_status, new_status):
                raise ValueError(f"Transição inválida: {old_status} -> {new_status}")
            if new_status == "fechado" and not data.get("resolution"):
                raise ValueError("Para fechar o ticket, é necessário fornecer uma resolução")
            if new_status == "aberto":
                data["resolution"] = None
            if user_id:
                self._add_history(ticket_id, user_id, "status", old_status, new_status)

        updated = self.repository.update(ticket_id, data)
        return updated