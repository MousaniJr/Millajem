from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/balances", tags=["balances"])


@router.get("/", response_model=List[schemas.Balance])
def list_balances(db: Session = Depends(get_db)):
    """Listar todos los saldos"""
    return db.query(models.Balance).all()


@router.get("/{balance_id}", response_model=schemas.Balance)
def get_balance(balance_id: int, db: Session = Depends(get_db)):
    """Obtener un saldo específico"""
    balance = db.query(models.Balance).filter(models.Balance.id == balance_id).first()
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance


@router.post("/", response_model=schemas.Balance)
def create_balance(balance: schemas.BalanceCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo saldo"""
    # Verificar que el programa existe
    program = db.query(models.LoyaltyProgram).filter(models.LoyaltyProgram.id == balance.program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    db_balance = models.Balance(**balance.dict())
    db.add(db_balance)
    db.commit()
    db.refresh(db_balance)
    return db_balance


@router.put("/{balance_id}", response_model=schemas.Balance)
def update_balance(balance_id: int, balance: schemas.BalanceUpdate, db: Session = Depends(get_db)):
    """Actualizar un saldo existente"""
    db_balance = db.query(models.Balance).filter(models.Balance.id == balance_id).first()
    if not db_balance:
        raise HTTPException(status_code=404, detail="Balance not found")

    db_balance.points = balance.points
    db_balance.notes = balance.notes
    db_balance.last_updated = datetime.utcnow()

    db.commit()
    db.refresh(db_balance)
    return db_balance


@router.delete("/{balance_id}")
def delete_balance(balance_id: int, db: Session = Depends(get_db)):
    """Eliminar un saldo"""
    db_balance = db.query(models.Balance).filter(models.Balance.id == balance_id).first()
    if not db_balance:
        raise HTTPException(status_code=404, detail="Balance not found")

    db.delete(db_balance)
    db.commit()
    return {"message": "Balance deleted successfully"}
