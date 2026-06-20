from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Carrega as variáveis do .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

# Importa a Base e todos os models
from infrastructure.database.database import Base
import infrastructure.models.user_models
import infrastructure.models.category_models
import infrastructure.models.ticket_models
import infrastructure.models.comment_models
import infrastructure.models.ticket_history_models


# Configuração do Alembic (apenas para logging)
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = os.getenv("DATABASE_URL")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    url = os.getenv("DATABASE_URL")
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()