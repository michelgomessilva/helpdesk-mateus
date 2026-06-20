from sqlalchemy.orm import Session

from infrastructure.models.ticket_models import Ticket


class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, ticket_data: dict) -> dict:
        ticket = Ticket(**ticket_data)
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "category_id": ticket.category_id,
            "user_id": ticket.user_id,
            "assigned_to": ticket.assigned_to,
            "resolution": ticket.resolution,
            "priority": ticket.priority,
            "status": ticket.status,
            "created_at": ticket.created_at,
            "updated_at": ticket.updated_at,
        }

    def get_all(self) -> list:
        tickets = self.session.query(Ticket).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "category_id": t.category_id,
                "user_id": t.user_id,
                "assigned_to": t.assigned_to,
                "resolution": t.resolution,
                "priority": t.priority,
                "status": t.status,
                "created_at": t.created_at,
                "updated_at": t.updated_at,
            }
            for t in tickets
        ]

    def get_by_id(self, id: int) -> dict | None:
        t = self.session.query(Ticket).filter(Ticket.id == id).first()
        if not t:
            return None
        return {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "category_id": t.category_id,
            "user_id": t.user_id,
            "assigned_to": t.assigned_to,
            "resolution": t.resolution,
            "priority": t.priority,
            "status": t.status,
            "created_at": t.created_at,
            "updated_at": t.updated_at,
        }

    def update(self, id: int, data: dict) -> dict | None:
        t = self.session.query(Ticket).filter(Ticket.id == id).first()
        if not t:
            return None

        for k, v in data.items():
            setattr(t, k, v)

        self.session.commit()
        self.session.refresh(t)
        return {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "category_id": t.category_id,
            "user_id": t.user_id,
            "assigned_to": t.assigned_to,
            "resolution": t.resolution,
            "priority": t.priority,
            "status": t.status,
            "created_at": t.created_at,
            "updated_at": t.updated_at,
        }

    def delete(self, id: int) -> bool:
        t = self.session.query(Ticket).filter(Ticket.id == id).first()
        if not t:
            return False
        self.session.delete(t)
        self.session.commit()
        return True

