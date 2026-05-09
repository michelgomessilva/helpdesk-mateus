from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.category_schemas import CategoryCreate, CategoryResponse
from app.services import CategoryService
from app.repositories import CategoryRepository
from app.core.dependencies import get_category_repository

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    category_repo: CategoryRepository = Depends(get_category_repository)
):
    """Cria uma nova categoria"""
    service = CategoryService(repository=category_repo)
    return service.create_category(category.model_dump())


@router.get("/", response_model=list[CategoryResponse])
def list_categories(category_repo: CategoryRepository = Depends(get_category_repository)):
    """Lista todas as categorias"""
    service = CategoryService(repository=category_repo)
    return service.get_all_categories()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    category_repo: CategoryRepository = Depends(get_category_repository)
):
    """Obtém uma categoria pelo ID"""
    service = CategoryService(repository=category_repo)
    category = service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {category_id} não encontrada"
        )
    return category


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryCreate,
    category_repo: CategoryRepository = Depends(get_category_repository)
):
    """Atualiza uma categoria"""
    service = CategoryService(repository=category_repo)
    updated = service.update_category(category_id, category.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {category_id} não encontrada"
        )
    return updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    category_repo: CategoryRepository = Depends(get_category_repository)
):
    """Elimina uma categoria"""

    service = CategoryService(repository=category_repo)
    deleted = service.delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {category_id} não encontrada"
        )