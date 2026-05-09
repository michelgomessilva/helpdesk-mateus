from fastapi import APIRouter, HTTPException, Depends, status
from app.services.comment_service import CommentService
from app.repositories import CommentRepository, TicketRepository
from app.core.dependencies import get_comment_repository, get_ticket_repository
from app.schemas.comment_schemas import CommentCreate, CommentResponse

router = APIRouter(prefix="/tickets/{ticket_id}/comments", tags=["comments"])


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    ticket_id: int,
    comment_data: CommentCreate,
    comment_repo: CommentRepository = Depends(get_comment_repository),
    ticket_repo: TicketRepository = Depends(get_ticket_repository)
):
    """Cria um novo comentário para um ticket"""
    service = CommentService(comment_repository=comment_repo, ticket_repository=ticket_repo)
    
    try:
        comment = service.create_comment(ticket_id, comment_data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return CommentResponse(**comment)

