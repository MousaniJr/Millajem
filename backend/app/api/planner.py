from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json

from ..database import get_db
from .. import models

router = APIRouter(prefix="/planner", tags=["planner"])


class StrategyRequest(BaseModel):
    category: str  # "hotel", "fuel", "restaurants", "supermarkets", "travel", "shopping", "rideshare"
    amount: float  # Amount in local currency
    country: str  # "ES", "BR", "GI"


class StrategyItem(BaseModel):
    rank: int
    # Earning opportunity info
    opportunity_name: Optional[str] = None
    opportunity_earning_description: Optional[str] = None
    opportunity_points: float
    opportunity_how_to_use: Optional[str] = None
    opportunity_program_name: Optional[str] = None
    # Card info
    card_name: Optional[str] = None
    card_bank: Optional[str] = None
    card_points: float
    card_earning_rate: float
    card_program_name: Optional[str] = None
    # Totals
    total_points: float
    avios_equivalent: float
    avios_per_euro: float
    # Avios redeemability
    is_avios_redeemable: bool  # True if points can be converted to Avios
    opportunity_earns_redeemable: bool  # True if the opportunity itself earns redeemable points (not cash/saldo)
    earning_currency: Optional[str] = None  # Currency name for non-Avios (e.g. "Pontos Livelo")
    # Enrollment status
    all_enrolled: bool  # True if user is enrolled in all required programs
    programs_needed: List[str]  # Programs not yet enrolled


class StrategyResponse(BaseModel):
    category: str
    amount: float
    country: str
    strategies: List[StrategyItem]


@router.post("/strategies", response_model=StrategyResponse)
def get_strategies(request: StrategyRequest, db: Session = Depends(get_db)):
    """Get ranked earning strategies for a planned purchase"""

    # Map category aliases for bonus_categories matching
    category_aliases = {
        "hotel": ["hotels", "hotel", "travel"],
        "fuel": ["fuel"],
        "restaurants": ["restaurants", "dining"],
        "supermarkets": ["supermarkets", "groceries"],
        "travel": ["travel", "flights", "airline"],
        "shopping": ["shopping", "shopping_portal", "all"],
        "rideshare": ["rideshare", "transport"],
    }

    aliases = category_aliases.get(request.category, [request.category])

    # 1. Get earning opportunities matching category + country
    opportunities = db.query(models.EarningOpportunity).filter(
        models.EarningOpportunity.country.in_([request.country, "INT"]),
        models.EarningOpportunity.category.in_(aliases + [request.category + "s", request.category]),
        models.EarningOpportunity.is_active == True,
    ).all()

    # 2. Get credit cards matching country
    cards = db.query(models.CreditCard).filter(
        models.CreditCard.country.in_([request.country, "INT"]),
        models.CreditCard.is_available == True,
    ).all()

    # 3. Get all loyalty programs for enrollment check
    programs = {p.id: p for p in db.query(models.LoyaltyProgram).all()}

    strategies = []

    # Generate strategies: each opportunity + each card combo
    for opp in opportunities:
        opp_program = programs.get(opp.loyalty_program_id)
        opp_points = opp.earning_rate * request.amount

        for card in cards:
            card_program = programs.get(card.loyalty_program_id)

            # Calculate card earning rate for this category
            card_rate = card.base_earning_rate
            if card.bonus_categories:
                try:
                    bonus = json.loads(card.bonus_categories)
                    for alias in aliases:
                        if alias in bonus:
                            card_rate = max(card_rate, bonus[alias])
                            break
                except (json.JSONDecodeError, TypeError):
                    pass

            card_points = card_rate * request.amount

            # Calculate Avios equivalent
            opp_avios = opp_points * (opp_program.avios_ratio if opp_program and opp_program.avios_ratio else 0)
            card_avios = card_points * (card_program.avios_ratio if card_program and card_program.avios_ratio else 0)
            total_avios = opp_avios + card_avios
            is_avios_redeemable = total_avios > 0
            # Does the opportunity ITSELF earn redeemable points (not cash/saldo)?
            opportunity_earns_redeemable = bool(opp_program and opp_program.avios_ratio and opp_program.avios_ratio > 0)

            avios_per_euro = total_avios / request.amount if request.amount > 0 and total_avios > 0 else 0

            # Determine earning currency for non-Avios strategies
            earning_currency = None
            if not is_avios_redeemable:
                if opp_program:
                    earning_currency = opp_program.currency
                elif card_program:
                    earning_currency = card_program.currency

            # Check enrollment
            programs_needed = []
            if opp_program and not opp_program.is_enrolled:
                programs_needed.append(opp_program.name)
            if card_program and not card_program.is_enrolled and (not opp_program or card_program.id != opp_program.id):
                programs_needed.append(card_program.name)

            strategies.append(StrategyItem(
                rank=0,
                opportunity_name=opp.name,
                opportunity_earning_description=opp.earning_description,
                opportunity_points=round(opp_points, 1),
                opportunity_how_to_use=opp.how_to_use,
                opportunity_program_name=opp_program.name if opp_program else None,
                card_name=card.name,
                card_bank=card.bank,
                card_points=round(card_points, 1),
                card_earning_rate=card_rate,
                card_program_name=card_program.name if card_program else None,
                total_points=round(opp_points + card_points, 1),
                avios_equivalent=round(total_avios, 1),
                avios_per_euro=round(avios_per_euro, 2),
                is_avios_redeemable=is_avios_redeemable,
                opportunity_earns_redeemable=opportunity_earns_redeemable,
                earning_currency=earning_currency,
                all_enrolled=len(programs_needed) == 0,
                programs_needed=programs_needed,
            ))

    # Also add card-only strategies (no earning opportunity, just paying with a card)
    for card in cards:
        card_program = programs.get(card.loyalty_program_id)

        card_rate = card.base_earning_rate
        if card.bonus_categories:
            try:
                bonus = json.loads(card.bonus_categories)
                for alias in aliases:
                    if alias in bonus:
                        card_rate = max(card_rate, bonus[alias])
                        break
            except (json.JSONDecodeError, TypeError):
                pass

        card_points = card_rate * request.amount
        card_avios = card_points * (card_program.avios_ratio if card_program and card_program.avios_ratio else 0)
        is_avios_redeemable = card_avios > 0

        avios_per_euro = card_avios / request.amount if request.amount > 0 and card_avios > 0 else 0

        earning_currency = None
        if not is_avios_redeemable and card_program:
            earning_currency = card_program.currency

        programs_needed = []
        if card_program and not card_program.is_enrolled:
            programs_needed.append(card_program.name)

        strategies.append(StrategyItem(
            rank=0,
            opportunity_name=None,
            opportunity_earning_description=None,
            opportunity_points=0,
            opportunity_how_to_use=None,
            opportunity_program_name=None,
            card_name=card.name,
            card_bank=card.bank,
            card_points=round(card_points, 1),
            card_earning_rate=card_rate,
            card_program_name=card_program.name if card_program else None,
            total_points=round(card_points, 1),
            avios_equivalent=round(card_avios, 1),
            avios_per_euro=round(avios_per_euro, 2),
            is_avios_redeemable=is_avios_redeemable,
            opportunity_earns_redeemable=True,  # Card-only: no non-redeemable opportunity
            earning_currency=earning_currency,
            all_enrolled=len(programs_needed) == 0,
            programs_needed=programs_needed,
        ))

    # Sort: redeemable opportunities first, then Avios-redeemable, then enrolled, then by avios_per_euro
    strategies.sort(key=lambda s: (
        -int(s.opportunity_earns_redeemable),  # Redeemable opportunities first
        -int(s.is_avios_redeemable),
        -int(s.all_enrolled),
        -s.avios_per_euro if s.is_avios_redeemable else 0,
        -s.total_points if not s.is_avios_redeemable else 0,
    ))

    # Assign ranks
    for i, s in enumerate(strategies):
        s.rank = i + 1

    return StrategyResponse(
        category=request.category,
        amount=request.amount,
        country=request.country,
        strategies=strategies,
    )
