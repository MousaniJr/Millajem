from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from ..database import get_db
from .. import models

router = APIRouter(prefix="/data", tags=["data"])

# --- Name aliases for renamed programs (old name -> new name) ---
PROGRAM_NAME_ALIASES: Dict[str, str] = {
    # Cepsa → Moeve rebrand (2025)
    "Cepsa Más": "Moeve (ex-Cepsa) Más",
    "Cepsa GOW": "Club Moeve gow",
}


class BalanceExport(BaseModel):
    program_name: str
    points: int
    notes: Optional[str] = None


class SourceExport(BaseModel):
    name: str
    source_type: str
    country: str
    url: str
    website_url: Optional[str] = None
    is_active: bool
    priority: int
    description: Optional[str] = None
    notes: Optional[str] = None


class DataExport(BaseModel):
    version: int = 2
    exported_at: str
    balances: List[BalanceExport]
    enrolled_programs: List[str]
    # v2: sources customization
    sources: Optional[List[SourceExport]] = None
    deactivated_sources: Optional[List[str]] = None  # URLs of sources user deactivated


class ImportResult(BaseModel):
    balances_imported: int
    balances_skipped: int
    programs_enrolled: int
    programs_not_found: List[str]
    sources_added: int
    sources_toggled: int


@router.get("/export", response_model=DataExport)
def export_data(db: Session = Depends(get_db)):
    """Export user data (balances + enrolled programs + source customizations) as JSON"""
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

    # Export custom sources (user-added, not from seed)
    # We export ALL sources so we can restore active/inactive state
    all_sources = db.query(models.Source).all()
    source_exports = []
    deactivated_urls = []
    for s in all_sources:
        source_exports.append(SourceExport(
            name=s.name,
            source_type=s.source_type,
            country=s.country,
            url=s.url,
            website_url=s.website_url,
            is_active=s.is_active,
            priority=s.priority,
            description=s.description,
            notes=s.notes,
        ))
        if not s.is_active:
            deactivated_urls.append(s.url)

    return DataExport(
        exported_at=datetime.utcnow().isoformat(),
        balances=balance_exports,
        enrolled_programs=enrolled,
        sources=source_exports,
        deactivated_sources=deactivated_urls,
    )


def _resolve_program_name(name: str, name_to_program: dict) -> Optional[object]:
    """Find a program by name, checking aliases for renamed programs."""
    program = name_to_program.get(name)
    if program:
        return program
    # Check if the name is an old alias
    new_name = PROGRAM_NAME_ALIASES.get(name)
    if new_name:
        return name_to_program.get(new_name)
    return None


@router.post("/import", response_model=ImportResult)
def import_data(data: DataExport, db: Session = Depends(get_db)):
    """Import user data (balances + enrolled programs + source customizations) from JSON"""
    # Build name -> program lookup
    all_programs = db.query(models.LoyaltyProgram).all()
    name_to_program = {p.name: p for p in all_programs}

    balances_imported = 0
    balances_skipped = 0
    programs_not_found = []

    # Import balances
    for b in data.balances:
        program = _resolve_program_name(b.program_name, name_to_program)
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
        program = _resolve_program_name(name, name_to_program)
        if program:
            program.is_enrolled = True
            programs_enrolled += 1
        else:
            if name not in programs_not_found:
                programs_not_found.append(name)

    # Import source customizations
    sources_added = 0
    sources_toggled = 0

    if data.sources:
        existing_urls = {s.url for s in db.query(models.Source).all()}
        for src in data.sources:
            if src.url not in existing_urls:
                # User-added source that doesn't exist in seed — re-add it
                db.add(models.Source(
                    name=src.name,
                    source_type=src.source_type,
                    country=src.country,
                    url=src.url,
                    website_url=src.website_url,
                    is_active=src.is_active,
                    priority=src.priority,
                    description=src.description,
                    notes=src.notes,
                ))
                sources_added += 1

    # Restore deactivated sources
    if data.deactivated_sources:
        for url in data.deactivated_sources:
            source = db.query(models.Source).filter_by(url=url).first()
            if source and source.is_active:
                source.is_active = False
                sources_toggled += 1

    db.commit()

    return ImportResult(
        balances_imported=balances_imported,
        balances_skipped=balances_skipped,
        programs_enrolled=programs_enrolled,
        programs_not_found=programs_not_found,
        sources_added=sources_added,
        sources_toggled=sources_toggled,
    )
