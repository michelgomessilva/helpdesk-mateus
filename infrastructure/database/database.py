import os
from dotenv import load_dotenv, find_dotenv

# Carrega as variáveis do arquivo .env antes de qualquer uso
load_dotenv(find_dotenv())

# Agora pode ler a variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Check your .env file.")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cria o motor (engine) de conexão
engine = create_engine(DATABASE_URL)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a classe base para os models
Base = declarative_base()

# Dependência para obter a sessão do banco (será usada nas rotas)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()