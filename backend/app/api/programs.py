from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get("/", response_model=List[schemas.LoyaltyProgram])
def list_programs(db: Session = Depends(get_db)):
    """Listar todos los programas de fidelidad"""
    return db.query(models.LoyaltyProgram).all()


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
