from infrastructure.models.comment_models import Comment

class CommentRepository:
    def __init__(self, session):
        self.session = session

    def create(self, comment_data: dict) -> dict:
        comment = Comment(**comment_data)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return self._to_dict(comment)
    
    def _to_dict(self, obj):
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}