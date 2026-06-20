import pytest
from app.services.ticket_service import TicketService
from infrastructure.repositories.ticket_repository import TicketRepository
from infrastructure.repositories.category_repository import CategoryRepository

def test_can_transition():
    service = TicketService(None)  # só para testar método interno
    assert service._can_transition("aberto", "em_andamento") == True
    assert service._can_transition("aberto", "fechado") == False
    assert service._can_transition("em_andamento", "fechado") == True