"""Importa todos os modelos para garantir que o SQLAlchemy/Alembic registre os mappers.

O projeto usa relationship("Ticket"), relationship("User"), etc. Para isso funcionar
sem errors de "failed to locate a name", todos os models precisam ser importados
antes que o SQLAlchemy configure os mappers.
"""

from infrastructure.models.user_models import User  # noqa: F401
from infrastructure.models.category_models import Category  # noqa: F401
from infrastructure.models.comment_models import Comment  # noqa: F401
from infrastructure.models.ticket_models import Ticket  # noqa: F401
from infrastructure.models.ticket_history_models import TicketHistory  # noqa: F401

