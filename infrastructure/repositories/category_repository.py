from pydantic import BaseModel


from infrastructure.models.category_models import Category

class CategoryRepository:   # sem BaseModel
    def __init__(self, session):
        self.session = session

    def create(self, category_data: dict) -> dict:
        category = Category(**category_data)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return self._to_dict(category)

    def get_all(self) -> list:
        categories = self.session.query(Category).all()
        return [self._to_dict(c) for c in categories]

    def get_by_id(self, id: int) -> dict | None:
        category = self.session.query(Category).filter(Category.id == id).first()
        return self._to_dict(category) if category else None

    def update(self, id: int, data: dict) -> dict | None:
        category = self.session.query(Category).filter(Category.id == id).first()
        if not category:
            return None
        for key, value in data.items():
            setattr(category, key, value)
        self.session.commit()
        self.session.refresh(category)
        return self._to_dict(category)

    def delete(self, id: int) -> bool:
        category = self.session.query(Category).filter(Category.id == id).first()
        if category:
            self.session.delete(category)
            self.session.commit()
            return True
        return False
    
    def _to_dict(self, obj):
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}