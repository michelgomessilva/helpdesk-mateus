from infrastructure.models.ticket_history_models import TicketHistory

class TicketHistoryRepository:
    def __init__(self, session):
        self.session = session

    def create(self, history_data: dict) -> dict:
        history = TicketHistory(**history_data)
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return {column.name: getattr(history, column.name) for column in history.__table__.columns}

    def get_by_ticket_id(self, ticket_id: int) -> list:
        history_list = self.session.query(TicketHistory).filter(TicketHistory.ticket_id == ticket_id).all()
        return [{column.name: getattr(h, column.name) for column in h.__table__.columns} for h in history_list]