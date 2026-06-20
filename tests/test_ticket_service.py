import pytest
from app.services.ticket_service import TicketService
from infrastructure.repositories.ticket_repository import TicketRepository
from infrastructure.repositories.category_repository import CategoryRepository

def test_can_transition():
    service = TicketService(None)  # só para testar método interno
    assert service._can_transition("aberto", "em_andamento") == True
    assert service._can_transition("aberto", "fechado") == False
    assert service._can_transition("em_andamento", "fechado") == True

def test_can_transition_additional():
    service = TicketService(None)
    # Reabertura (fechado → aberto)
    assert service._can_transition("fechado", "aberto")
    # Status inválido
    assert not service._can_transition("aberto", "invalido")
    assert not service._can_transition("qualquer", "outro")
    # Transição de fechado para em_andamento (não permitida)
    assert not service._can_transition("fechado", "em_andamento")