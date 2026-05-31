from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import init_db
from .auth import get_current_user
from .api import programs, balances, calculator, alerts, promotions, recommendations, sources, auth, planner, data_export

settings = get_settings()
cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

# Create FastAPI app
app = FastAPI(
    title="Millajem API",
    description="API para gestión de puntos, millas y Avios",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)  # Auth router (no prefix, already has /api/auth)
protected = [Depends(get_current_user)]
app.include_router(programs.router, prefix="/api", dependencies=protected)
app.include_router(balances.router, prefix="/api", dependencies=protected)
app.include_router(calculator.router, prefix="/api", dependencies=protected)
app.include_router(alerts.router, prefix="/api", dependencies=protected)
app.include_router(promotions.router, prefix="/api", dependencies=protected)
app.include_router(recommendations.router, prefix="/api", dependencies=protected)
app.include_router(sources.router, dependencies=protected)
app.include_router(planner.router, prefix="/api", dependencies=protected)
app.include_router(data_export.router, prefix="/api", dependencies=protected)


def _migrate_db():
    """Run lightweight migrations for existing databases"""
    from sqlalchemy import inspect, text
    from .database import engine
    inspector = inspect(engine)

    migrations = {
        "loyalty_programs": [
            ("is_enrolled", "ALTER TABLE loyalty_programs ADD COLUMN is_enrolled BOOLEAN DEFAULT 0"),
            ("ratio_confidence", "ALTER TABLE loyalty_programs ADD COLUMN ratio_confidence VARCHAR"),
            ("ratio_source_url", "ALTER TABLE loyalty_programs ADD COLUMN ratio_source_url VARCHAR"),
            ("ratio_last_verified_at", "ALTER TABLE loyalty_programs ADD COLUMN ratio_last_verified_at DATETIME"),
        ],
        "earning_opportunities": [
            ("source_url", "ALTER TABLE earning_opportunities ADD COLUMN source_url VARCHAR"),
            ("start_date", "ALTER TABLE earning_opportunities ADD COLUMN start_date DATETIME"),
            ("end_date", "ALTER TABLE earning_opportunities ADD COLUMN end_date DATETIME"),
            ("last_verified_at", "ALTER TABLE earning_opportunities ADD COLUMN last_verified_at DATETIME"),
            ("confidence", "ALTER TABLE earning_opportunities ADD COLUMN confidence VARCHAR"),
        ],
        "sources": [
            ("last_verified_at", "ALTER TABLE sources ADD COLUMN last_verified_at DATETIME"),
        ],
        "alerts": [
            ("confidence", "ALTER TABLE alerts ADD COLUMN confidence VARCHAR"),
            ("last_verified_at", "ALTER TABLE alerts ADD COLUMN last_verified_at DATETIME"),
            ("start_date", "ALTER TABLE alerts ADD COLUMN start_date DATETIME"),
            ("end_date", "ALTER TABLE alerts ADD COLUMN end_date DATETIME"),
            ("detected_bonus_percentage", "ALTER TABLE alerts ADD COLUMN detected_bonus_percentage FLOAT"),
        ],
    }

    with engine.connect() as conn:
        for table_name, table_migrations in migrations.items():
            existing_columns = {c["name"] for c in inspector.get_columns(table_name)}
            for column_name, ddl in table_migrations:
                if column_name not in existing_columns:
                    conn.execute(text(ddl))
                    print(f"Migration: added {column_name} column to {table_name}")
        conn.commit()


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
