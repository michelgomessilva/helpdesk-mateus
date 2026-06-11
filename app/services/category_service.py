from infrastructure.repositories import CategoryRepository


class CategoryService:
    def __init__(self, repository):
        self.repository = repository

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
