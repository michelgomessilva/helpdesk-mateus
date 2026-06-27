import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto (um nível acima de tests) ao sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from infrastructure.database.database import Base, get_db

# 1. Banco de dados de teste (SQLite em memória é rápido e isolado)
TEST_DATABASE_URL = "sqlite:///./test.db"  # ou use ":memory:" para RAM

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Substitui a dependência get_db do FastAPI pela nossa sessão de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Fixture que fornece um cliente HTTP para testar a API
@pytest.fixture(scope="module")
def client():
    # Cria as tabelas no banco de teste antes de todos os testes do módulo
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Após todos os testes, remove as tabelas
    Base.metadata.drop_all(bind=engine)

# 4. Fixture que fornece uma sessão de banco de dados isolada (útil para testes unitários de repositórios)
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()