from fastapi import APIRouter

from app.schemas.health_schemas import HealthCheckResponse
import time

router = APIRouter()

@router.get("/")
def check():
    return {"HelpDesk Hub API"}

@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    start_time = time.time()
    uptime = time.time() - start_time
    return HealthCheckResponse(
        status="OK",
        version="1.0.0",
        message="API funcionando",
        uptime=uptime
    )   