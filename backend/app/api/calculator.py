from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Optional
from ..database import get_db
from ..services.calculator import PointsCalculator

router = APIRouter(prefix="/calculator", tags=["calculator"])


class ConvertToAviosRequest(BaseModel):
    program_id: int
    points: float


class ConvertBetweenProgramsRequest(BaseModel):
    source_program_id: int
    target_program_id: int
    points: float
    bonus_percentage: float = 0.0


class CompareValueRequest(BaseModel):
    points_dict: Dict[int, float]  # {program_id: points}


@router.post("/to-avios")
def convert_to_avios(request: ConvertToAviosRequest, db: Session = Depends(get_db)):
    """Convertir puntos de un programa a Avios"""
    calculator = PointsCalculator(db)
    result = calculator.convert_to_avios(request.program_id, request.points)

    if result is None:
        raise HTTPException(status_code=404, detail="Program not found")

    return result


@router.post("/between-programs")
def convert_between_programs(request: ConvertBetweenProgramsRequest, db: Session = Depends(get_db)):
    """Convertir puntos entre dos programas (via Avios)"""
    calculator = PointsCalculator(db)
    result = calculator.convert_between_programs(
        request.source_program_id,
        request.target_program_id,
        request.points,
        request.bonus_percentage
    )

    if result is None:
        raise HTTPException(status_code=404, detail="One or both programs not found")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.get("/all-to-avios/{points}")
def get_all_conversions_to_avios(points: float, db: Session = Depends(get_db)):
    """Obtener todas las conversiones posibles a Avios para una cantidad de puntos"""
    calculator = PointsCalculator(db)
    return calculator.get_all_conversions_to_avios(points)


@router.post("/compare-value")
def compare_value(request: CompareValueRequest, db: Session = Depends(get_db)):
    """Comparar el valor en Avios de diferentes cantidades de puntos"""
    calculator = PointsCalculator(db)
    return calculator.compare_value(request.points_dict)
