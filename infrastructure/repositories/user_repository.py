from infrastructure.models.user_models import User

class UserRepository:
    def __init__(self, session):
        self.session = session
    
    def create(self, user_data: dict) -> dict:
        """Cria um novo usuário no banco e retorna um dicionário."""
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        # Converte o objeto para dicionário
        return {column.name: getattr(user, column.name) for column in user.__table__.columns}
    
    def get_by_username(self, username: str) -> dict | None:
        """Busca um usuário pelo nome de usuário."""
        user = self.session.query(User).filter(User.username == username).first()
        if user:
            return {column.name: getattr(user, column.name) for column in user.__table__.columns}
        return None
    
    def get_by_email(self, email: str) -> dict | None:
        """Busca um usuário pelo email."""
        user = self.session.query(User).filter(User.email == email).first()
        if user:
            return {column.name: getattr(user, column.name) for column in user.__table__.columns}
        return None
    
    def get_by_id(self, user_id: int) -> dict | None:
        """Busca um usuário pelo ID."""
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            user_dict = {column.name: getattr(user, column.name) for column in user.__table__.columns}
            user_dict.pop("hashed_password", None)
            return user_dict
        return None