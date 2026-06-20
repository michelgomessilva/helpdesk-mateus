from infrastructure.repositories import CategoryRepository
from app.core.logging import logger

class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def create_category(self, category_data: dict) -> dict:
        logger.info(f"Criando categoria: {category_data.get('name')}")
        result = self.repository.create(category_data)
        logger.info(f"Categoria criada com ID {result.get('id')}")
        return result

    def get_all_categories(self) -> list:
        return self.repository.get_all()

    def get_category_by_id(self, id: int) -> dict | None:
        return self.repository.get_by_id(id)

    def update_category(self, id: int, data: dict) -> dict | None:
        logger.info(f"Atualizando categoria {id}")
        result = self.repository.update(id, data)
        if result:
            logger.info(f"Categoria {id} atualizada")
        else:
            logger.warning(f"Categoria {id} não encontrada para atualização")
        return result

    def delete_category(self, id: int) -> bool:
        logger.info(f"Deletando categoria {id}")
        result = self.repository.delete(id)
        if result:
            logger.info(f"Categoria {id} deletada")
        else:
            logger.warning(f"Categoria {id} não encontrada para deleção")
        return result
