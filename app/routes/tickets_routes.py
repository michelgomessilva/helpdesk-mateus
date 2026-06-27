from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session


from app.core.dependencies import get_category_repository, get_ticket_repository
from app.core.security import get_current_user
from app.services import CategoryService, TicketService


from app.schemas.ticket_history_schemas import TicketHistoryResponse
from app.schemas.ticket_schemas import (
    TicketAssign,
    TicketCreate,
    TicketResponse,
    TicketStatusUpdate,
    TicketUpdate,
)
from infrastructure.database.database import get_db

from infrastructure.repositories import CategoryRepository, TicketRepository
from infrastructure.repositories.ticket_history_repository import TicketHistoryRepository

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # <-- Adicione esta linha
):
    ticket_repo = TicketRepository(db)
    category_repo = CategoryRepository(db)
    ticket_service = TicketService(ticket_repo)
    category_service = CategoryService(category_repo)
    
    # Validar se a categoria existe
    category = category_service.get_category_by_id(ticket.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {ticket.category_id} não encontrada"
        )
    
    # Converter os dados para dicionário e adicionar o user_id do usuário autenticado
    ticket_data = ticket.model_dump()
    ticket_data["user_id"] = current_user["id"]   # <-- Adicione esta linha
    
    return ticket_service.create_ticket(ticket_data)

@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    ticket_repo: TicketRepository = Depends(get_ticket_repository),
    status: str = None,
    priority: str = None,
    category_id: int = None,
    skip: int = 0,
    limit: int = 100
):
    """Lista tickets com filtros e paginação"""
    service = TicketService(repository=ticket_repo)

    # Criar dicionário de filtros (apenas os não-None)
    filters = {}
    if status is not None:
        filters["status"] = status
    if priority is not None:
        filters["priority"] = priority
    if category_id is not None:
        filters["category_id"] = category_id

    return service.list_tickets(filters, skip, limit)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, ticket_repo: TicketRepository = Depends(get_ticket_repository)):
    """Obtém um ticket pelo ID"""
    service = TicketService(repository=ticket_repo)
    ticket = service.get_ticket_by_id(ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket com ID {ticket_id} não encontrado"
        )
    return ticket

@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    ticket_repo: TicketRepository = Depends(get_ticket_repository)
):
    """Atualiza um ticket (parcial)"""
    service = TicketService(repository=ticket_repo)
    
    # Filtrar apenas campos que foram enviados (não None)
    update_data = ticket.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum dado fornecido para atualização"
        )
    
    updated = service.update_ticket(ticket_id, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket com ID {ticket_id} não encontrado"
        )
    return updated

@router.patch("/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(
    ticket_id: int,
    assign_data: TicketAssign,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["agent", "admin"]:
        raise HTTPException(status_code=403, detail="Permissão negada")
    
    ticket_repo = TicketRepository(db)
    service = TicketService(ticket_repo)
    
    updated = service.assign_ticket(ticket_id, assign_data.assigned_to, current_user["id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    return updated


@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int,
    status_data: TicketStatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["agent", "admin"]:
        raise HTTPException(status_code=403, detail="Permissão negada")
    
    ticket_repo = TicketRepository(db)
    service = TicketService(ticket_repo)
    update_data = status_data.dict(exclude_unset=True)
    
    try:
        updated = service.update_ticket(ticket_id, update_data, current_user["id"])
        if not updated:
            raise HTTPException(status_code=404, detail="Ticket não encontrado")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{ticket_id}/history", response_model=list[TicketHistoryResponse])
def get_ticket_history(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Qualquer usuário logado pode ver o histórico? Ajuste conforme regra
    history_repo = TicketHistoryRepository(db)
    history = history_repo.get_by_ticket_id(ticket_id)
    return history