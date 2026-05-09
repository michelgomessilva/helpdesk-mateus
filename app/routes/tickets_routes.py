from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.ticket_schemas import TicketCreate, TicketResponse, TicketUpdate
from app.services import TicketService, CategoryService
from app.repositories import TicketRepository, CategoryRepository
from app.core.dependencies import get_ticket_repository, get_category_repository

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: TicketCreate,
    ticket_repo: TicketRepository = Depends(get_ticket_repository),
    category_repo: CategoryRepository = Depends(get_category_repository)
):
    """Cria um novo ticket (valida se category_id existe)"""
    ticket_service = TicketService(repository=ticket_repo)
    category_service = CategoryService(repository=category_repo)
    
    # Validar se a categoria existe
    category = category_service.get_category_by_id(ticket.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {ticket.category_id} não encontrada"
        )
    
    return ticket_service.create_ticket(ticket.model_dump())


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