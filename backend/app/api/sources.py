"""
API endpoints para gestión de fuentes de información
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Source
from app import schemas

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("/", response_model=List[schemas.Source])
def list_sources(
    source_type: Optional[str] = None,
    country: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Listar todas las fuentes con filtros opcionales

    Filtros:
    - source_type: rss_feed, instagram, twitter, telegram
    - country: ES, BR, GI, INT
    - is_active: true/false
    """
    query = db.query(Source)

    if source_type:
        query = query.filter(Source.source_type == source_type)

    if country:
        query = query.filter(Source.country == country)

    if is_active is not None:
        query = query.filter(Source.is_active == is_active)

    # Ordenar por prioridad (mayor primero) y luego por nombre
    query = query.order_by(Source.priority.desc(), Source.name)

    return query.offset(skip).limit(limit).all()


@router.get("/{source_id}", response_model=schemas.Source)
def get_source(source_id: int, db: Session = Depends(get_db)):
    """Obtener una fuente específica por ID"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post("/", response_model=schemas.Source)
def create_source(source: schemas.SourceCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva fuente

    Tipos disponibles:
    - rss_feed: Feed RSS de blog
    - instagram: Cuenta de Instagram
    - twitter: Cuenta de Twitter/X
    - telegram: Canal de Telegram

    Países:
    - ES: España
    - BR: Brasil
    - GI: Gibraltar/UK
    - INT: Internacional
    """
    # Verificar que no exista ya una fuente con esa URL
    existing = db.query(Source).filter(Source.url == source.url).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Source with URL {source.url} already exists"
        )

    db_source = Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


@router.put("/{source_id}", response_model=schemas.Source)
def update_source(
    source_id: int,
    source_update: schemas.SourceUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una fuente existente"""
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")

    # Actualizar solo los campos proporcionados
    update_data = source_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_source, field, value)

    db_source.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_source)
    return db_source


@router.delete("/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db)):
    """Eliminar una fuente"""
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")

    db.delete(db_source)
    db.commit()
    return {"message": f"Source {db_source.name} deleted successfully"}


@router.post("/{source_id}/toggle")
def toggle_source(source_id: int, db: Session = Depends(get_db)):
    """Activar/desactivar una fuente"""
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")

    db_source.is_active = not db_source.is_active
    db_source.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_source)

    status = "activated" if db_source.is_active else "deactivated"
    return {
        "message": f"Source {db_source.name} {status}",
        "is_active": db_source.is_active
    }


@router.get("/stats/summary")
def get_sources_stats(db: Session = Depends(get_db)):
    """Obtener estadísticas de fuentes"""
    total = db.query(Source).count()
    active = db.query(Source).filter(Source.is_active == True).count()
    inactive = total - active

    by_type = {}
    for source_type in ["rss_feed", "instagram", "twitter", "telegram"]:
        count = db.query(Source).filter(Source.source_type == source_type).count()
        by_type[source_type] = count

    by_country = {}
    for country in ["ES", "BR", "GI", "INT"]:
        count = db.query(Source).filter(Source.country == country).count()
        by_country[country] = count

    return {
        "total": total,
        "active": active,
        "inactive": inactive,
        "by_type": by_type,
        "by_country": by_country
    }
