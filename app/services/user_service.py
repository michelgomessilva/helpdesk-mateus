from infrastructure.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from datetime import timedelta

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def register(self, user_data: dict) -> dict:
        """Registra um novo usuário."""
        # Verificar se username já existe
        existing = self.user_repo.get_by_username(user_data["username"])
        if existing:
            raise ValueError("Username já está em uso")
        
        # Verificar se email já existe
        existing = self.user_repo.get_by_email(user_data["email"])
        if existing:
            raise ValueError("Email já está em uso")
        
        # Hashear a senha
        hashed = hash_password(user_data["password"])
        # Criar dicionário para o repositório (sem a senha original)
        user_to_create = {
            "username": user_data["username"],
            "email": user_data["email"],
            "hashed_password": hashed,
            "role": user_data.get("role", "employee")
        }
        return self.user_repo.create(user_to_create)
    
    def authenticate(self, username: str, password: str) -> dict | None:
        """Verifica credenciais e retorna o usuário (sem token) se ok."""
        user = self.user_repo.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user
    
    def get_user_by_id(self, user_id: int) -> dict | None:
        return self.user_repo.get_by_id(user_id)