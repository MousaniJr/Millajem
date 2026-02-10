from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import init_db
from .api import programs, balances, calculator, alerts, promotions, recommendations, sources, auth

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Millajem API",
    description="API para gestión de puntos, millas y Avios",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)  # Auth router (no prefix, already has /api/auth)
app.include_router(programs.router, prefix="/api")
app.include_router(balances.router, prefix="/api")
app.include_router(calculator.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(promotions.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(sources.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized")

    # Iniciar scheduler para tareas automáticas
    from .scheduler import start_scheduler
    start_scheduler()
    print("Scheduler started - Promotions will be scanned every 2 hours")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "Millajem API",
        "version": "0.1.0",
        "status": "running"
    }


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    from .scheduler import stop_scheduler
    stop_scheduler()
    print("Scheduler stopped")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from .scheduler import scheduler
    return {
        "status": "healthy",
        "environment": settings.environment,
        "scheduler_running": scheduler.running if scheduler else False
    }
