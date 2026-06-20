from infrastructure.repositories.comment_repository import CommentRepository
from infrastructure.repositories.ticket_repository import TicketRepository
from app.core.logging import logger

class CommentService():
    def __init__(self, comment_repository: CommentRepository, ticket_repository: TicketRepository):
        self.comment_repository = comment_repository
        self.ticket_repository = ticket_repository

    def create_comment(self, ticket_id: int, comment_data: dict) -> dict:
        logger.info(f"Tentando adicionar comentário ao ticket {ticket_id}")

        # Verifica se o ticket existe (se você tiver essa validação)
        ticket = self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            logger.warning(f"Tentativa de comentar em ticket inexistente: {ticket_id}")
            raise ValueError("Ticket não encontrado")

        # Adiciona o ticket_id ao comment_data
        comment_data["ticket_id"] = ticket_id
        result = self.comment_repository.create(comment_data)

        logger.info(f"Comentário criado com ID {result.get('id')} no ticket {ticket_id}")
        return result

    


