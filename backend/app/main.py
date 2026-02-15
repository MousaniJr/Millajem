from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import init_db
from .api import programs, balances, calculator, alerts, promotions, recommendations, sources, auth, planner, data_export

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
app.include_router(planner.router, prefix="/api")
app.include_router(data_export.router, prefix="/api")


def _migrate_db():
    """Run lightweight migrations for existing databases"""
    from sqlalchemy import inspect, text
    from .database import engine
    inspector = inspect(engine)
    columns = [c['name'] for c in inspector.get_columns('loyalty_programs')]
    if 'is_enrolled' not in columns:
        with engine.connect() as conn:
            conn.execute(text('ALTER TABLE loyalty_programs ADD COLUMN is_enrolled BOOLEAN DEFAULT 0'))
            conn.commit()
        print("Migration: added is_enrolled column to loyalty_programs")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    _migrate_db()
    print("Database initialized")

    # Seed initial data if database is empty
    from .database import SessionLocal
    from .seed import run_seed
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

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
