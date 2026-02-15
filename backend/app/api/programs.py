from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get("/", response_model=List[schemas.LoyaltyProgram])
def list_programs(enrolled: Optional[bool] = Query(None), db: Session = Depends(get_db)):
    """Listar todos los programas de fidelidad, opcionalmente filtrar por inscripción"""
    query = db.query(models.LoyaltyProgram)
    if enrolled is not None:
        query = query.filter(models.LoyaltyProgram.is_enrolled == enrolled)
    return query.all()


@router.get("/{program_id}", response_model=schemas.LoyaltyProgram)
def get_program(program_id: int, db: Session = Depends(get_db)):
    """Obtener un programa específico"""
    program = db.query(models.LoyaltyProgram).filter(models.LoyaltyProgram.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program


@router.post("/", response_model=schemas.LoyaltyProgram)
def create_program(program: schemas.LoyaltyProgramCreate, db: Session = Depends(get_db)):
    """Crear un nuevo programa de fidelidad"""
    db_program = models.LoyaltyProgram(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


@router.patch("/{program_id}/toggle-enrollment", response_model=schemas.LoyaltyProgram)
def toggle_enrollment(program_id: int, db: Session = Depends(get_db)):
    """Activar/desactivar inscripción en un programa"""
    program = db.query(models.LoyaltyProgram).filter(models.LoyaltyProgram.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    program.is_enrolled = not program.is_enrolled
    db.commit()
    db.refresh(program)
    return program
