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


class PaymentOption(BaseModel):
    card_name: str
    card_bank: str
    card_points: float
    card_earning_rate: float
    card_program_name: Optional[str] = None
    total_avios: float
    avios_per_euro: float
    programs_needed: List[str]


class StrategyItem(BaseModel):
    rank: int
    # Earning opportunity info
    opportunity_name: Optional[str] = None
    opportunity_earning_description: Optional[str] = None
    opportunity_points: float
    opportunity_how_to_use: Optional[str] = None
    opportunity_program_name: Optional[str] = None
    # Avios redeemability
    is_avios_redeemable: bool
    opportunity_earns_redeemable: bool
    earning_currency: Optional[str] = None
    # Payment options (sorted best to worst)
    payment_options: List[PaymentOption]
    # Best option summary
    best_avios_per_euro: float
    best_total_avios: float


class StrategyResponse(BaseModel):
    category: str
    amount: float
    country: str
    strategies: List[StrategyItem]


@router.post("/strategies", response_model=StrategyResponse)
def get_strategies(request: StrategyRequest, db: Session = Depends(get_db)):
    """Get ranked earning strategies for a planned purchase"""

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

    # 3. Get all loyalty programs
    programs = {p.id: p for p in db.query(models.LoyaltyProgram).all()}

    def calc_card_rate(card, aliases):
        rate = card.base_earning_rate
        if card.bonus_categories:
            try:
                bonus = json.loads(card.bonus_categories)
                for alias in aliases:
                    if alias in bonus:
                        rate = max(rate, bonus[alias])
                        break
            except (json.JSONDecodeError, TypeError):
                pass
        return rate

    strategies = []

    # Generate strategies: one per opportunity, with all card options inside
    for opp in opportunities:
        opp_program = programs.get(opp.loyalty_program_id)
        opp_points = opp.earning_rate * request.amount
        opp_avios = opp_points * (opp_program.avios_ratio if opp_program and opp_program.avios_ratio else 0)
        opportunity_earns_redeemable = bool(opp_program and opp_program.avios_ratio and opp_program.avios_ratio > 0)

        earning_currency = None
        if not opportunity_earns_redeemable and opp_program:
            earning_currency = opp_program.currency

        payment_options = []
        for card in cards:
            card_program = programs.get(card.loyalty_program_id)
            card_rate = calc_card_rate(card, aliases)
            card_points = card_rate * request.amount
            card_avios = card_points * (card_program.avios_ratio if card_program and card_program.avios_ratio else 0)
            total_avios = opp_avios + card_avios
            avios_per_euro = total_avios / request.amount if request.amount > 0 and total_avios > 0 else 0

            progs_needed = []
            if opp_program and not opp_program.is_enrolled:
                progs_needed.append(opp_program.name)
            if card_program and not card_program.is_enrolled and (not opp_program or card_program.id != opp_program.id):
                progs_needed.append(card_program.name)

            payment_options.append(PaymentOption(
                card_name=card.name,
                card_bank=card.bank,
                card_points=round(card_points, 1),
                card_earning_rate=card_rate,
                card_program_name=card_program.name if card_program else None,
                total_avios=round(total_avios, 1),
                avios_per_euro=round(avios_per_euro, 2),
                programs_needed=progs_needed,
            ))

        # Sort payment options: highest avios_per_euro first
        payment_options.sort(key=lambda p: (-p.avios_per_euro, -p.total_avios))

        # Filter out cards with 0 avios if there are better options
        if any(p.avios_per_euro > 0 for p in payment_options):
            payment_options = [p for p in payment_options if p.avios_per_euro > 0]

        if not payment_options:
            continue

        best = payment_options[0]
        is_avios_redeemable = best.total_avios > 0

        strategies.append(StrategyItem(
            rank=0,
            opportunity_name=opp.name,
            opportunity_earning_description=opp.earning_description,
            opportunity_points=round(opp_points, 1),
            opportunity_how_to_use=opp.how_to_use,
            opportunity_program_name=opp_program.name if opp_program else None,
            is_avios_redeemable=is_avios_redeemable,
            opportunity_earns_redeemable=opportunity_earns_redeemable,
            earning_currency=earning_currency,
            payment_options=payment_options,
            best_avios_per_euro=best.avios_per_euro,
            best_total_avios=best.total_avios,
        ))

    # Add a card-only strategy (no opportunity, just best cards)
    card_only_options = []
    for card in cards:
        card_program = programs.get(card.loyalty_program_id)
        card_rate = calc_card_rate(card, aliases)
        card_points = card_rate * request.amount
        card_avios = card_points * (card_program.avios_ratio if card_program and card_program.avios_ratio else 0)
        avios_per_euro = card_avios / request.amount if request.amount > 0 and card_avios > 0 else 0

        progs_needed = []
        if card_program and not card_program.is_enrolled:
            progs_needed.append(card_program.name)

        card_only_options.append(PaymentOption(
            card_name=card.name,
            card_bank=card.bank,
            card_points=round(card_points, 1),
            card_earning_rate=card_rate,
            card_program_name=card_program.name if card_program else None,
            total_avios=round(card_avios, 1),
            avios_per_euro=round(avios_per_euro, 2),
            programs_needed=progs_needed,
        ))

    card_only_options.sort(key=lambda p: (-p.avios_per_euro, -p.total_avios))
    if any(p.avios_per_euro > 0 for p in card_only_options):
        card_only_options = [p for p in card_only_options if p.avios_per_euro > 0]

    if card_only_options:
        best = card_only_options[0]
        strategies.append(StrategyItem(
            rank=0,
            opportunity_name=None,
            opportunity_earning_description=None,
            opportunity_points=0,
            opportunity_how_to_use=None,
            opportunity_program_name=None,
            is_avios_redeemable=best.total_avios > 0,
            opportunity_earns_redeemable=True,
            earning_currency=None,
            payment_options=card_only_options,
            best_avios_per_euro=best.avios_per_euro,
            best_total_avios=best.total_avios,
        ))

    # Sort strategies
    strategies.sort(key=lambda s: (
        -int(s.opportunity_earns_redeemable),
        -int(s.is_avios_redeemable),
        -s.best_avios_per_euro,
        -s.best_total_avios,
    ))

    for i, s in enumerate(strategies):
        s.rank = i + 1

    return StrategyResponse(
        category=request.category,
        amount=request.amount,
        country=request.country,
        strategies=strategies,
    )
