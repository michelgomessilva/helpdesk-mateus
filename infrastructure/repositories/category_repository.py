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
        return {column.name: getattr(category, column.name) for column in category.__table__.columns}

    def get_all(self) -> list:
        categories = self.session.query(Category).all()
        return [{column.name: getattr(cat, column.name) for column in cat.__table__.columns} for cat in categories]

    def get_by_id(self, id: int) -> dict | None:
        category = self.session.query(Category).filter(Category.id == id).first()
        if category:
            return {column.name: getattr(category, column.name) for column in category.__table__.columns}
        return None

    def update(self, id: int, data: dict) -> dict | None:
        category = self.session.query(Category).filter(Category.id == id).first()
        if not category:
            return None
        for key, value in data.items():
            setattr(category, key, value)
        self.session.commit()
        self.session.refresh(category)
        return {column.name: getattr(category, column.name) for column in category.__table__.columns}

    def delete(self, id: int) -> bool:
        category = self.session.query(Category).filter(Category.id == id).first()
        if category:
            self.session.delete(category)
            self.session.commit()
            return True
        return False