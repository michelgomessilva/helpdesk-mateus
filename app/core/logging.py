import sys
from loguru import logger
from pathlib import Path

# Remove handlers padrão
logger.remove()

# Adiciona saída para terminal (colorida)
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

# Adiciona saída para arquivo (rotação diária)
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logger.add(
    LOG_DIR / "app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO"
)

# Exporta o logger para ser usado em outros módulos
__all__ = ["logger"]