from fastapi import FastAPI
from app.routes.health_route import router as health_router
from app.routes.categories_routes import router as categories_router
from app.routes.tickets_routes import router as tickets_router
from app.routes.comments_route import router as comments_router

app = FastAPI(
    title="HelpDesk Hub API",
    description="API para gestão de chamados de suporte interno",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(categories_router)
app.include_router(tickets_router)
app.include_router(comments_router)
