import os

try:
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
except ImportError as e:
    raise ImportError("SQLAlchemy is required. Install it with: pip install sqlalchemy") from e

# Pega a string de conexão do ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

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