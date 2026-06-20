from infrastructure.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from datetime import timedelta
from app.core.logging import logger

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def register(self, user_data: dict) -> dict:
        logger.info(f"Tentando registrar usuário: {user_data.get('username')}")
        
        existing = self.user_repo.get_by_username(user_data["username"])
        if existing:
            logger.warning(f"Tentativa de registro com username já existente: {user_data['username']}")
            raise ValueError("Username já está em uso")
        
        existing = self.user_repo.get_by_email(user_data["email"])
        if existing:
            logger.warning(f"Tentativa de registro com email já existente: {user_data['email']}")
            raise ValueError("Email já está em uso")
        
        hashed = hash_password(user_data["password"])
        user_to_create = {
            "username": user_data["username"],
            "email": user_data["email"],
            "hashed_password": hashed,
            "role": user_data.get("role", "employee")
        }
        result = self.user_repo.create(user_to_create)
        logger.info(f"Usuário registrado com sucesso: {result.get('username')} (ID {result.get('id')})")
        return result
    
    def get_user_by_id(self, user_id: int) -> dict | None:
        return self.user_repo.get_by_id(user_id)

    def authenticate(self, username: str, password: str) -> dict | None:
        logger.info(f"Tentativa de login para usuário: {username}")
        user = self.user_repo.get_by_username(username)
        if not user:
            logger.warning(f"Usuário não encontrado: {username}")
            return None
        if not verify_password(password, user["hashed_password"]):
            logger.warning(f"Senha incorreta para usuário: {username}")
            return None
        logger.info(f"Usuário autenticado com sucesso: {username} (ID {user['id']})")
        return user