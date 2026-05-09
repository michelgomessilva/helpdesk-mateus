from app.repositories.category_repository import CategoryRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.ticket_repository import TicketRepository

_category_repository: CategoryRepository | None = None
_comment_repository: CommentRepository | None = None
_ticket_repository: TicketRepository | None = None


def _seed_categories(repo: CategoryRepository) -> None:
    """Popula o repositório com categorias iniciais"""
    if not repo.get_all():
        repo.create({"name": "Infraestrutura", "description": "Problemas de hardware e rede"})
        repo.create({"name": "Software", "description": "Problemas com aplicativos e sistemas"})
        repo.create({"name": "Redes", "description": "Problemas de conectividade"})
        repo.create({"name": "Segurança", "description": "Questões de segurança"})
        repo.create({"name": "Outros", "description": "Outras questões"})


def get_category_repository() -> CategoryRepository:
    global _category_repository
    if _category_repository is None:
        _category_repository = CategoryRepository()
        _seed_categories(_category_repository)
    return _category_repository


def get_comment_repository() -> CommentRepository:
    global _comment_repository
    if _comment_repository is None:
        _comment_repository = CommentRepository()
    return _comment_repository


def get_ticket_repository() -> TicketRepository:
    global _ticket_repository
    if _ticket_repository is None:
        _ticket_repository = TicketRepository()
    return _ticket_repository