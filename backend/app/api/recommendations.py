from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models
from ..schemas import recommendations as rec_schemas

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/cards", response_model=List[rec_schemas.CreditCard])
def list_credit_cards(
    country: Optional[str] = None,
    min_score: int = Query(50, ge=0, le=100),
    db: Session = Depends(get_db)
):
    """Listar tarjetas de crédito recomendadas"""
    query = db.query(models.CreditCard).filter(
        models.CreditCard.recommendation_score >= min_score
    )

    if country:
        query = query.filter(models.CreditCard.country == country)

    # Ordenar por score descendente
    return query.order_by(models.CreditCard.recommendation_score.desc()).all()


@router.get("/cards/{card_id}", response_model=rec_schemas.CreditCard)
def get_credit_card(card_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de una tarjeta"""
    return db.query(models.CreditCard).filter(models.CreditCard.id == card_id).first()


@router.get("/opportunities", response_model=List[rec_schemas.EarningOpportunity])
def list_earning_opportunities(
    country: Optional[str] = None,
    category: Optional[str] = None,
    min_score: int = Query(50, ge=0, le=100),
    db: Session = Depends(get_db)
):
    """Listar oportunidades de ganar puntos"""
    query = db.query(models.EarningOpportunity).filter(
        models.EarningOpportunity.recommendation_score >= min_score,
        models.EarningOpportunity.is_active == True
    )

    if country:
        query = query.filter(models.EarningOpportunity.country == country)

    if category:
        query = query.filter(models.EarningOpportunity.category == category)

    return query.order_by(models.EarningOpportunity.recommendation_score.desc()).all()


@router.get("/top-cards/{country}")
def get_top_cards_by_country(
    country: str,
    limit: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """Obtener top N tarjetas por país"""
    cards = db.query(models.CreditCard).filter(
        models.CreditCard.country == country,
        models.CreditCard.is_available == True
    ).order_by(
        models.CreditCard.recommendation_score.desc()
    ).limit(limit).all()

    return [
        {
            "id": card.id,
            "name": card.name,
            "bank": card.bank,
            "earning_rate": card.base_earning_rate,
            "annual_fee": card.annual_fee,
            "currency": card.currency,
            "welcome_bonus": card.welcome_bonus,
            "recommendation_score": card.recommendation_score,
            "notes": card.notes,
            "program": card.loyalty_program.name if card.loyalty_program else None
        }
        for card in cards
    ]


@router.get("/strategy/{country}")
def get_strategy_for_country(country: str, db: Session = Depends(get_db)):
    """Obtener estrategia recomendada para un país"""

    # Top tarjeta
    top_card = db.query(models.CreditCard).filter(
        models.CreditCard.country == country,
        models.CreditCard.is_available == True
    ).order_by(models.CreditCard.recommendation_score.desc()).first()

    # Top opportunities
    opportunities = db.query(models.EarningOpportunity).filter(
        models.EarningOpportunity.country == country,
        models.EarningOpportunity.is_active == True
    ).order_by(models.EarningOpportunity.recommendation_score.desc()).limit(5).all()

    return {
        "country": country,
        "recommended_card": {
            "name": top_card.name,
            "earning_rate": top_card.base_earning_rate,
            "annual_fee": top_card.annual_fee,
            "welcome_bonus": top_card.welcome_bonus,
            "notes": top_card.notes
        } if top_card else None,
        "earning_opportunities": [
            {
                "name": opp.name,
                "category": opp.category,
                "earning_description": opp.earning_description,
                "how_to_use": opp.how_to_use
            }
            for opp in opportunities
        ]
    }
