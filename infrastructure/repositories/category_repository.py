from pydantic import BaseModel


class CategoryRepository(BaseModel):
    def __init__(self):
        self._categories = []
        self._next_id = 1

    def create(self, category_data: dict) -> dict:
        category = {"id": self._next_id, **category_data}
        self._categories.append(category)
        self._next_id += 1
        return category

    def get_all(self) -> list:
        return self._categories

    def get_by_id(self, id: int) -> dict | None:
        for category in self._categories:
            if category["id"] == id:
                return category
        return None

    def update(self, id: int, data: dict) -> dict | None:
        category = self.get_by_id(id)
        if category:
            category.update(data)
            return category
        return None

    def delete(self, id: int) -> bool:
        category = self.get_by_id(id)
        if category:
            self._categories.remove(category)
            return True
        return False