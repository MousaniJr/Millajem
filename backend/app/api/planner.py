from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
import json

from ..database import get_db
from .. import models

router = APIRouter(prefix="/planner", tags=["planner"])


class StrategyRequest(BaseModel):
    category: str  # "hotel", "fuel", "restaurants", "supermarkets", "travel", "shopping", "rideshare"
    amount: float  # Amount in local currency
    country: str  # "ES", "BR", "GI"


class TripMapRequest(BaseModel):
    origin: str
    destination: str
    passengers: int = 1
    cabin: str = "economy"
    country: str = "ES"
    flexibility: str = "medium"


class LostMilesRequest(BaseModel):
    country: str
    monthly_hotel: float = 0
    monthly_fuel: float = 0
    monthly_restaurants: float = 0
    monthly_supermarkets: float = 0
    monthly_travel: float = 0
    monthly_shopping: float = 0
    monthly_rideshare: float = 0
    monthly_utilities: float = 0


class PaymentOption(BaseModel):
    card_name: str
    card_bank: str
    card_points: float
    card_earning_rate: float
    card_program_name: Optional[str] = None
    total_avios: float
    avios_per_euro: float
    programs_needed: List[str]


class PartnerStoreOption(BaseModel):
    name: str
    portal_name: str
    program_name: Optional[str] = None
    base_rate: float
    promo_rate: Optional[float] = None
    effective_rate: float
    total_points: float
    total_avios: float
    supports_gift_card: bool
    supports_stacking: bool
    confidence: Optional[str] = None
    notes: Optional[str] = None


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
    partner_store_options: List[PartnerStoreOption] = Field(default_factory=list)
    stack_steps: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class StrategyResponse(BaseModel):
    category: str
    amount: float
    country: str
    strategies: List[StrategyItem]


class TransferRouteItem(BaseModel):
    id: int
    source_program: str
    target_program: str
    base_ratio: float
    typical_bonus_min: Optional[float] = None
    typical_bonus_max: Optional[float] = None
    current_bonus: Optional[float] = None
    effective_ratio: float
    confidence: Optional[str] = None
    notes: Optional[str] = None


class AwardRouteItem(BaseModel):
    id: int
    route_name: str
    origin: str
    destination: str
    cabin: str
    program_name: str
    operating_airlines: Optional[str] = None
    alliance: Optional[str] = None
    table_type: Optional[str] = None
    points_one_way: Optional[float] = None
    total_points: Optional[float] = None
    taxes_estimate: Optional[float] = None
    taxes_currency: Optional[str] = None
    baggage_included: bool
    change_policy: Optional[str] = None
    cancellation_policy: Optional[str] = None
    recommended_booking_window: Optional[str] = None
    notes: Optional[str] = None


class TripMapResponse(BaseModel):
    origin: str
    destination: str
    passengers: int
    cabin: str
    routes: List[AwardRouteItem]
    transfer_routes: List[TransferRouteItem]
    decision_steps: List[str]
    warnings: List[str]


class LostMilesResponse(BaseModel):
    country: str
    annual_spend: float
    conservative_points: float
    aggressive_points: float
    conservative_avios: float
    aggressive_avios: float
    recommendations: List[str]


def points_to_avios(points: float, program: Optional[models.LoyaltyProgram]) -> float:
    if not program or not program.avios_ratio or program.avios_ratio <= 0:
        return 0
    return points / program.avios_ratio


def transfer_effective_ratio(route: models.TransferRoute) -> float:
    bonus = route.current_bonus or 0
    return route.base_ratio / (1 + (bonus / 100))


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
        "gift_cards": ["gift_cards", "shopping", "shopping_portal"],
        "rideshare": ["rideshare", "transport"],
        "utilities": ["utilities"],
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
        opp_avios = points_to_avios(opp_points, opp_program)
        opportunity_earns_redeemable = bool(opp_program and opp_program.avios_ratio and opp_program.avios_ratio > 0)

        earning_currency = None
        if not opportunity_earns_redeemable and opp_program:
            earning_currency = opp_program.currency

        payment_options = []
        for card in cards:
            card_program = programs.get(card.loyalty_program_id)
            card_rate = calc_card_rate(card, aliases)
            card_points = card_rate * request.amount
            card_avios = points_to_avios(card_points, card_program)
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

        partner_store_options = []
        stores = db.query(models.PartnerStore).filter(
            models.PartnerStore.country.in_([request.country, "INT", "UK"] if request.country == "GI" else [request.country, "INT"]),
            models.PartnerStore.category.in_(aliases + [request.category]),
            models.PartnerStore.is_active == True,
        ).order_by(models.PartnerStore.promo_rate.desc().nullslast(), models.PartnerStore.base_rate.desc()).limit(5).all()

        for store in stores:
            store_program = programs.get(store.loyalty_program_id)
            effective_rate = store.promo_rate or store.base_rate
            store_points = effective_rate * request.amount
            store_avios = points_to_avios(store_points, store_program)
            partner_store_options.append(PartnerStoreOption(
                name=store.name,
                portal_name=store.portal_name,
                program_name=store_program.name if store_program else None,
                base_rate=store.base_rate,
                promo_rate=store.promo_rate,
                effective_rate=effective_rate,
                total_points=round(store_points, 1),
                total_avios=round(store_avios, 1),
                supports_gift_card=store.supports_gift_card,
                supports_stacking=store.supports_stacking,
                confidence=store.confidence,
                notes=store.notes,
            ))

        stack_steps = []
        warnings = []
        if opp.category in ["shopping_portal", "shopping", "gift_cards"] or partner_store_options:
            stack_steps = [
                "Busca primero la tienda en Iberia Shopping, BA eStore, Vueling eStore u otro portal activo.",
                "Si existe gift card bonificada, compra la gift card antes de entrar en la tienda final.",
                "Paga con la tarjeta que más puntos genere y conserva capturas/confirmaciones del tracking.",
            ]
        if opp.confidence == "stale":
            warnings.append("Dato marcado como desactualizado: verifica la fuente antes de comprar.")

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
            partner_store_options=partner_store_options,
            stack_steps=stack_steps,
            warnings=warnings,
        ))

    # Add a card-only strategy (no opportunity, just best cards)
    card_only_options = []
    for card in cards:
        card_program = programs.get(card.loyalty_program_id)
        card_rate = calc_card_rate(card, aliases)
        card_points = card_rate * request.amount
        card_avios = points_to_avios(card_points, card_program)
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
            stack_steps=["Usa tarjeta solo como capa final; primero comprueba si existe portal, gift card o partner directo."],
            warnings=["Estrategia menos potente que una compra bonificada si existe portal o partner activo."],
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


@router.get("/partner-stores", response_model=List[PartnerStoreOption])
def list_partner_stores(
    country: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.PartnerStore).filter(models.PartnerStore.is_active == True)
    if country:
        countries = [country, "INT", "UK"] if country == "GI" else [country, "INT"]
        query = query.filter(models.PartnerStore.country.in_(countries))
    if category:
        query = query.filter(models.PartnerStore.category == category)

    programs = {p.id: p for p in db.query(models.LoyaltyProgram).all()}
    stores = query.order_by(models.PartnerStore.promo_rate.desc().nullslast(), models.PartnerStore.base_rate.desc()).all()
    return [
        PartnerStoreOption(
            name=s.name,
            portal_name=s.portal_name,
            program_name=programs[s.loyalty_program_id].name if s.loyalty_program_id in programs else None,
            base_rate=s.base_rate,
            promo_rate=s.promo_rate,
            effective_rate=s.promo_rate or s.base_rate,
            total_points=0,
            total_avios=0,
            supports_gift_card=s.supports_gift_card,
            supports_stacking=s.supports_stacking,
            confidence=s.confidence,
            notes=s.notes,
        )
        for s in stores
    ]


@router.get("/transfer-routes", response_model=List[TransferRouteItem])
def list_transfer_routes(
    source_program: Optional[str] = None,
    target_program: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.TransferRoute).filter(models.TransferRoute.is_active == True)
    if source_program:
        query = query.join(models.TransferRoute.source_program).filter(models.LoyaltyProgram.name.ilike(f"%{source_program}%"))
    if target_program:
        query = query.join(models.TransferRoute.target_program).filter(models.LoyaltyProgram.name.ilike(f"%{target_program}%"))
    routes = query.all()
    return [
        TransferRouteItem(
            id=r.id,
            source_program=r.source_program.name,
            target_program=r.target_program.name,
            base_ratio=r.base_ratio,
            typical_bonus_min=r.typical_bonus_min,
            typical_bonus_max=r.typical_bonus_max,
            current_bonus=r.current_bonus,
            effective_ratio=round(transfer_effective_ratio(r), 3),
            confidence=r.confidence,
            notes=r.notes,
        )
        for r in routes
    ]


@router.get("/award-routes", response_model=List[AwardRouteItem])
def list_award_routes(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    cabin: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.AwardRoute).filter(models.AwardRoute.is_active == True)
    if origin:
        query = query.filter(models.AwardRoute.origin.ilike(f"%{origin}%"))
    if destination:
        query = query.filter(models.AwardRoute.destination.ilike(f"%{destination}%"))
    if cabin:
        query = query.filter(models.AwardRoute.cabin == cabin)
    routes = query.all()
    return [
        AwardRouteItem(
            id=r.id,
            route_name=r.route_name,
            origin=r.origin,
            destination=r.destination,
            cabin=r.cabin,
            program_name=r.program.name,
            operating_airlines=r.operating_airlines,
            alliance=r.alliance,
            table_type=r.table_type,
            points_one_way=r.points_one_way,
            total_points=r.points_one_way,
            taxes_estimate=r.taxes_estimate,
            taxes_currency=r.taxes_currency,
            baggage_included=r.baggage_included,
            change_policy=r.change_policy,
            cancellation_policy=r.cancellation_policy,
            recommended_booking_window=r.recommended_booking_window,
            notes=r.notes,
        )
        for r in routes
    ]


@router.post("/trip-map", response_model=TripMapResponse)
def get_trip_map(request: TripMapRequest, db: Session = Depends(get_db)):
    route_query = db.query(models.AwardRoute).filter(
        models.AwardRoute.is_active == True,
        models.AwardRoute.cabin == request.cabin,
    )
    origin = request.origin.strip()
    destination = request.destination.strip()
    if origin:
        route_query = route_query.filter(models.AwardRoute.origin.ilike(f"%{origin}%"))
    if destination:
        route_query = route_query.filter(models.AwardRoute.destination.ilike(f"%{destination}%"))

    routes = route_query.order_by(models.AwardRoute.points_one_way.asc().nullslast()).all()
    if not routes:
        routes = db.query(models.AwardRoute).filter(
            models.AwardRoute.is_active == True,
            models.AwardRoute.cabin == request.cabin,
            models.AwardRoute.region.in_(["BR", "South America", "Europe-Brazil"]),
        ).order_by(models.AwardRoute.points_one_way.asc().nullslast()).limit(8).all()

    program_ids = {r.program_id for r in routes}
    transfers = []
    if program_ids:
        transfers = db.query(models.TransferRoute).filter(
            models.TransferRoute.is_active == True,
            models.TransferRoute.target_program_id.in_(program_ids),
        ).all()

    route_items = [
        AwardRouteItem(
            id=r.id,
            route_name=r.route_name,
            origin=r.origin,
            destination=r.destination,
            cabin=r.cabin,
            program_name=r.program.name,
            operating_airlines=r.operating_airlines,
            alliance=r.alliance,
            table_type=r.table_type,
            points_one_way=r.points_one_way,
            total_points=(r.points_one_way or 0) * request.passengers,
            taxes_estimate=(r.taxes_estimate or 0) * request.passengers if r.taxes_estimate else None,
            taxes_currency=r.taxes_currency,
            baggage_included=r.baggage_included,
            change_policy=r.change_policy,
            cancellation_policy=r.cancellation_policy,
            recommended_booking_window=r.recommended_booking_window,
            notes=r.notes,
        )
        for r in routes
    ]

    transfer_items = [
        TransferRouteItem(
            id=t.id,
            source_program=t.source_program.name,
            target_program=t.target_program.name,
            base_ratio=t.base_ratio,
            typical_bonus_min=t.typical_bonus_min,
            typical_bonus_max=t.typical_bonus_max,
            current_bonus=t.current_bonus,
            effective_ratio=round(transfer_effective_ratio(t), 3),
            confidence=t.confidence,
            notes=t.notes,
        )
        for t in transfers
    ]

    return TripMapResponse(
        origin=request.origin,
        destination=request.destination,
        passengers=request.passengers,
        cabin=request.cabin,
        routes=route_items,
        transfer_routes=transfer_items,
        decision_steps=[
            "Confirma qué aerolíneas vuelan la ruta antes de acumular puntos.",
            "Elige programa de emisión por disponibilidad, tasas, equipaje y política de cambios.",
            "Después decide si conviene acumular, comprar puntos o esperar transferencia bonificada.",
            "Valida disponibilidad en el programa final antes de transferir puntos.",
        ],
        warnings=[
            "No transfieras puntos hasta confirmar disponibilidad real.",
            "Los datos de tasas y disponibilidad cambian; verifica la fuente antes de emitir.",
        ],
    )


@router.post("/lost-miles", response_model=LostMilesResponse)
def calculate_lost_miles(request: LostMilesRequest):
    spend_by_category = {
        "hotel": request.monthly_hotel,
        "fuel": request.monthly_fuel,
        "restaurants": request.monthly_restaurants,
        "supermarkets": request.monthly_supermarkets,
        "travel": request.monthly_travel,
        "shopping": request.monthly_shopping,
        "rideshare": request.monthly_rideshare,
        "utilities": request.monthly_utilities,
    }
    annual_spend = sum(spend_by_category.values()) * 12
    conservative_rates = {
        "hotel": 4,
        "fuel": 1,
        "restaurants": 2,
        "supermarkets": 1,
        "travel": 3,
        "shopping": 3,
        "rideshare": 1,
        "utilities": 0.5,
    }
    aggressive_rates = {
        "hotel": 10,
        "fuel": 2,
        "restaurants": 4,
        "supermarkets": 2,
        "travel": 8,
        "shopping": 10,
        "rideshare": 2,
        "utilities": 1,
    }
    conservative_points = sum(spend_by_category[k] * 12 * conservative_rates[k] for k in spend_by_category)
    aggressive_points = sum(spend_by_category[k] * 12 * aggressive_rates[k] for k in spend_by_category)

    return LostMilesResponse(
        country=request.country,
        annual_spend=round(annual_spend, 2),
        conservative_points=round(conservative_points, 0),
        aggressive_points=round(aggressive_points, 0),
        conservative_avios=round(conservative_points, 0),
        aggressive_avios=round(aggressive_points, 0),
        recommendations=[
            "Prioriza portales y compras bonificadas antes que solo tarjeta.",
            "Revisa gift cards y partners directos en compras grandes.",
            "Activa alertas para multiplicadores temporales y transferencias bonificadas.",
        ],
    )
