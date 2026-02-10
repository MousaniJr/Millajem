from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=List[schemas.Alert])
def list_alerts(
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
    favorites_only: bool = False,
    country: Optional[str] = None,
    alert_type: Optional[str] = None,
    source_type: Optional[str] = None,
    source_name: Optional[str] = None,
    related_program: Optional[str] = None,
    priority: Optional[str] = None,
    order_by: str = "date_desc",  # date_desc, date_asc, priority_desc
    db: Session = Depends(get_db)
):
    """Listar alertas con filtros avanzados"""
    query = db.query(models.Alert)

    # Filtros booleanos
    if unread_only:
        query = query.filter(models.Alert.is_read == False)

    if favorites_only:
        query = query.filter(models.Alert.is_favorite == True)

    # Filtros por campo
    if country:
        query = query.filter(models.Alert.country == country)

    if alert_type:
        query = query.filter(models.Alert.alert_type == alert_type)

    if source_type:
        query = query.filter(models.Alert.source_type == source_type)

    if source_name:
        query = query.filter(models.Alert.source_name == source_name)

    if related_program:
        query = query.filter(models.Alert.related_program == related_program)

    if priority:
        query = query.filter(models.Alert.priority == priority)

    # Ordenamiento
    if order_by == "date_asc":
        query = query.order_by(models.Alert.created_at.asc())
    elif order_by == "priority_desc":
        # Orden personalizado de prioridad
        priority_order = {"urgent": 1, "high": 2, "normal": 3, "low": 4}
        query = query.order_by(
            models.Alert.priority.case(priority_order, value=models.Alert.priority),
            models.Alert.created_at.desc()
        )
    else:  # date_desc por defecto
        query = query.order_by(models.Alert.created_at.desc())

    return query.offset(skip).limit(limit).all()


@router.get("/{alert_id}", response_model=schemas.Alert)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Obtener una alerta específica"""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/", response_model=schemas.Alert)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    """Crear una nueva alerta"""
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.patch("/{alert_id}/read")
def mark_as_read(alert_id: int, db: Session = Depends(get_db)):
    """Marcar alerta como leída"""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_read = True
    db.commit()
    return {"message": "Alert marked as read"}


@router.patch("/{alert_id}/favorite")
def toggle_favorite(alert_id: int, db: Session = Depends(get_db)):
    """Alternar favorito de una alerta"""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_favorite = not alert.is_favorite
    db.commit()
    return {"message": "Favorite toggled", "is_favorite": alert.is_favorite}


@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Eliminar una alerta"""
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted"}


@router.get("/stats/summary")
def get_alerts_summary(db: Session = Depends(get_db)):
    """Obtener resumen de alertas"""
    total = db.query(models.Alert).count()
    unread = db.query(models.Alert).filter(models.Alert.is_read == False).count()
    favorites = db.query(models.Alert).filter(models.Alert.is_favorite == True).count()

    # Por tipo
    by_type = {}
    types = db.query(models.Alert.alert_type).distinct().all()
    for (alert_type,) in types:
        count = db.query(models.Alert).filter(models.Alert.alert_type == alert_type).count()
        by_type[alert_type] = count

    return {
        "total": total,
        "unread": unread,
        "favorites": favorites,
        "by_type": by_type
    }
