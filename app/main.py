from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.core.logging import logger
from app.routes.health_route import router as health_router
from app.routes.categories_routes import router as categories_router
from app.routes.tickets_routes import router as tickets_router
from app.routes.comments_route import router as comments_router
from app.routes.users_routes import router as users_router


# ========== MIDDLEWARE DE LOGS DE REQUISIÇÃO ==========
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - Status {response.status_code} - {process_time:.3f}s"
        )
        return response


# ========== CRIAÇÃO DA APLICAÇÃO ==========
app = FastAPI(
    title="HelpDesk Hub API",
    description="API para gestão de chamados de suporte interno",
    version="1.0.0"
)

# Adiciona middleware de logs
app.add_middleware(LoggingMiddleware)


# ========== TRATADORES GLOBAIS DE EXCEÇÕES ==========
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Erro de validação: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(f"Erro de integridade: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Violação de integridade do banco de dados. Verifique os dados enviados."}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocorreu um erro interno. Tente novamente mais tarde."}
    )


# ========== ROTAS ==========
app.include_router(health_router)
app.include_router(categories_router)
app.include_router(tickets_router)
app.include_router(comments_router)
app.include_router(users_router)