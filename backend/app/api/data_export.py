from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from .. import models

router = APIRouter(prefix="/data", tags=["data"])


class BalanceExport(BaseModel):
    program_name: str
    points: int
    notes: Optional[str] = None


class DataExport(BaseModel):
    version: int = 1
    exported_at: str
    balances: List[BalanceExport]
    enrolled_programs: List[str]


class ImportResult(BaseModel):
    balances_imported: int
    balances_skipped: int
    programs_enrolled: int
    programs_not_found: List[str]


@router.get("/export", response_model=DataExport)
def export_data(db: Session = Depends(get_db)):
    """Export user data (balances + enrolled programs) as JSON"""
    # Get balances with program names
    balances = db.query(models.Balance).all()
    programs = {p.id: p for p in db.query(models.LoyaltyProgram).all()}

    balance_exports = []
    for b in balances:
        program = programs.get(b.program_id)
        if program:
            balance_exports.append(BalanceExport(
                program_name=program.name,
                points=b.points,
                notes=b.notes,
            ))

    # Get enrolled program names
    enrolled = [
        p.name for p in db.query(models.LoyaltyProgram).filter(
            models.LoyaltyProgram.is_enrolled == True
        ).all()
    ]

    return DataExport(
        exported_at=datetime.utcnow().isoformat(),
        balances=balance_exports,
        enrolled_programs=enrolled,
    )


@router.post("/import", response_model=ImportResult)
def import_data(data: DataExport, db: Session = Depends(get_db)):
    """Import user data (balances + enrolled programs) from JSON"""
    # Build name -> program lookup
    all_programs = db.query(models.LoyaltyProgram).all()
    name_to_program = {p.name: p for p in all_programs}

    balances_imported = 0
    balances_skipped = 0
    programs_not_found = []

    # Import balances
    for b in data.balances:
        program = name_to_program.get(b.program_name)
        if not program:
            balances_skipped += 1
            if b.program_name not in programs_not_found:
                programs_not_found.append(b.program_name)
            continue

        # Check if balance exists for this program
        existing = db.query(models.Balance).filter(
            models.Balance.program_id == program.id
        ).first()

        if existing:
            existing.points = b.points
            existing.notes = b.notes
        else:
            db.add(models.Balance(
                program_id=program.id,
                points=b.points,
                notes=b.notes,
            ))
        balances_imported += 1

    # Import enrollment status
    # First reset all to not enrolled
    for p in all_programs:
        p.is_enrolled = False

    programs_enrolled = 0
    for name in data.enrolled_programs:
        program = name_to_program.get(name)
        if program:
            program.is_enrolled = True
            programs_enrolled += 1
        else:
            if name not in programs_not_found:
                programs_not_found.append(name)

    db.commit()

    return ImportResult(
        balances_imported=balances_imported,
        balances_skipped=balances_skipped,
        programs_enrolled=programs_enrolled,
        programs_not_found=programs_not_found,
    )
