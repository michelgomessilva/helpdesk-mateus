from pydantic import BaseModel

from app.repositories import CategoryRepository


class CategoryService(BaseModel):
    repository: CategoryRepository  # Injeção de dependência

    def create_category(self, category_data: dict) -> dict:
        return self.repository.create(category_data)

    def get_all_categories(self) -> list:
        return self.repository.get_all()

    def get_category_by_id(self, id: int) -> dict | None:
        return self.repository.get_by_id(id)

    def update_category(self, id: int, data: dict) -> dict | None:
        return self.repository.update(id, data)

    def delete_category(self, id: int) -> bool:
        return self.repository.delete(id) 
