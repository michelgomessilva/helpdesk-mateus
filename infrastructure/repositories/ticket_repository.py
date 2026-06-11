from sqlalchemy.orm import Session

from infrastructure.models.ticket_models import Ticket


class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _to_dict(ticket: Ticket) -> dict:
        return {column.name: getattr(ticket, column.name) for column in ticket.__table__.columns}

    def create(self, ticket_data: dict, commit: bool = True) -> dict:
        ticket = Ticket(**ticket_data)
        self.session.add(ticket)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        self.session.refresh(ticket)
        return self._to_dict(ticket)

    def get_all(self) -> list:
        tickets = self.session.query(Ticket).all()
        return [self._to_dict(t) for t in tickets]

    def get_by_id(self, id: int) -> dict | None:
        t = self.session.query(Ticket).filter(Ticket.id == id).first()
        if not t:
            return None
        return self._to_dict(t) if t else None

    def update(self, id: int, data: dict, commit: bool = True) -> dict | None:
        t = self.session.query(Ticket).filter(Ticket.id == id).first()
        if not t:
            return None

        for k, v in data.items():
            setattr(t, k, v)

        if commit:
            self.session.commit()
        else:
            self.session.flush()
        self.session.refresh(t)
        return self._to_dict(t)

    def delete(self, id: int) -> bool:
        t = self.session.query(Ticket).filter(Ticket.id == id).first()
        if not t:
            return False
        self.session.delete(t)
        self.session.commit()
        return True

    def _to_dict(self, obj):
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}