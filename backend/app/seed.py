"""
Seed de datos iniciales para Millajem.
Se ejecuta automáticamente en startup si las tablas están vacías.
"""
from sqlalchemy.orm import Session
from . import models


def seed_loyalty_programs(db: Session) -> dict:
    """Inserta programas de fidelidad y devuelve mapa nombre->id"""
    programs = [
        # España / Avios
        dict(name="Iberia Club", currency="Avios", country="ES", category="airline",
             avios_ratio=1.0,
             website_url="https://www.iberia.com/es/iberia-plus/",
             login_url="https://www.iberia.com/es/login/",
             notes="Programa principal. Permite Family Account con 7 miembros (necesita Silver)."),
        dict(name="British Airways Executive Club", currency="Avios", country="INT", category="airline",
             avios_ratio=1.0,
             website_url="https://www.britishairways.com/es-es/executive-club",
             login_url="https://www.britishairways.com/es-es/login",
             notes="Household Account disponible. GIB-LHR = 7.250 Avios off-peak."),
        dict(name="American Express Membership Rewards ES", currency="MR Points", country="ES", category="transfer",
             avios_ratio=1.0,
             website_url="https://www.americanexpress.com/es-es/rewards/membership-rewards/index.mtw",
             notes="1 MR = 1 Avios (Iberia o BA). Mejor ratio de transferencia en España."),
        dict(name="Vueling Club", currency="Avios", country="ES", category="airline",
             avios_ratio=1.0,
             website_url="https://www.vueling.com/es/vueling-club/que-es-vueling-club",
             notes="Usa Avios como moneda. Acumula volando Vueling y con partners. Intercambiable con Iberia Club y BA."),

        # Brasil
        dict(name="Livelo", currency="Pontos Livelo", country="BR", category="transfer",
             avios_ratio=1.0,
             website_url="https://www.livelo.com.br/",
             notes="Transfere a aerolíneas (1:1 con bonos). Necesita CPF. Accesible desde España."),
        dict(name="Esfera Santander", currency="Pontos Esfera", country="BR", category="shopping",
             avios_ratio=0.5,
             website_url="https://www.esfera.com.vc/",
             notes="Mejor ratio Brasil→Avios: 2 Esfera = 1 Avios vía Iberia. Necesita CPF."),
        dict(name="Smiles GOL", currency="Milhas Smiles", country="BR", category="airline",
             avios_ratio=None,
             website_url="https://www.smiles.com.br/",
             notes="Programa de GOL. Útil para vuelos internos Brasil. API reverse-engineered en GitHub."),

        # Hotel
        dict(name="Accor Live Limitless", currency="Puntos ALL", country="INT", category="hotel",
             avios_ratio=1.0,
             website_url="https://all.accor.com/",
             notes="Mejor conversión hotel→Avios: 1:1. Transfere a Iberia o BA."),
        dict(name="Marriott Bonvoy", currency="Puntos Marriott", country="INT", category="hotel",
             avios_ratio=None,
             website_url="https://www.marriott.com/loyalty/",
             notes="60.000 Marriott = 25.000 Avios. Ratio bajo."),
    ]

    program_map = {}
    for p in programs:
        exists = db.query(models.LoyaltyProgram).filter_by(name=p["name"]).first()
        if not exists:
            obj = models.LoyaltyProgram(**p)
            db.add(obj)
            db.flush()
            program_map[p["name"]] = obj.id
        else:
            program_map[p["name"]] = exists.id

    db.commit()
    return program_map


def seed_credit_cards(db: Session, program_map: dict):
    """Inserta tarjetas de crédito recomendadas"""
    iberia_id = program_map.get("Iberia Club")
    ba_id = program_map.get("British Airways Executive Club")
    amex_mr_id = program_map.get("American Express Membership Rewards ES")
    livelo_id = program_map.get("Livelo")

    cards = [
        # ===== ESPAÑA =====
        dict(
            name="American Express Platinum España",
            bank="American Express",
            country="ES",
            card_network="Amex",
            loyalty_program_id=amex_mr_id,
            base_earning_rate=1.0,
            bonus_categories='{"travel": 2.0}',
            annual_fee=700.0,
            currency="EUR",
            first_year_fee=None,
            welcome_bonus=40000,
            welcome_bonus_requirement="Gasta 5.000 EUR en los primeros 3 meses",
            minimum_income=None,
            is_available=True,
            application_url="https://www.americanexpress.com/es-es/tarjetas/tarjetas-de-cargo/tarjeta-platinum/",
            notes="1 MR = 1 Avios (Iberia/BA). Acceso salones, seguro viaje premium. Mejor tarjeta ES.",
            recommendation_score=95,
        ),
        dict(
            name="American Express Gold España",
            bank="American Express",
            country="ES",
            card_network="Amex",
            loyalty_program_id=amex_mr_id,
            base_earning_rate=1.0,
            bonus_categories='{"restaurants": 2.0, "supermarkets": 2.0}',
            annual_fee=160.0,
            currency="EUR",
            first_year_fee=0.0,
            welcome_bonus=20000,
            welcome_bonus_requirement="Gasta 3.000 EUR en los primeros 3 meses",
            minimum_income=None,
            is_available=True,
            application_url="https://www.americanexpress.com/es-es/tarjetas/tarjetas-de-cargo/tarjeta-gold-card/",
            notes="Primer año gratis. 1 MR = 1 Avios. Relación calidad/precio excelente para España.",
            recommendation_score=92,
        ),
        dict(
            name="Iberia Visa Iconic",
            bank="CaixaBank",
            country="ES",
            card_network="Visa",
            loyalty_program_id=iberia_id,
            base_earning_rate=3.0,
            bonus_categories='{"iberia": 5.0}',
            annual_fee=220.0,
            currency="EUR",
            first_year_fee=None,
            welcome_bonus=25000,
            welcome_bonus_requirement="Gasta 3.000 EUR en los primeros 4 meses",
            minimum_income=None,
            is_available=True,
            application_url="https://www.iberia.com/es/iberia-plus/tarjeta-iconic/",
            notes="Acumula Avios directamente. Mejor para gastos en Iberia. Upgrade a Silver más fácil.",
            recommendation_score=88,
        ),
        dict(
            name="Iberia Visa Classic",
            bank="CaixaBank",
            country="ES",
            card_network="Visa",
            loyalty_program_id=iberia_id,
            base_earning_rate=1.5,
            bonus_categories=None,
            annual_fee=60.0,
            currency="EUR",
            first_year_fee=0.0,
            welcome_bonus=6000,
            welcome_bonus_requirement="Gasta 1.000 EUR en los primeros 4 meses",
            minimum_income=None,
            is_available=True,
            application_url="https://www.iberia.com/es/iberia-plus/tarjeta-classic/",
            notes="Opción económica. Primer año gratis. Acumula Avios directamente.",
            recommendation_score=78,
        ),

        # ===== GIBRALTAR =====
        dict(
            name="HSBC Premier World Elite Mastercard (GIB)",
            bank="HSBC Gibraltar",
            country="GI",
            card_network="Mastercard",
            loyalty_program_id=ba_id,
            base_earning_rate=1.5,
            bonus_categories=None,
            annual_fee=0.0,
            currency="GBP",
            first_year_fee=None,
            welcome_bonus=None,
            welcome_bonus_requirement=None,
            minimum_income=None,
            is_available=True,
            application_url="https://www.hsbc.gi/",
            notes="PENDIENTE VERIFICAR con HSBC GIB. Si accesible para fronterizos = mejor tarjeta GIB. 1.5 Avios/GBP.",
            recommendation_score=80,
        ),

        # ===== BRASIL =====
        dict(
            name="Santander Unlimited Visa Infinite",
            bank="Santander Brasil",
            country="BR",
            card_network="Visa",
            loyalty_program_id=livelo_id,
            base_earning_rate=2.5,
            bonus_categories='{"travel": 3.5}',
            annual_fee=1080.0,
            currency="BRL",
            first_year_fee=None,
            welcome_bonus=None,
            welcome_bonus_requirement=None,
            minimum_income=None,
            is_available=True,
            application_url="https://www.santander.com.br/cartao-de-credito/unlimited",
            notes="Acumula Livelo. Livelo→Iberia vía Esfera (2:1) es la mejor ruta Brasil→Avios.",
            recommendation_score=85,
        ),
        dict(
            name="Itaú Personnalité Visa Infinite",
            bank="Itaú",
            country="BR",
            card_network="Visa",
            loyalty_program_id=livelo_id,
            base_earning_rate=2.0,
            bonus_categories=None,
            annual_fee=1080.0,
            currency="BRL",
            first_year_fee=None,
            welcome_bonus=None,
            welcome_bonus_requirement=None,
            minimum_income=None,
            is_available=True,
            application_url="https://www.itau.com.br/cartoes/personnalite/",
            notes="Acumula Livelo. Necesita cuenta Personnalité.",
            recommendation_score=82,
        ),
    ]

    for c in cards:
        exists = db.query(models.CreditCard).filter_by(name=c["name"]).first()
        if not exists:
            obj = models.CreditCard(**c)
            db.add(obj)

    db.commit()


def seed_earning_opportunities(db: Session, program_map: dict):
    """Inserta oportunidades de ganar puntos"""
    iberia_id = program_map.get("Iberia Club")
    ba_id = program_map.get("British Airways Executive Club")
    livelo_id = program_map.get("Livelo")
    esfera_id = program_map.get("Esfera Santander")
    all_id = program_map.get("Accor Live Limitless")

    opportunities = [
        # ===== ESPAÑA =====
        dict(
            name="Moeve (ex-Cepsa) Más — Avios por gasolina",
            category="fuel",
            country="ES",
            loyalty_program_id=iberia_id,
            earning_rate=2.0,
            earning_description="2 Avios por litro de combustible en estaciones Moeve (antes Cepsa)",
            how_to_use="Regístrate en Cepsa/Moeve Más con tu nº de Iberia Club. Usa la app en estaciones Moeve. Distinto de Club Moeve gow (que da saldo en euros).",
            requirements="Socio Iberia Club + app Moeve",
            signup_url="https://www.moeve.es/es/particular",
            notes="Partnership Moeve (ex-Cepsa) + Iberia Club: Avios directos. Coexiste con Club Moeve gow (saldo euros). Usar ambos si es posible. Cepsa rebrandeó a Moeve en 2025.",
            is_active=True,
            recommendation_score=90,
        ),
        dict(
            name="Cabify Iberia Club",
            category="rideshare",
            country="ES",
            loyalty_program_id=iberia_id,
            earning_rate=1.0,
            earning_description="1 Avios por EUR gastado en Cabify",
            how_to_use="Vincula tu cuenta Iberia Club en la app de Cabify. Cada viaje acumula Avios.",
            requirements="Socio Iberia Club + app Cabify",
            signup_url="https://www.cabify.com/es",
            notes="Fácil de usar en ciudades españolas. Acumulación automática.",
            is_active=True,
            recommendation_score=80,
        ),
        dict(
            name="Iberia Plus Shopping — Portal de compras",
            category="shopping_portal",
            country="ES",
            loyalty_program_id=iberia_id,
            earning_rate=2.0,
            earning_description="2-10 Avios por EUR en tiendas online partner",
            how_to_use="Accede a las tiendas desde el portal iberia.com/es/iberia-plus/shopping antes de comprar.",
            requirements="Socio Iberia Club",
            signup_url="https://www.iberia.com/es/iberia-plus/shopping/",
            notes="Varía según tienda. El Click originating es obligatorio para recibir los puntos.",
            is_active=True,
            recommendation_score=82,
        ),
        dict(
            name="Accor Live Limitless — Hotel a Avios",
            category="hotels",
            country="INT",
            loyalty_program_id=all_id,
            earning_rate=1.0,
            earning_description="1 Punto ALL = 1 Avios (Iberia o BA)",
            how_to_use="Acumula puntos ALL en hoteles Accor. Transfiere a Iberia Club o BA desde tu cuenta ALL.",
            requirements="Cuenta Accor ALL + cuenta Iberia Club o BA",
            signup_url="https://all.accor.com/loyalty/",
            notes="Mejor ratio hotel→Avios disponible. Sin mínimo de transferencia.",
            is_active=True,
            recommendation_score=88,
        ),

        # ===== BRASIL =====
        dict(
            name="Esfera → Iberia Club (2:1)",
            category="shopping_portal",
            country="BR",
            loyalty_program_id=iberia_id,
            earning_rate=0.5,
            earning_description="2 Pontos Esfera = 1 Avios Iberia",
            how_to_use="Acumula Esfera con tarjetas Santander Brasil. Transfiere a Iberia Club desde esfera.com.vc.",
            requirements="CPF brasileño + tarjeta Santander + cuenta Iberia Club",
            signup_url="https://www.esfera.com.vc/",
            notes="MEJOR RUTA Brasil→Avios. Necesitas CPF (obtenible en consulado brasileño en Madrid).",
            is_active=True,
            recommendation_score=95,
        ),
        dict(
            name="Livelo → Aerolíneas (1:1 con bonos)",
            category="shopping_portal",
            country="BR",
            loyalty_program_id=livelo_id,
            earning_rate=1.0,
            earning_description="1 Ponto Livelo = 1 milla (con bonos de transferencia)",
            how_to_use="Acumula Livelo con tarjetas partner. Transfiere a LATAM Pass, Smiles u otras aerolíneas.",
            requirements="CPF brasileño + cuenta Livelo",
            signup_url="https://www.livelo.com.br/",
            notes="Accesible desde España con CPF. Frecuentes bonos de transferencia del 100%.",
            is_active=True,
            recommendation_score=88,
        ),

        # ===== GIBRALTAR =====
        dict(
            name="British Airways GIB-LHR Avios",
            category="rideshare",
            country="GI",
            loyalty_program_id=ba_id,
            earning_rate=7250.0,
            earning_description="7.250 Avios por vuelo GIB-LHR off-peak (ida)",
            how_to_use="Vuela con BA entre Gibraltar y Heathrow. Acumula en BA Executive Club.",
            requirements="Cuenta BA Executive Club",
            signup_url="https://www.britishairways.com/es-es/executive-club",
            notes="Off-peak: 7.250 Avios. Peak: más alto. Directo, ~2h. Muy útil con salario GBP.",
            is_active=True,
            recommendation_score=85,
        ),
    ]

    for o in opportunities:
        exists = db.query(models.EarningOpportunity).filter_by(name=o["name"]).first()
        if not exists:
            obj = models.EarningOpportunity(**o)
            db.add(obj)

    db.commit()


def seed_sources(db: Session):
    """Inserta fuentes de información (RSS feeds, Telegram, etc.)"""
    sources = [
        # ===== ESPAÑA =====
        dict(
            name="Puntos Viajeros",
            source_type="rss_feed",
            country="ES",
            url="https://puntosviajeros.com/feed/",
            website_url="https://puntosviajeros.com",
            is_active=True,
            priority=9,
            description="Blog líder en España sobre millas y puntos. Análisis de tarjetas y estrategias.",
        ),
        # NOTE: millasdecarton.com, viajeroastuto.com, elviajeromillas.com — removed (domains dead as of Feb 2026)

        # ===== BRASIL =====
        dict(
            name="Passageiro de Primeira",
            source_type="rss_feed",
            country="BR",
            url="https://passageirodeprimeira.com/feed/",
            website_url="https://passageirodeprimeira.com",
            is_active=True,
            priority=10,
            description="Mayor referencia brasileña en milhas aéreas. Análisis y promociones.",
        ),
        dict(
            name="Quanto Vale Minha Milha",
            source_type="rss_feed",
            country="BR",
            url="https://www.quantovaleminhamilha.com.br/feed/",
            website_url="https://www.quantovaleminhamilha.com.br",
            is_active=True,
            priority=9,
            description="Valoración de milhas y comparativas de programas brasileños.",
        ),
        dict(
            name="Max Milhas Blog",
            source_type="rss_feed",
            country="BR",
            url="https://blog.maxmilhas.com.br/feed/",
            website_url="https://maxmilhas.com.br",
            is_active=True,
            priority=8,
            description="Blog de la plataforma MaxMilhas. Noticias y ofertas del mercado brasileño.",
        ),

        # ===== INTERNACIONAL =====
        dict(
            name="The Points Guy",
            source_type="rss_feed",
            country="INT",
            url="https://thepointsguy.com/feed/",
            website_url="https://thepointsguy.com",
            is_active=True,
            priority=8,
            description="Referencia mundial en puntos y millas. Enfoque USA pero muy completo.",
        ),
        dict(
            name="Head for Points",
            source_type="rss_feed",
            country="INT",
            url="https://www.headforpoints.com/feed/",
            website_url="https://www.headforpoints.com",
            is_active=True,
            priority=9,
            description="Especializado en Avios (BA y otros). Muy relevante para estrategia Avios.",
        ),
        dict(
            name="InsideFlyer",
            source_type="rss_feed",
            country="INT",
            url="https://www.insideflyer.co.uk/feed/",
            website_url="https://www.insideflyer.co.uk",
            is_active=True,
            priority=7,
            description="Noticias de programas de fidelidad internacionales.",
        ),

        # ===== TELEGRAM (manual monitoring) =====
        dict(
            name="Chollos de Vuelos",
            source_type="telegram",
            country="ES",
            url="https://t.me/chollosvuelos",
            website_url=None,
            is_active=True,
            priority=8,
            description="Canal Telegram con ofertas de vuelos desde España.",
        ),
        dict(
            name="Milhas Aéreas Brasil",
            source_type="telegram",
            country="BR",
            url="https://t.me/milhasaereasbr",
            website_url=None,
            is_active=True,
            priority=8,
            description="Canal Telegram con promociones de milhas en Brasil.",
        ),
    ]

    for s in sources:
        exists = db.query(models.Source).filter_by(url=s["url"]).first()
        if not exists:
            obj = models.Source(**s)
            db.add(obj)

    db.commit()


def seed_spain_additions(db: Session):
    """Añade nuevas fuentes de España del documento de investigación (idempotente)"""

    # --- Nuevos programas de fidelidad ---
    new_programs = [
        dict(name="Más Renfe", currency="Puntos Renfe", country="ES", category="transport",
             avios_ratio=None,
             website_url="https://www.renfe.com/es/es/programa-mas-renfe",
             notes="Puntos por viajes Renfe y por gasolina vía Waylet/Repsol. Canjea por billetes AVE/Larga Distancia."),
        dict(name="Travel Club (Repsol)", currency="Puntos Travel Club", country="ES", category="fuel",
             avios_ratio=None,
             website_url="https://www.repsol.es/particulares/beneficios-clientes/tarjeta-repsol-travel/",
             notes="Programa integrado Repsol Travel. Puntos por gasolina, luz/gas, recarga eléctrica. Canjea por viajes, carburante, lavados."),
        dict(name="Revolut RevPoints ES", currency="RevPoints", country="ES", category="transfer",
             avios_ratio=None,
             website_url="https://www.revolut.com/es-ES/",
             notes="RevPoints transferibles a Iberia, Air Europa, Turkish y otras. Promos frecuentes. Fintech, no banco tradicional."),
    ]

    program_map = {}
    for p in new_programs:
        exists = db.query(models.LoyaltyProgram).filter_by(name=p["name"]).first()
        if not exists:
            obj = models.LoyaltyProgram(**p)
            db.add(obj)
            db.flush()
            program_map[p["name"]] = obj.id
        else:
            program_map[p["name"]] = exists.id

    # Corregir Vueling Club si tenía datos antiguos incorrectos
    vueling_existing = db.query(models.LoyaltyProgram).filter_by(name="Vueling Club").first()
    if vueling_existing and vueling_existing.currency != "Avios":
        vueling_existing.currency = "Avios"
        vueling_existing.avios_ratio = 1.0
        vueling_existing.notes = "Usa Avios como moneda. Acumula volando Vueling y con partners. Intercambiable con Iberia Club y BA."

    # También recuperar los ya existentes que necesitamos
    iberia = db.query(models.LoyaltyProgram).filter_by(name="Iberia Club").first()
    iberia_id = iberia.id if iberia else None
    travel_club = db.query(models.LoyaltyProgram).filter_by(name="Travel Club (Repsol)").first()
    travel_club_id = travel_club.id if travel_club else program_map.get("Travel Club (Repsol)")
    mas_renfe = db.query(models.LoyaltyProgram).filter_by(name="Más Renfe").first()
    mas_renfe_id = mas_renfe.id if mas_renfe else program_map.get("Más Renfe")
    vueling = db.query(models.LoyaltyProgram).filter_by(name="Vueling Club").first()
    vueling_id = vueling.id if vueling else program_map.get("Vueling Club")

    db.commit()

    # --- Nuevas oportunidades de acumulación España ---
    new_opportunities = [
        dict(
            name="Repsol Waylet + Travel Club",
            category="fuel",
            country="ES",
            loyalty_program_id=travel_club_id,
            earning_rate=1.0,
            earning_description="Puntos Travel Club por litro de gasolina, recarga eléctrica y luz/gas",
            how_to_use="Añade la tarjeta Repsol Travel en la app Waylet. Repostaje acumula Puntos Travel Club canjeables por viajes, carburante o lavados.",
            requirements="App Waylet + tarjeta Repsol Travel",
            signup_url="https://www.repsol.es/particulares/beneficios-clientes/tarjeta-repsol-travel/",
            notes="Cepsa GOW es competidor directo. Repsol Travel canjea también por viajes vía Travel Club.",
            is_active=True,
            recommendation_score=82,
        ),
        dict(
            name="Repsol Waylet + Más Renfe",
            category="fuel",
            country="ES",
            loyalty_program_id=mas_renfe_id,
            earning_rate=1.0,
            earning_description="Puntos Renfe por repostaje en Repsol con Waylet vinculado a Más Renfe",
            how_to_use="Vincula tu número Más Renfe dentro de la app Waylet. Cada repostaje suma Puntos Renfe (con límite mensual).",
            requirements="App Waylet + número Más Renfe",
            signup_url="https://www.renfe.com/es/es/programa-mas-renfe/partners/repsol",
            notes="Doble acumulación posible: Travel Club + Más Renfe en el mismo repostaje. Límites mensuales aplicables.",
            is_active=True,
            recommendation_score=75,
        ),
        dict(
            name="Club Moeve gow — Saldo por gasolina y partners",
            category="fuel",
            country="ES",
            loyalty_program_id=iberia_id,
            earning_rate=1.0,
            earning_description="Saldo (saldow) por repostaje, recargas, lavados y 40+ marcas colaboradoras",
            how_to_use="Regístrate en Club Moeve gow (antes Cepsa GOW). Usa la app en estaciones Moeve. Saldo canjeable por combustible, lavados o catálogo.",
            requirements="App Moeve",
            signup_url="https://www.moeve.es/es/particular",
            notes="Antes Cepsa GOW, ahora Club Moeve gow. Partners incluyen Amazon, eDreams, Europcar, MediaMarkt, Pangea, Sprinter. Saldo en euros, no puntos.",
            is_active=True,
            recommendation_score=78,
        ),
        dict(
            name="Club Avolta — Duty Free Aeropuertos → Avios",
            category="shopping_portal",
            country="ES",
            loyalty_program_id=iberia_id,
            earning_rate=1.0,
            earning_description="1 Avios por €/£ gastado en tiendas duty free de aeropuertos españoles y Heathrow",
            how_to_use="Descarga la app Club Avolta y vincula tu cuenta Iberia Club o BA. Escanea el QR al pagar en tiendas duty free participantes.",
            requirements="App Club Avolta + cuenta Iberia Club o BA Executive Club",
            signup_url="https://www.clubavolta.com/",
            notes="Promos frecuentes de doble Avios. Aplica en aeropuertos españoles y en Heathrow (relevante para GIB-LHR).",
            is_active=True,
            recommendation_score=80,
        ),
        dict(
            name="Vueling Club — Avios por vuelos domésticos",
            category="rideshare",
            country="ES",
            loyalty_program_id=vueling_id,
            earning_rate=1.0,
            earning_description="Avios por vuelos Vueling y compras con partners",
            how_to_use="Regístrate en Vueling Club. Indica tu número al comprar vuelos Vueling. Los Avios son intercambiables con Iberia Club y BA.",
            requirements="Cuenta Vueling Club (gratuita)",
            signup_url="https://www.vueling.com/es/vueling-club",
            notes="Misma moneda Avios que Iberia y BA. Útil para vuelos domésticos e intraeuropeos desde España.",
            is_active=True,
            recommendation_score=76,
        ),
    ]

    for o in new_opportunities:
        exists = db.query(models.EarningOpportunity).filter_by(name=o["name"]).first()
        if not exists:
            obj = models.EarningOpportunity(**o)
            db.add(obj)

    # --- Nuevas tarjetas España ---
    revolut_prog = db.query(models.LoyaltyProgram).filter_by(name="Revolut RevPoints ES").first()
    revolut_id = revolut_prog.id if revolut_prog else program_map.get("Revolut RevPoints ES")

    new_cards = [
        dict(
            name="Revolut Premium / Metal (RevPoints ES)",
            bank="Revolut",
            country="ES",
            card_network="Visa/Mastercard",
            loyalty_program_id=revolut_id,
            base_earning_rate=1.0,
            bonus_categories='{"travel": 3.0}',
            annual_fee=99.0,
            currency="EUR",
            first_year_fee=None,
            welcome_bonus=None,
            welcome_bonus_requirement=None,
            minimum_income=None,
            is_available=True,
            application_url="https://www.revolut.com/es-ES/",
            notes="RevPoints transferibles a Iberia, Air Europa, Turkish. Promos frecuentes. Sin comisiones en divisas. Buena opción fintech.",
            recommendation_score=72,
        ),
    ]

    for c in new_cards:
        exists = db.query(models.CreditCard).filter_by(name=c["name"]).first()
        if not exists:
            obj = models.CreditCard(**c)
            db.add(obj)

    db.commit()
    print("Spain additions seed complete.")


def seed_brazil_additions(db: Session):
    """Añade nuevas fuentes de Brasil del documento de investigación (idempotente)"""

    # --- Nuevos programas de fidelidad Brasil ---
    new_programs = [
        dict(name="Iupp Itaú", currency="Pontos Iupp", country="BR", category="transfer",
             avios_ratio=None,
             website_url="https://www.iupp.com.br/",
             notes="Programa de pontos del Itaú. Transfiere a Smiles, LATAM Pass, TudoAzul y otros. Similar a Livelo."),
        dict(name="LATAM Pass", currency="Milhas LATAM", country="BR", category="airline",
             avios_ratio=None,
             website_url="https://www.latamairlines.com/br/pt/latam-pass",
             notes="Programa de LATAM Airlines. Acepta transferencias desde Livelo, Iupp, Esfera, Km de Vantagens."),
        dict(name="TudoAzul", currency="Pontos TudoAzul", country="BR", category="airline",
             avios_ratio=None,
             website_url="https://www.tudoazul.com.br/",
             notes="Programa de Azul Airlines. Acepta Petrobras Premmia, Km de Vantagens, Livelo, Iupp."),
        dict(name="Petrobras Premmia", currency="Pontos Premmia", country="BR", category="fuel",
             avios_ratio=None,
             website_url="https://premmia.com.br/",
             notes="Pontos por gasolina en red Petrobras/BR. Posto premiado = doble puntos. Transfiere a TudoAzul."),
        dict(name="Km de Vantagens (Ipiranga)", currency="Km", country="BR", category="fuel",
             avios_ratio=None,
             website_url="https://www.kmsdevantagens.com.br/",
             notes="37M participantes. App abastece-aí. Transfiere km a LATAM Pass y TudoAzul (con coste en R$). Cashback también disponible."),
        dict(name="Shell Box", currency="Pontos Shell Box", country="BR", category="fuel",
             avios_ratio=None,
             website_url="https://www.shell.com.br/motoristas/shell-box.html",
             notes="Programa Shell. Conecta con Smiles, TudoAzul y LATAM según época. Doble dip: tarjeta + puntos posto."),
    ]

    program_map = {}
    for p in new_programs:
        exists = db.query(models.LoyaltyProgram).filter_by(name=p["name"]).first()
        if not exists:
            obj = models.LoyaltyProgram(**p)
            db.add(obj)
            db.flush()
            program_map[p["name"]] = obj.id
        else:
            program_map[p["name"]] = exists.id

    db.commit()

    # Recuperar IDs necesarios
    def get_id(name):
        prog = db.query(models.LoyaltyProgram).filter_by(name=name).first()
        return prog.id if prog else program_map.get(name)

    livelo_id = get_id("Livelo")
    esfera_id = get_id("Esfera Santander")
    iupp_id = get_id("Iupp Itaú")
    latam_id = get_id("LATAM Pass")
    tudoazul_id = get_id("TudoAzul")
    premmia_id = get_id("Petrobras Premmia")
    km_id = get_id("Km de Vantagens (Ipiranga)")
    shell_id = get_id("Shell Box")

    # --- Nuevas oportunidades de acumulación Brasil ---
    new_opportunities = [
        dict(
            name="Petrobras Premmia → TudoAzul",
            category="fuel",
            country="BR",
            loyalty_program_id=premmia_id,
            earning_rate=1.0,
            earning_description="Pontos Premmia por real gastado en gasolina BR/Petrobras. Posto premiado = doble pontos.",
            how_to_use="Regístrate en Premmia. Acumula en postos Petrobras/BR. Transfiere pontos a TudoAzul (Azul Airlines).",
            requirements="Cuenta Premmia (gratuita) + CPF",
            signup_url="https://premmia.com.br/",
            notes="Elegir 'posto premiado' duplica los puntos. TudoAzul es el destino de transferencia principal.",
            is_active=True,
            recommendation_score=82,
        ),
        dict(
            name="Km de Vantagens (Ipiranga) → LATAM/TudoAzul",
            category="fuel",
            country="BR",
            loyalty_program_id=km_id,
            earning_rate=1.0,
            earning_description="Km por real gastado en postos Ipiranga + cashback. Transfiere a LATAM Pass o TudoAzul.",
            how_to_use="Descarga la app abastece-aí de Ipiranga. Registra el repostaje. Transfiere km a aerolíneas (coste en R$).",
            requirements="App abastece-aí + CPF",
            signup_url="https://www.kmsdevantagens.com.br/",
            notes="37M participantes. Transferencia a millas tiene coste en reales. También ofrece cashback directo.",
            is_active=True,
            recommendation_score=78,
        ),
        dict(
            name="Shell Box → Smiles/TudoAzul/LATAM",
            category="fuel",
            country="BR",
            loyalty_program_id=shell_id,
            earning_rate=1.0,
            earning_description="Pontos Shell Box por litro en postos Shell, transferibles a programas aéreos",
            how_to_use="Usa la app Shell Box al repostar. Acumula pontos y transfiere a Smiles, TudoAzul o LATAM según promos activas.",
            requirements="App Shell Box + CPF",
            signup_url="https://www.shell.com.br/motoristas/shell-box.html",
            notes="Partnerships con aerolíneas varían por época. Verificar promos activas antes de transferir.",
            is_active=True,
            recommendation_score=75,
        ),
        dict(
            name="Iupp Itaú Marketplace → Smiles/LATAM/TudoAzul",
            category="shopping_portal",
            country="BR",
            loyalty_program_id=iupp_id,
            earning_rate=2.0,
            earning_description="Pontos Iupp por compras en marketplace + campañas de 10x pontos",
            how_to_use="Accede al marketplace de Iupp o compra con tarjeta Itaú. Transfiere pontos a Smiles, LATAM Pass o TudoAzul.",
            requirements="Cuenta Itaú + CPF",
            signup_url="https://www.iupp.com.br/",
            notes="Campañas frecuentes de pontos em dobro o 10x. Transferir en bonificación maximiza el valor.",
            is_active=True,
            recommendation_score=83,
        ),
        dict(
            name="Livelo Marketplace — Campañas bonificadas",
            category="shopping_portal",
            country="BR",
            loyalty_program_id=livelo_id,
            earning_rate=5.0,
            earning_description="5-10x pontos Livelo en compras online (electrónica, moda, viajes)",
            how_to_use="Accede al shopping de Livelo. Compra en tiendas partner. Transfiere a LATAM, Smiles u otras aerolíneas con bonus.",
            requirements="Cuenta Livelo + CPF",
            signup_url="https://www.livelo.com.br/ganhe-pontos/shopping",
            notes="Campañas de '10x pontos' son frecuentes. Combina con bonos de transferencia para máximo valor.",
            is_active=True,
            recommendation_score=88,
        ),
    ]

    for o in new_opportunities:
        exists = db.query(models.EarningOpportunity).filter_by(name=o["name"]).first()
        if not exists:
            obj = models.EarningOpportunity(**o)
            db.add(obj)

    # --- Nuevas tarjetas Brasil ---
    new_cards = [
        dict(
            name="Itaú Personnalité Mastercard Black",
            bank="Itaú",
            country="BR",
            card_network="Mastercard",
            loyalty_program_id=iupp_id,
            base_earning_rate=2.5,
            bonus_categories='{"travel": 3.5, "restaurants": 3.0}',
            annual_fee=1200.0,
            currency="BRL",
            first_year_fee=None,
            welcome_bonus=None,
            welcome_bonus_requirement=None,
            minimum_income=None,
            is_available=True,
            application_url="https://www.itau.com.br/cartoes/personnalite/",
            notes="Acumula Iupp. Transfiere a Smiles, LATAM, TudoAzul. Necesita cuenta Personnalité.",
            recommendation_score=82,
        ),
        dict(
            name="Nubank Ultravioleta (Livelo)",
            bank="Nubank",
            country="BR",
            card_network="Mastercard",
            loyalty_program_id=livelo_id,
            base_earning_rate=1.0,
            bonus_categories='{"all": 1.0}',
            annual_fee=588.0,
            currency="BRL",
            first_year_fee=None,
            welcome_bonus=None,
            welcome_bonus_requirement=None,
            minimum_income=None,
            is_available=True,
            application_url="https://nubank.com.br/cartao/ultravioleta/",
            notes="1% cashback o acumula Livelo. Fintech accesible. Sin burocracia de banco tradicional.",
            recommendation_score=75,
        ),
    ]

    for c in new_cards:
        exists = db.query(models.CreditCard).filter_by(name=c["name"]).first()
        if not exists:
            obj = models.CreditCard(**c)
            db.add(obj)

    db.commit()
    print("Brazil additions seed complete.")


def seed_uk_gibraltar_additions(db: Session):
    """Añade nuevas fuentes de UK/Gibraltar del documento de investigación (idempotente)"""

    # --- Nuevos programas de fidelidad UK/GIB ---
    new_programs = [
        dict(name="BPme Rewards", currency="BPme Points", country="GI", category="fuel",
             avios_ratio=None,
             website_url="https://www.bp.com/en_gb/united-kingdom/home/products-and-services/bpme-rewards.html",
             notes="Mejor programa de gasolinera UK para Air Miles. 1-2 puntos/litro → Avios. 'Best for Air Miles' según comparativas."),
        dict(name="Nectar (Sainsbury's/Esso)", currency="Nectar Points", country="GI", category="supermarket",
             avios_ratio=None,
             website_url="https://www.nectar.com/",
             notes="400 Nectar = 250 Avios (Iberia o BA). Conversión automática posible. Acumula en Sainsbury's y estaciones Esso."),
        dict(name="Tesco Clubcard", currency="Clubcard Points", country="GI", category="supermarket",
             avios_ratio=None,
             website_url="https://www.tesco.com/clubcard/",
             notes="Puntos por compras Tesco y gasolina (Esso con Tesco Express). Ya no convierte a Avios directamente; valor vía partners Boost."),
        dict(name="Heathrow Rewards", currency="Heathrow Points", country="GI", category="airport",
             avios_ratio=None,
             website_url="https://www.heathrow.com/rewards",
             notes="1 punto por £1 en tiendas/bares/parking Heathrow, 1 punto por £10 en casa de cambio. Convierte a Avios (Iberia o BA)."),
        dict(name="American Express Membership Rewards UK", currency="MR Points UK", country="GI", category="transfer",
             avios_ratio=1.0,
             website_url="https://www.americanexpress.com/en-gb/rewards/membership-rewards/",
             notes="Puntos transferibles a BA, Iberia y otros. 'Livelo británico'. Tarjetas Gold/Platinum UK."),
    ]

    program_map = {}
    for p in new_programs:
        exists = db.query(models.LoyaltyProgram).filter_by(name=p["name"]).first()
        if not exists:
            obj = models.LoyaltyProgram(**p)
            db.add(obj)
            db.flush()
            program_map[p["name"]] = obj.id
        else:
            program_map[p["name"]] = exists.id

    db.commit()

    def get_id(name):
        prog = db.query(models.LoyaltyProgram).filter_by(name=name).first()
        return prog.id if prog else program_map.get(name)

    ba_id = get_id("British Airways Executive Club")
    bpme_id = get_id("BPme Rewards")
    nectar_id = get_id("Nectar (Sainsbury's/Esso)")
    tesco_id = get_id("Tesco Clubcard")
    heathrow_id = get_id("Heathrow Rewards")
    amex_uk_id = get_id("American Express Membership Rewards UK")

    # --- Nuevas oportunidades UK/GIB ---
    new_opportunities = [
        dict(
            name="BP BPme Rewards → Avios (UK/GIB)",
            category="fuel",
            country="GI",
            loyalty_program_id=bpme_id,
            earning_rate=1.5,
            earning_description="1 punto/litro gasolina normal, 2 puntos/litro Ultimate, 1 punto/£1 en tienda → Avios",
            how_to_use="Descarga la app BPme. Escanea al repostar en estaciones BP. Convierte BPme points a Avios desde la app.",
            requirements="App BPme (gratuita)",
            signup_url="https://www.bp.com/en_gb/united-kingdom/home/products-and-services/bpme-rewards.html",
            notes="Destacado como 'Best for Air Miles' en comparativas UK 2025. Aplica en Gibraltar si hay BP.",
            is_active=True,
            recommendation_score=88,
        ),
        dict(
            name="Sainsbury's + Esso Nectar → Avios (UK/GIB)",
            category="supermarket",
            country="GI",
            loyalty_program_id=nectar_id,
            earning_rate=1.0,
            earning_description="1 punto Nectar/litro en Esso + puntos por compras en Sainsbury's → 400 Nectar = 250 Avios",
            how_to_use="Registra tu tarjeta Nectar en Sainsbury's/Esso. Activa la conversión automática a Avios en la app Nectar.",
            requirements="Tarjeta Nectar (gratuita) + cuenta BA o Iberia Club",
            signup_url="https://www.nectar.com/",
            notes="400 Nectar = 250 Avios. Conversión automática activable. Fuente muy directa de Avios en UK.",
            is_active=True,
            recommendation_score=85,
        ),
        dict(
            name="Tesco Clubcard — Puntos por súper y gasolina (UK)",
            category="supermarket",
            country="GI",
            loyalty_program_id=tesco_id,
            earning_rate=0.5,
            earning_description="1 punto Clubcard por £2 de gasolina + puntos por compras Tesco",
            how_to_use="Usa la tarjeta/app Tesco Clubcard al comprar en Tesco o repostar en Esso con Tesco Express. Usa los puntos vía partners Boost.",
            requirements="Tesco Clubcard (gratuita)",
            signup_url="https://www.tesco.com/clubcard/",
            notes="Ya no convierte a Avios directamente. Sigue siendo valiosa vía partners Boost (viajes, restaurantes).",
            is_active=True,
            recommendation_score=72,
        ),
        dict(
            name="Heathrow Rewards → Avios (tránsito LHR)",
            category="shopping_portal",
            country="GI",
            loyalty_program_id=heathrow_id,
            earning_rate=1.0,
            earning_description="1 punto por £1 en tiendas/bares/parking Heathrow; convierte a Avios Iberia o BA",
            how_to_use="Regístrate en Heathrow Rewards. Escanea al comprar en tiendas y restaurantes del aeropuerto. Convierte puntos a Avios.",
            requirements="Cuenta Heathrow Rewards (gratuita)",
            signup_url="https://www.heathrow.com/rewards",
            notes="Muy relevante para conexiones GIB-LHR. También 1 punto por £10 en casa de cambio.",
            is_active=True,
            recommendation_score=80,
        ),
        dict(
            name="BA Avios eStore — Portal compras UK → Avios",
            category="shopping_portal",
            country="GI",
            loyalty_program_id=ba_id,
            earning_rate=2.0,
            earning_description="Avios por £ gastada en cientos de tiendas UK/online",
            how_to_use="Accede a shopping.ba.com antes de comprar en tiendas participantes (tecnología, moda, viajes, etc.).",
            requirements="Cuenta BA Executive Club",
            signup_url="https://shopping.ba.com/",
            notes="Equivalente británico de Iberia Plus Store. Varía por tienda (1-10+ Avios/£).",
            is_active=True,
            recommendation_score=82,
        ),
    ]

    for o in new_opportunities:
        exists = db.query(models.EarningOpportunity).filter_by(name=o["name"]).first()
        if not exists:
            obj = models.EarningOpportunity(**o)
            db.add(obj)

    # --- Nuevas tarjetas UK/GIB ---
    new_cards = [
        dict(
            name="BA Amex Premium Plus (UK)",
            bank="American Express UK",
            country="GI",
            card_network="Amex",
            loyalty_program_id=ba_id,
            base_earning_rate=1.5,
            bonus_categories='{"ba_flights": 3.0}',
            annual_fee=250.0,
            currency="GBP",
            first_year_fee=None,
            welcome_bonus=25000,
            welcome_bonus_requirement="Gasta £3.000 en los primeros 3 meses",
            minimum_income=None,
            is_available=True,
            application_url="https://www.americanexpress.com/en-gb/credit-cards/british-airways-american-express-premium-plus-card/",
            notes="Mejor tarjeta BA UK. 1.5 Avios/£ base, 3 Avios/£ en BA. 2-4-1 voucher con £10k gasto/año. Necesita dirección UK.",
            recommendation_score=88,
        ),
        dict(
            name="Barclaycard Avios Plus (UK)",
            bank="Barclaycard",
            country="GI",
            card_network="Visa",
            loyalty_program_id=ba_id,
            base_earning_rate=1.5,
            bonus_categories=None,
            annual_fee=20.0,
            currency="GBP",
            first_year_fee=None,
            welcome_bonus=5000,
            welcome_bonus_requirement="Gasta £1.000 en los primeros 3 meses",
            minimum_income=None,
            is_available=True,
            application_url="https://www.barclaycard.co.uk/personal/credit-cards/avios/",
            notes="1.5 Avios/£. Alternativa a BA Amex. Necesita dirección UK.",
            recommendation_score=78,
        ),
        dict(
            name="Amex Gold UK (Membership Rewards UK)",
            bank="American Express UK",
            country="GI",
            card_network="Amex",
            loyalty_program_id=amex_uk_id,
            base_earning_rate=1.0,
            bonus_categories='{"travel": 2.0, "restaurants": 2.0}',
            annual_fee=0.0,
            currency="GBP",
            first_year_fee=0.0,
            welcome_bonus=20000,
            welcome_bonus_requirement="Gasta £3.000 en los primeros 3 meses",
            minimum_income=None,
            is_available=True,
            application_url="https://www.americanexpress.com/en-gb/credit-cards/gold-card/",
            notes="MR UK transferibles a BA y otros. Primer año gratis. Necesita dirección UK.",
            recommendation_score=80,
        ),
    ]

    for c in new_cards:
        exists = db.query(models.CreditCard).filter_by(name=c["name"]).first()
        if not exists:
            obj = models.CreditCard(**c)
            db.add(obj)

    db.commit()
    print("UK/Gibraltar additions seed complete.")


def seed_remaining_additions(db: Session):
    """Añade fuentes restantes: Qatar, gasolineras menores ES y UK (idempotente)"""

    def get_id(name):
        prog = db.query(models.LoyaltyProgram).filter_by(name=name).first()
        return prog.id if prog else None

    # --- Qatar Privilege Club ---
    if not db.query(models.LoyaltyProgram).filter_by(name="Qatar Airways Privilege Club").first():
        qatar = models.LoyaltyProgram(
            name="Qatar Airways Privilege Club",
            currency="Avios",
            country="GI",
            category="airline",
            avios_ratio=1.0,
            website_url="https://www.qatarairways.com/en/privilege-club.html",
            notes="Usa Avios como moneda (unificación IAG). Acumula volando Qatar + OneWorld. Accesible desde UK/GIB y España. Canjea en BA, Iberia, Vueling.",
        )
        db.add(qatar)
        db.flush()
        qatar_id = qatar.id
    else:
        qatar_id = get_id("Qatar Airways Privilege Club")

    db.commit()

    iberia_id = get_id("Iberia Club")
    ba_id = get_id("British Airways Executive Club")

    # Earning opportunity Qatar
    if not db.query(models.EarningOpportunity).filter_by(name="Qatar Privilege Club — Avios por vuelos OneWorld").first():
        db.add(models.EarningOpportunity(
            name="Qatar Privilege Club — Avios por vuelos OneWorld",
            category="rideshare",
            country="GI",
            loyalty_program_id=qatar_id,
            earning_rate=1.0,
            earning_description="Avios por vuelos Qatar Airways y aerolíneas OneWorld",
            how_to_use="Regístrate en Qatar Privilege Club. Al volar Qatar o cualquier aerolínea OneWorld, indica tu número para acumular Avios intercambiables con BA/Iberia.",
            requirements="Cuenta Qatar Privilege Club (gratuita)",
            signup_url="https://www.qatarairways.com/en/privilege-club/enroll.html",
            notes="Avios unificados IAG. Útil para vuelos Qatar desde LHR o MAD. Canjeable en BA, Iberia y Vueling.",
            is_active=True,
            recommendation_score=78,
        ))

    # --- Gasolineras menores España (valor indirecto) ---
    spain_minor_fuel = [
        dict(
            name="Naftë — Puntos por repostaje",
            category="fuel",
            country="ES",
            loyalty_program_id=None,
            earning_rate=1.0,
            earning_description="1 punto por litro de combustible, canjeable por regalos o lavados",
            how_to_use="Solicita la tarjeta Naftë en la gasolinera. Acumula puntos en cada repostaje. Canjea por regalos del catálogo.",
            requirements="Tarjeta Naftë",
            signup_url="https://www.nafte.es/",
            notes="Valor indirecto: no convierte a Avios/millas. Útil como ahorro complementario en gasolina.",
            is_active=True,
            recommendation_score=45,
        ),
        dict(
            name="Gasoprix — Puntos por repostaje",
            category="fuel",
            country="ES",
            loyalty_program_id=None,
            earning_rate=1.0,
            earning_description="1 punto por litro, canjeable por regalos o lavados",
            how_to_use="Regístrate en el programa Gasoprix. Acumula puntos en cada visita.",
            requirements="Tarjeta Gasoprix",
            signup_url="https://www.gasoprix.com/programa-puntos/",
            notes="Valor indirecto: no convierte a Avios. Descuentos y catálogo propio. Útil si usas Gasoprix habitualmente.",
            is_active=True,
            recommendation_score=40,
        ),
    ]

    for o in spain_minor_fuel:
        if not db.query(models.EarningOpportunity).filter_by(name=o["name"]).first():
            db.add(models.EarningOpportunity(**o))

    # --- Gasolineras menores UK (valor indirecto, sin Avios directos) ---
    uk_minor_fuel = [
        dict(
            name="Morrisons More — Puntos por compras y gasolina (UK)",
            category="fuel",
            country="GI",
            loyalty_program_id=None,
            earning_rate=1.0,
            earning_description="Puntos More por compras en Morrisons y gasolineras Morrisons",
            how_to_use="Usa la app/tarjeta Morrisons More al comprar. Canjea puntos por vales de descuento en Morrisons.",
            requirements="App Morrisons More (gratuita)",
            signup_url="https://my.morrisons.com/more-card/",
            notes="No convierte a Avios directamente. Valor en descuentos supermercado. Útil si compras en Morrisons UK.",
            is_active=True,
            recommendation_score=42,
        ),
        dict(
            name="Texaco Star Rewards — Puntos por gasolina (UK)",
            category="fuel",
            country="GI",
            loyalty_program_id=None,
            earning_rate=1.0,
            earning_description="1 punto por litro (valor 1p), doble puntos en primeros repostajes + bonus bienvenida",
            how_to_use="Regístrate en Texaco Star Rewards. Escanea en cada repostaje. Canjea por vales.",
            requirements="App Texaco Star Rewards (gratuita)",
            signup_url="https://www.texaco.co.uk/star-rewards",
            notes="No convierte a Avios. Buen bono de bienvenida. Útil si hay Texaco cerca en UK/GIB.",
            is_active=True,
            recommendation_score=43,
        ),
        dict(
            name="ASDA Rewards — Cashback por compras y gasolina (UK)",
            category="fuel",
            country="GI",
            loyalty_program_id=None,
            earning_rate=1.0,
            earning_description="Cashback en 'Cashpot' por compras ASDA y repostaje en gasolineras ASDA",
            how_to_use="Usa la app ASDA Rewards al comprar. El cashback se acumula en tu Cashpot y se aplica en la próxima compra.",
            requirements="App ASDA Rewards (gratuita)",
            signup_url="https://www.asda.com/cashpot",
            notes="Cashback directo, no millas. Útil como ahorro si compras en ASDA. No convierte a Avios.",
            is_active=True,
            recommendation_score=44,
        ),
        dict(
            name="Valero SaveUp — Puntos por gasolina (UK)",
            category="fuel",
            country="GI",
            loyalty_program_id=None,
            earning_rate=1.0,
            earning_description="Puntos SaveUp por litro en estaciones Valero/Texas",
            how_to_use="Regístrate en SaveUp. Escanea al repostar en estaciones Valero participantes.",
            requirements="App SaveUp (gratuita)",
            signup_url="https://www.valero.co.uk/",
            notes="No convierte a Avios. Valor en descuentos. Baja prioridad salvo que sea tu gasolinera habitual en UK.",
            is_active=True,
            recommendation_score=38,
        ),
    ]

    for o in uk_minor_fuel:
        if not db.query(models.EarningOpportunity).filter_by(name=o["name"]).first():
            db.add(models.EarningOpportunity(**o))

    db.commit()
    print("Remaining additions seed complete.")


def run_seed(db: Session):
    """Ejecuta el seed completo si la BD está vacía"""
    # Solo ejecutar si no hay programas (evita duplicados)
    count = db.query(models.LoyaltyProgram).count()
    if count == 0:
        print("Seeding database with initial data...")
        program_map = seed_loyalty_programs(db)
        seed_credit_cards(db, program_map)
        seed_earning_opportunities(db, program_map)
        seed_sources(db)
        print(f"Seed complete: {len(program_map)} programs, cards, opportunities, and sources added.")

    # Siempre ejecutar actualizaciones incrementales (idempotente)
    seed_spain_additions(db)
    seed_brazil_additions(db)
    seed_uk_gibraltar_additions(db)
    seed_remaining_additions(db)
    seed_full_v2(db)
    seed_full_v3(db)
    seed_fix_broken_data(db)
    return True


def seed_full_v2(db):
    def get_prog(name):
        p = db.query(models.LoyaltyProgram).filter_by(name=name).first()
        return p.id if p else None
    new_programs = [
        dict(name='Finnair Plus', currency='Avios', country='INT',
             category='airline', avios_ratio=1.0,
             website_url='https://www.finnair.com/finnairplus',
             notes='Programa Finnair, oneworld. Avios unificados IAG. Sweet spot para vuelos a Asia via Helsinki.'),
        dict(name='Aer Lingus AerClub', currency='Avios', country='INT',
             category='airline', avios_ratio=1.0,
             website_url='https://www.aerlingus.com/aerclub',
             notes='Programa IAG. Avios unificados. Transatlantico economico desde Europa.'),
        dict(name='Air Europa SUMA', currency='Millas SUMA', country='ES',
             category='airline', avios_ratio=None,
             website_url='https://www.aireuropa.com/suma',
             notes='SkyTeam. Vuela MAD-GRU directo. Alternativa a Iberia para Brasil desde Madrid.'),
        dict(name='Flying Blue (AF/KLM)', currency='Miles Flying Blue', country='INT',
             category='airline', avios_ratio=None,
             website_url='https://www.flyingblue.com',
             notes='SkyTeam. Promo Rewards mensuales hasta 50% descuento en millas. Economy desde 15.000 millas Europa.'),
        dict(name='Virgin Atlantic Flying Club', currency='Virgin Points', country='INT',
             category='airline', avios_ratio=None,
             website_url='https://www.virginatlantic.com/flyingclub',
             notes='Permite reservar metal Delta. Delta One a USA por ~50.000 puntos. Sin fuel surcharges en Delta.'),
        dict(name='Turkish Miles & Smiles', currency='Miles', country='INT',
             category='airline', avios_ratio=None,
             website_url='https://www.turkishairlines.com/milesandsmiles',
             notes='Star Alliance. Sin fuel surcharges en Lufthansa/SWISS. Round-the-world, Lufthansa First Class.'),
        dict(name='Air Canada Aeroplan', currency='Aeroplan Points', country='INT',
             category='airline', avios_ratio=None,
             website_url='https://www.aircanada.com/aeroplan',
             notes='Star Alliance. Sin fuel surcharges. Family pooling. Stopovers y mixed-cabin awards.'),
        dict(name='TAP Miles&Go', currency='Miles TAP', country='INT',
             category='airline', avios_ratio=None,
             website_url='https://www.flytap.com/milesandgo',
             notes='Star Alliance. El usuario ya lo tiene activo. Vuelos Lisboa-Brasil. Lifetime status disponible.'),
        dict(name='IHG One Rewards', currency='IHG Points', country='INT',
             category='hotel', avios_ratio=None,
             website_url='https://www.ihg.com/onerewards',
             notes='Ratio ~5:1 a Avios. InterContinental, Holiday Inn, Hotel Indigo. Buena presencia Espana/Brasil.'),
        dict(name='Hilton Honors', currency='Hilton Points', country='INT',
             category='hotel', avios_ratio=None,
             website_url='https://www.hilton.com/honors',
             notes='Ratio 10:1 via BA Avios. Mejor en USA/UK que Espana. Util para viajes a USA/Asia.'),
    ]
    for prog_data in new_programs:
        if not db.query(models.LoyaltyProgram).filter_by(name=prog_data['name']).first():
            db.add(models.LoyaltyProgram(**prog_data))
    db.commit()
    iberia_id = get_prog('Iberia Club')
    ba_id = get_prog('British Airways Executive Club')
    vueling_id = get_prog('Vueling Club')
    new_cards = [
        dict(name='Santander Iberia Club Visa', bank='Santander Espana', country='ES', card_network='Visa',
             loyalty_program_id=iberia_id, base_earning_rate=0.5, bonus_categories=None,
             annual_fee=48.0, currency='EUR', first_year_fee=None,
             welcome_bonus=None, welcome_bonus_requirement='Tras gastar 700 EUR',
             minimum_income=None, is_available=True, application_url='https://www.bancosantander.es/particulares/tarjetas/credito/plan-iberia-plus',
             notes='1 Avios/2 EUR + 100 Avios/mes por domiciliar nomina + 100 Avios/mes por recibos. 10% dto en iberia.com. 4 EUR/mes.', recommendation_score=65),
        dict(name='BBVA Iberia Icon Visa', bank='BBVA', country='ES', card_network='Visa',
             loyalty_program_id=iberia_id, base_earning_rate=0.33, bonus_categories=None,
             annual_fee=0.0, currency='EUR', first_year_fee=0.0,
             welcome_bonus=9000, welcome_bonus_requirement='Condiciones BBVA',
             minimum_income=None, is_available=True, application_url='https://www.bbva.es/personas/productos/tarjetas/iberia-icon.html',
             notes='1 Avios/3 EUR. 9.000 Avios bienvenida. 10% descuento en iberia.com. Sin cuota anual.', recommendation_score=60),
        dict(name='Visa Iberia Zenit', bank='CaixaBank', country='ES', card_network='Visa',
             loyalty_program_id=iberia_id, base_earning_rate=3.0, bonus_categories='{"iberia": 5.0}',
             annual_fee=948.0, currency='EUR', first_year_fee=None,
             welcome_bonus=40000, welcome_bonus_requirement='Escalonado segun gasto',
             minimum_income=None, is_available=False, application_url='https://www.iberia.com/es/iberia-plus/tarjeta-zenit/',
             notes='Solo por invitacion. 3 Avios/EUR general, 5 Avios/EUR en Iberia. Status Oro automatico. La mejor tarjeta Iberia si tienes acceso.', recommendation_score=95),
        dict(name='NatWest International Reward Black (GIB)', bank='NatWest International', country='GI', card_network='Visa',
             loyalty_program_id=ba_id, base_earning_rate=0.5, bonus_categories='{"supermarkets": 1.0}',
             annual_fee=336.0, currency='GBP', first_year_fee=None,
             welcome_bonus=None, welcome_bonus_requirement=None,
             minimum_income=None, is_available=True, application_url='https://www.natwestinternational.com/',
             notes='Cashback convertible a BA Avios o Emirates. 0% FX fees. Potencialmente accesible desde Gibraltar. Verificar disponibilidad.', recommendation_score=68),
        dict(name='BRB DUX Visa Infinite', bank='BRB', country='BR', card_network='Visa',
             loyalty_program_id=None, base_earning_rate=5.0, bonus_categories='{"international": 7.0}',
             annual_fee=1080.0, currency='BRL', first_year_fee=None,
             welcome_bonus=None, welcome_bonus_requirement=None,
             minimum_income=None, is_available=True, application_url='https://www.brb.com.br/',
             notes='5 pts/R$1 nacional, 7 pts/R$1 internacional. Transfiere a Smiles, LATAM, TudoAzul. Requiere cuenta BRB.', recommendation_score=80),
        dict(name='Bradesco Aeternum Visa Infinite', bank='Bradesco', country='BR', card_network='Visa',
             loyalty_program_id=None, base_earning_rate=4.0, bonus_categories='{"international": 6.0}',
             annual_fee=1440.0, currency='BRL', first_year_fee=None,
             welcome_bonus=None, welcome_bonus_requirement=None,
             minimum_income=None, is_available=True, application_url='https://banco.bradesco/html/classic/produtos-servicos/cartoes/cartoes-credito/aeternum.shtm',
             notes='4 pts/R$1 nacional, 4-6 pts/R$1 internacional -> Livelo. Alta cuota pero excelente earning.', recommendation_score=78),
    ]
    for card_data in new_cards:
        if not db.query(models.CreditCard).filter_by(name=card_data['name']).first():
            db.add(models.CreditCard(**card_data))
    new_opportunities = [
        dict(name='Booking.com -> Avios via Iberia Partner', category='hotels', country='ES',
             loyalty_program_id=iberia_id, earning_rate=1.0,
             earning_description='1 Avios por EUR gastado en reservas Booking.com',
             how_to_use='Accede a Booking.com a traves del portal Iberia Plus Store o vincula tu cuenta Iberia Club.',
             requirements='Cuenta Iberia Club', signup_url='https://www.iberia.com/es/iberia-plus/shopping/',
             notes='Partner directo de Iberia Club. Acumula Avios en reservas de hotel.', is_active=True, recommendation_score=75),
        dict(name='Avis/Budget -> Avios por alquiler de coche', category='rideshare', country='ES',
             loyalty_program_id=iberia_id, earning_rate=1.0,
             earning_description='Avios por alquiler de coche con Avis o Budget',
             how_to_use='Al reservar con Avis o Budget, indica tu numero Iberia Club para acumular Avios.',
             requirements='Cuenta Iberia Club', signup_url='https://www.iberia.com/es/iberia-plus/partners/',
             notes='Partner directo. Util en viajes por Espana, Brasil y UK.', is_active=True, recommendation_score=70),
        dict(name='Vueling Club eStore - Portal compras Vueling', category='shopping_portal', country='ES',
             loyalty_program_id=vueling_id, earning_rate=2.0,
             earning_description='Avios por compras online en 100+ tiendas via portal Vueling',
             how_to_use='Accede al eStore de Vueling Club antes de comprar en tiendas participantes.',
             requirements='Cuenta Vueling Club', signup_url='https://www.vueling.com/es/vueling-club/gana-puntos/compras-online',
             notes='Distinto del Iberia Plus Store aunque comparten moneda Avios. Complementario.', is_active=True, recommendation_score=72),
        dict(name='Gib Oil GO Card - Combustible Gibraltar', category='fuel', country='GI',
             loyalty_program_id=None, earning_rate=1.0,
             earning_description='Puntos GO Card por litro de combustible en Gib Oil',
             how_to_use='Solicita la GO Card en las gasolineras Gib Oil de Gibraltar.',
             requirements='GO Card (gratuita)', signup_url='https://www.giboil.com/',
             notes='Programa local Gibraltar. No convierte a Avios pero es util dado que Gibraltar tiene combustible mas barato.', is_active=True, recommendation_score=45),
        dict(name='Compra directa de Avios - Iberia (hasta 50% bonus)', category='shopping_portal', country='ES',
             loyalty_program_id=iberia_id, earning_rate=1.5,
             earning_description='Compra Avios con hasta 50% bonus en promociones Iberia',
             how_to_use='En promociones periodicas, Iberia ofrece hasta 50% bonus en compra de Avios.',
             requirements='Cuenta Iberia Club', signup_url='https://www.iberia.com/es/iberia-plus/comprar-avios/',
             notes='Con 50% bonus: coste ~1,54 ctvs/Avios. Qatar ofrece hasta 45% bonus. BA tiene Avios Booster.', is_active=True, recommendation_score=82),
    ]
    for opp_data in new_opportunities:
        if not db.query(models.EarningOpportunity).filter_by(name=opp_data['name']).first():
            db.add(models.EarningOpportunity(**opp_data))
    new_sources = [
        dict(name='Viajero Millero', source_type='rss_feed', country='ES',
             url='https://www.viajeromillero.com/feed/', website_url='https://www.viajeromillero.com',
             is_active=True, priority=8, description='Blog espanol de viajero frecuente. Estrategias y analisis de programas.'),
        dict(name='Guia Low Cost', source_type='rss_feed', country='ES',
             url='https://www.guialowcost.es/feed/', website_url='https://www.guialowcost.es',
             is_active=True, priority=7, description='Deals de viaje y guias Iberia Plus en espanol.'),
        dict(name='Modo Avion', source_type='rss_feed', country='ES',
             url='https://modoavion.com/feed/', website_url='https://modoavion.com',
             is_active=True, priority=7, description='Educacion sobre millas y puntos en espanol.'),
        dict(name='Proyecto Millas', source_type='rss_feed', country='ES',
             url='https://proyectomillas.com/feed/', website_url='https://proyectomillas.com',
             is_active=True, priority=7, description='Comunidad espanola de viajes con millas.'),
        dict(name='Melhores Destinos', source_type='rss_feed', country='BR',
             url='https://www.melhoresdestinos.com.br/feed', website_url='https://www.melhoresdestinos.com.br',
             is_active=True, priority=10, description='Lider absoluto Brasil. Deals, millas, error fares. Lectura diaria obligatoria.'),
        dict(name='Pontos pra Voar', source_type='rss_feed', country='BR',
             url='https://pontospravoar.com/feed/', website_url='https://pontospravoar.com',
             is_active=True, priority=9, description='Alertas rapidas de promos brasilenas. Telegram/WhatsApp activos.'),
        dict(name='Turning Left for Less', source_type='rss_feed', country='INT',
             url='https://www.turningleftforless.com/feed/', website_url='https://www.turningleftforless.com',
             is_active=True, priority=8, description='BA/Iberia Avios y viajes premium europeos. Muy relevante para estrategia Avios.'),
        dict(name='One Mile at a Time', source_type='rss_feed', country='INT',
             url='https://onemileatatime.com/feed/', website_url='https://onemileatatime.com',
             is_active=True, priority=8, description='Guias detalladas de Iberia, BA y premium travel. Referencia mundial.'),
        dict(name='Frequent Miler', source_type='rss_feed', country='INT',
             url='https://frequentmiler.com/feed/', website_url='https://frequentmiler.com',
             is_active=True, priority=7, description='Guia completa de los 7 programas Avios y maximizacion de puntos.'),
        dict(name='PromoPassagens', source_type='telegram', country='BR',
             url='https://t.me/promopassagens', website_url=None,
             is_active=True, priority=9, description='Canal Telegram con promociones de pasajes Brasil.'),
        dict(name='BECO News', source_type='telegram', country='BR',
             url='https://t.me/beconews', website_url=None,
             is_active=True, priority=8, description='Noticias de millas y promociones Brasil.'),
        dict(name='Barbadas pelo Mundo', source_type='telegram', country='BR',
             url='https://t.me/barbadasnomundo', website_url=None,
             is_active=True, priority=9, description='Alertas de error fares y ofertas excepcionales Brasil.'),
        dict(name='Estevam Pelo Mundo - Alerta Promos', source_type='telegram', country='BR',
             url='https://t.me/estevampelomundo', website_url=None,
             is_active=True, priority=8, description='Canal Telegram alertas de promos brasilenas de Estevam Pelo Mundo.'),
    ]
    for src_data in new_sources:
        if not db.query(models.Source).filter_by(url=src_data['url']).first():
            db.add(models.Source(**src_data))
    db.commit()
    print('Full v2 seed complete.')


def seed_full_v3(db):
    """v3: Add earning opportunities for all planner categories (supermarkets, restaurants, hotels, rideshare)"""
    def get_prog(name):
        p = db.query(models.LoyaltyProgram).filter_by(name=name).first()
        return p.id if p else None

    # === New loyalty programs for stores ===
    new_programs = [
        dict(name='El Corte Inglés Club', currency='Puntos ECI', country='ES', category='shopping',
             avios_ratio=None, website_url='https://www.elcorteingles.es/',
             notes='Programa fidelidad El Corte Inglés. Supermercado, moda, electrónica. No convierte a Avios.'),
        dict(name='Club Carrefour', currency='Puntos Carrefour', country='ES', category='shopping',
             avios_ratio=None, website_url='https://www.carrefour.es/club-carrefour/',
             notes='Programa fidelidad Carrefour España. Descuentos en gasolina y compras. No convierte a Avios.'),
        dict(name='TheFork Yums', currency='Yums', country='ES', category='dining',
             avios_ratio=None, website_url='https://www.thefork.es/',
             notes='Programa de reservas de restaurantes. Acumula Yums canjeables por descuentos. No Avios.'),
        dict(name='NH Rewards', currency='NH Points', country='INT', category='hotel',
             avios_ratio=None, website_url='https://www.nh-hotels.com/rewards',
             notes='Programa NH Hotel Group. Presencia en España, Brasil y Europa. No convierte a Avios.'),
        dict(name='Meliá Rewards', currency='MeliáRewards Points', country='ES', category='hotel',
             avios_ratio=None, website_url='https://www.melia.com/es/meliarewards',
             notes='Programa Meliá Hotels International. Fuerte presencia España y Caribe. No convierte directamente a Avios.'),
        dict(name='Stix (GPA)', currency='Stix', country='BR', category='shopping',
             avios_ratio=None, website_url='https://www.stix.com.br/',
             notes='Programa fidelidad Pão de Açúcar, Extra, Droga Raia. Intercambia con Livelo.'),
        dict(name='Lidl Plus', currency='Descuentos', country='ES', category='shopping',
             avios_ratio=None, website_url='https://www.lidl.es/lidl-plus',
             notes='App Lidl Plus con cupones y cashback. Solo descuentos, no puntos convertibles.'),
    ]
    for prog_data in new_programs:
        if not db.query(models.LoyaltyProgram).filter_by(name=prog_data['name']).first():
            db.add(models.LoyaltyProgram(**prog_data))
    db.commit()

    # Get program IDs
    iberia_id = get_prog('Iberia Club')
    ba_id = get_prog('British Airways Executive Club')
    amex_mr_id = get_prog('American Express Membership Rewards ES')
    livelo_id = get_prog('Livelo')
    esfera_id = get_prog('Esfera Santander')
    accor_id = get_prog('Accor Live Limitless')
    marriott_id = get_prog('Marriott Bonvoy')
    ihg_id = get_prog('IHG One Rewards')
    hilton_id = get_prog('Hilton Honors')
    eci_id = get_prog('El Corte Inglés Club')
    carrefour_id = get_prog('Club Carrefour')
    thefork_id = get_prog('TheFork Yums')
    nh_id = get_prog('NH Rewards')
    melia_id = get_prog('Meliá Rewards')
    stix_id = get_prog('Stix (GPA)')
    lidl_id = get_prog('Lidl Plus')

    new_opportunities = [
        # ===== ESPAÑA — SUPERMERCADOS =====
        dict(name='El Corte Inglés Supermercado — Iberia Plus Store',
             category='supermarkets', country='ES',
             loyalty_program_id=iberia_id, earning_rate=1.0,
             earning_description='1 Avios/€ comprando en El Corte Inglés via Iberia Plus Store',
             how_to_use='Accede a El Corte Inglés a través del portal Iberia Plus Store antes de comprar online.',
             requirements='Cuenta Iberia Club',
             signup_url='https://www.iberia.com/es/iberia-plus/shopping/',
             notes='Compras online en El Corte Inglés acumulando Avios vía portal.',
             is_active=True, recommendation_score=80),
        dict(name='El Corte Inglés Supermercado — Club ECI',
             category='supermarkets', country='ES',
             loyalty_program_id=eci_id, earning_rate=1.0,
             earning_description='Puntos ECI por compras en supermercado El Corte Inglés',
             how_to_use='Presenta tu tarjeta Club ECI al pagar en supermercados El Corte Inglés.',
             requirements='Tarjeta Club El Corte Inglés (gratuita)',
             signup_url='https://www.elcorteingles.es/',
             notes='Puntos canjeables por descuentos. Compatible con pagar con tarjeta Avios.',
             is_active=True, recommendation_score=60),
        dict(name='Carrefour España — Club Carrefour',
             category='supermarkets', country='ES',
             loyalty_program_id=carrefour_id, earning_rate=1.0,
             earning_description='Puntos Club Carrefour + descuentos en gasolina Carrefour',
             how_to_use='Usa la app o tarjeta Club Carrefour al pagar. Descuento en gasolinera Carrefour.',
             requirements='Tarjeta Club Carrefour (gratuita)',
             signup_url='https://www.carrefour.es/club-carrefour/',
             notes='Descuentos acumulables. Compatible con pagar con tarjeta Avios.',
             is_active=True, recommendation_score=55),
        dict(name='Lidl Plus España',
             category='supermarkets', country='ES',
             loyalty_program_id=lidl_id, earning_rate=0.5,
             earning_description='Cupones y cashback vía app Lidl Plus',
             how_to_use='Descarga la app Lidl Plus y escanea al pagar.',
             requirements='App Lidl Plus',
             signup_url='https://www.lidl.es/lidl-plus',
             notes='Solo cashback y cupones, no puntos convertibles. Precios ya bajos.',
             is_active=True, recommendation_score=45),
        dict(name='Mercadona — Solo tarjeta',
             category='supermarkets', country='ES',
             loyalty_program_id=None, earning_rate=0.0,
             earning_description='Sin programa de fidelidad propio. Usa tarjeta Avios para acumular.',
             how_to_use='Paga con tu tarjeta AmEx o Iberia Visa para acumular puntos de la tarjeta.',
             requirements=None,
             notes='Mercadona no tiene programa de puntos. Acumulas solo vía tarjeta de crédito.',
             is_active=True, recommendation_score=50),

        # ===== ESPAÑA — RESTAURANTES =====
        dict(name='TheFork (ElTenedor) — Yums',
             category='restaurants', country='ES',
             loyalty_program_id=thefork_id, earning_rate=1.0,
             earning_description='Yums por reservar y cenar en restaurantes TheFork',
             how_to_use='Reserva restaurantes a través de TheFork/ElTenedor. Acumulas Yums automáticamente.',
             requirements='Cuenta TheFork',
             signup_url='https://www.thefork.es/',
             notes='1000 Yums = descuento en cena. No convierte a Avios, pero complementa con tarjeta.',
             is_active=True, recommendation_score=55),
        dict(name='Iberia Plus Dining — Restaurantes partner',
             category='restaurants', country='ES',
             loyalty_program_id=iberia_id, earning_rate=1.0,
             earning_description='1 Avios/€ en restaurantes partner Iberia Plus',
             how_to_use='Consulta restaurantes partner en iberia.com/partners y presenta tu número Iberia Plus.',
             requirements='Cuenta Iberia Club',
             signup_url='https://www.iberia.com/es/iberia-plus/partners/',
             notes='Red limitada pero directa. Combinable con tarjeta AmEx para doble acumulación.',
             is_active=True, recommendation_score=75),
        dict(name='Uber Eats España — AmEx Offers',
             category='restaurants', country='ES',
             loyalty_program_id=amex_mr_id, earning_rate=2.0,
             earning_description='2 MR/€ vía AmEx Offers en Uber Eats (cuando disponible)',
             how_to_use='Activa la oferta Uber Eats en tu app AmEx antes de pedir.',
             requirements='Tarjeta AmEx España',
             signup_url='https://www.americanexpress.com/es/',
             notes='Ofertas rotativas. Cuando está activa, 2x puntos. Verificar disponibilidad.',
             is_active=True, recommendation_score=70),

        # ===== ESPAÑA — HOTELES =====
        dict(name='Marriott Bonvoy España — Reserva directa',
             category='hotels', country='ES',
             loyalty_program_id=marriott_id, earning_rate=1.0,
             earning_description='Puntos Marriott por noche (60K = 25K Avios)',
             how_to_use='Reserva directamente en marriott.com con tu cuenta Bonvoy.',
             requirements='Cuenta Marriott Bonvoy (gratuita)',
             signup_url='https://www.marriott.com/loyalty/',
             notes='Ratio bajo a Avios pero buena red en España. AC Hotels, Renaissance, W.',
             is_active=True, recommendation_score=65),
        dict(name='NH Hotels — NH Rewards',
             category='hotels', country='ES',
             loyalty_program_id=nh_id, earning_rate=1.0,
             earning_description='Puntos NH Rewards por reserva directa',
             how_to_use='Reserva en nh-hotels.com con tu cuenta NH Rewards.',
             requirements='Cuenta NH Rewards (gratuita)',
             signup_url='https://www.nh-hotels.com/rewards',
             notes='Muchos hoteles en España. No convierte a Avios. Canjeable por noches gratis.',
             is_active=True, recommendation_score=50),
        dict(name='Meliá Hotels — MeliáRewards',
             category='hotels', country='ES',
             loyalty_program_id=melia_id, earning_rate=1.0,
             earning_description='MeliáRewards Points por reserva directa',
             how_to_use='Reserva en melia.com con tu cuenta MeliáRewards.',
             requirements='Cuenta MeliáRewards (gratuita)',
             signup_url='https://www.melia.com/es/meliarewards',
             notes='Cadena española. Sol, Tryp, Paradisus. No convierte a Avios.',
             is_active=True, recommendation_score=50),

        # ===== BRASIL — SUPERMERCADOS =====
        dict(name='Pão de Açúcar / Extra — Stix + Livelo',
             category='supermarkets', country='BR',
             loyalty_program_id=livelo_id, earning_rate=1.0,
             earning_description='Pontos Livelo/Stix por compras en Pão de Açúcar y Extra',
             how_to_use='Vincula tu cuenta Stix/Livelo al CPF y compra en Pão de Açúcar o Extra.',
             requirements='CPF + cuenta Stix/Livelo',
             signup_url='https://www.stix.com.br/',
             notes='Stix intercambia con Livelo. Livelo transfiere 1:1 a aerolíneas con bonos.',
             is_active=True, recommendation_score=75),
        dict(name='Carrefour Brasil — Programa propio',
             category='supermarkets', country='BR',
             loyalty_program_id=None, earning_rate=0.5,
             earning_description='Descuentos exclusivos socios Carrefour Brasil',
             how_to_use='Usa el cartão Carrefour o app para descuentos exclusivos.',
             requirements='Cartão Carrefour',
             signup_url='https://www.carrefour.com.br/',
             notes='Programa propio de descuentos. No convierte a millas. Usa tarjeta Esfera/Livelo para acumular.',
             is_active=True, recommendation_score=40),

        # ===== BRASIL — RESTAURANTES =====
        dict(name='iFood — Partner Livelo',
             category='restaurants', country='BR',
             loyalty_program_id=livelo_id, earning_rate=2.0,
             earning_description='Até 2 Pontos Livelo/R$ em pedidos iFood',
             how_to_use='Vincule sua conta Livelo ao iFood na app. Pontos acumulados automaticamente.',
             requirements='CPF + conta Livelo + app iFood',
             signup_url='https://www.livelo.com.br/',
             notes='Campañas frecuentes hasta 10x puntos. Principal app delivery Brasil.',
             is_active=True, recommendation_score=80),
        dict(name='Rappi Brasil — Partner Livelo',
             category='restaurants', country='BR',
             loyalty_program_id=livelo_id, earning_rate=1.0,
             earning_description='Pontos Livelo por pedidos en Rappi',
             how_to_use='Vincule Livelo con Rappi para acumular pontos.',
             requirements='CPF + conta Livelo',
             signup_url='https://www.livelo.com.br/',
             notes='Alternativa a iFood. Campañas esporádicas con bonus Livelo.',
             is_active=True, recommendation_score=65),

        # ===== BRASIL — HOTELES =====
        dict(name='Accor ALL Brasil — Reserva directa',
             category='hotels', country='BR',
             loyalty_program_id=accor_id, earning_rate=1.0,
             earning_description='Pontos ALL por noches en Accor Brasil (1:1 a Avios)',
             how_to_use='Reserve en all.accor.com con sua conta ALL. Hoteis: Ibis, Novotel, Pullman, Sofitel.',
             requirements='Conta Accor ALL (gratuita)',
             signup_url='https://all.accor.com/',
             notes='Mejor ratio hotel→Avios (1:1). Amplia red en Brasil.',
             is_active=True, recommendation_score=90),
        dict(name='Marriott Bonvoy Brasil — Reserva directa',
             category='hotels', country='BR',
             loyalty_program_id=marriott_id, earning_rate=1.0,
             earning_description='Pontos Marriott por noche (60K = 25K Avios)',
             how_to_use='Reserve en marriott.com con conta Bonvoy.',
             requirements='Conta Marriott Bonvoy (gratuita)',
             signup_url='https://www.marriott.com/loyalty/',
             notes='Renaissance, JW Marriott São Paulo. Ratio bajo pero buena red.',
             is_active=True, recommendation_score=65),
        dict(name='Booking.com Brasil — via Livelo',
             category='hotels', country='BR',
             loyalty_program_id=livelo_id, earning_rate=1.0,
             earning_description='Pontos Livelo por reservas Booking.com vía portal Livelo',
             how_to_use='Acesse Booking.com pelo portal de compras Livelo.',
             requirements='CPF + conta Livelo',
             signup_url='https://www.livelo.com.br/',
             notes='Acumula Livelo que transfiere 1:1 a aerolíneas. Campañas con bonus.',
             is_active=True, recommendation_score=75),

        # ===== BRASIL — RIDESHARE/TRANSPORTE =====
        dict(name='Uber Brasil — Partner Livelo',
             category='rideshare', country='BR',
             loyalty_program_id=livelo_id, earning_rate=1.0,
             earning_description='Pontos Livelo por corridas Uber',
             how_to_use='Vincule sua conta Livelo ao Uber na app Livelo.',
             requirements='CPF + conta Livelo',
             signup_url='https://www.livelo.com.br/',
             notes='Acumula Livelo en viajes diarios. Transfiere a aerolíneas.',
             is_active=True, recommendation_score=75),
        dict(name='99 (DiDi) Brasil — Partner Livelo',
             category='rideshare', country='BR',
             loyalty_program_id=livelo_id, earning_rate=1.0,
             earning_description='Pontos Livelo por corridas 99/DiDi',
             how_to_use='Vincule Livelo con 99 para acumular pontos.',
             requirements='CPF + conta Livelo',
             signup_url='https://www.livelo.com.br/',
             notes='Alternativa a Uber en Brasil. Campañas ocasionales de bonus.',
             is_active=True, recommendation_score=65),

        # ===== GIBRALTAR/UK — HOTELES =====
        dict(name='Accor ALL UK/Gibraltar — Reserva directa',
             category='hotels', country='GI',
             loyalty_program_id=accor_id, earning_rate=1.0,
             earning_description='ALL Points por noches (1:1 a Avios)',
             how_to_use='Book on all.accor.com with your ALL account.',
             requirements='Accor ALL account (free)',
             signup_url='https://all.accor.com/',
             notes='Best hotel-to-Avios ratio (1:1). Ibis, Novotel, Sofitel in UK.',
             is_active=True, recommendation_score=90),
        dict(name='Marriott Bonvoy UK — Reserva directa',
             category='hotels', country='GI',
             loyalty_program_id=marriott_id, earning_rate=1.0,
             earning_description='Marriott Points per night (60K = 25K Avios)',
             how_to_use='Book on marriott.com with Bonvoy account.',
             requirements='Marriott Bonvoy account (free)',
             signup_url='https://www.marriott.com/loyalty/',
             notes='Good UK presence. Low Avios ratio but wide network.',
             is_active=True, recommendation_score=65),
        dict(name='IHG One Rewards UK — Reserva directa',
             category='hotels', country='GI',
             loyalty_program_id=ihg_id, earning_rate=1.0,
             earning_description='IHG Points per night',
             how_to_use='Book on ihg.com with One Rewards account.',
             requirements='IHG One Rewards account (free)',
             signup_url='https://www.ihg.com/onerewards',
             notes='Holiday Inn, InterContinental. Good UK presence. ~5:1 to Avios.',
             is_active=True, recommendation_score=55),

        # ===== GIBRALTAR/UK — RESTAURANTES =====
        dict(name='BA Avios Dining — eStore restaurants',
             category='restaurants', country='GI',
             loyalty_program_id=ba_id, earning_rate=1.0,
             earning_description='Avios per £ at BA dining partners',
             how_to_use='Check BA Avios eStore for dining partners. Link your Executive Club number.',
             requirements='BA Executive Club account',
             signup_url='https://www.britishairways.com/es-es/executive-club',
             notes='Limited network but earns Avios directly. Combine with Avios credit card.',
             is_active=True, recommendation_score=70),

        # ===== INTERNATIONAL — HOTELES (expand) =====
        dict(name='IHG One Rewards — Reserva global',
             category='hotels', country='INT',
             loyalty_program_id=ihg_id, earning_rate=1.0,
             earning_description='IHG Points por noche (~5:1 a Avios)',
             how_to_use='Reserva en ihg.com con tu cuenta One Rewards.',
             requirements='Cuenta IHG One Rewards (gratuita)',
             signup_url='https://www.ihg.com/onerewards',
             notes='Holiday Inn, InterContinental, Hotel Indigo. Buena red global.',
             is_active=True, recommendation_score=60),
        dict(name='Hilton Honors — Reserva global',
             category='hotels', country='INT',
             loyalty_program_id=hilton_id, earning_rate=1.0,
             earning_description='Hilton Points por noche (~10:1 a Avios vía BA)',
             how_to_use='Reserva en hilton.com con tu cuenta Honors.',
             requirements='Cuenta Hilton Honors (gratuita)',
             signup_url='https://www.hilton.com/honors',
             notes='Ratio bajo a Avios pero 5ª noche gratis en canjes. Útil en USA/Asia.',
             is_active=True, recommendation_score=55),
    ]

    for opp_data in new_opportunities:
        if not db.query(models.EarningOpportunity).filter_by(name=opp_data['name']).first():
            db.add(models.EarningOpportunity(**opp_data))

    db.commit()
    print('Full v3 seed complete: Added earning opportunities for supermarkets, restaurants, hotels, rideshare.')


def seed_fix_broken_data(db):
    """Fix broken URLs, dead sources, and outdated names in existing DB records (idempotent)."""

    # --- Remove dead RSS feed sources (domains no longer exist as of Feb 2026) ---
    dead_urls = [
        "https://www.millasdecarton.com/feed/",
        "https://viajeroastuto.com/feed/",
        "https://www.elviajeromillas.com/feed/",
    ]
    for url in dead_urls:
        source = db.query(models.Source).filter_by(url=url).first()
        if source:
            db.delete(source)
            print(f"  Removed dead source: {source.name} ({url})")

    # --- Fix Cepsa → Moeve rebrand on earning opportunities ---
    cepsa_mas = db.query(models.EarningOpportunity).filter_by(
        name="Cepsa Más — Avios por gasolina"
    ).first()
    if cepsa_mas:
        cepsa_mas.name = "Moeve (ex-Cepsa) Más — Avios por gasolina"
        cepsa_mas.earning_description = "2 Avios por litro de combustible en estaciones Moeve (antes Cepsa)"
        cepsa_mas.signup_url = "https://www.moeve.es/es/particular"
        cepsa_mas.notes = "Partnership Moeve (ex-Cepsa) + Iberia Club: Avios directos. Coexiste con Club Moeve gow (saldo euros). Usar ambos si es posible. Cepsa rebrandeó a Moeve en 2025."
        print("  Updated: Cepsa Más → Moeve Más")

    cepsa_gow = db.query(models.EarningOpportunity).filter_by(
        name="Cepsa GOW — Saldo por gasolina y partners"
    ).first()
    if cepsa_gow:
        cepsa_gow.name = "Club Moeve gow — Saldo por gasolina y partners"
        cepsa_gow.earning_description = "Saldo (saldow) por repostaje, recargas, lavados y 40+ marcas colaboradoras"
        cepsa_gow.signup_url = "https://www.moeve.es/es/particular"
        cepsa_gow.notes = "Antes Cepsa GOW, ahora Club Moeve gow. Partners incluyen Amazon, eDreams, Europcar, MediaMarkt, Pangea, Sprinter. Saldo en euros, no puntos."
        print("  Updated: Cepsa GOW → Club Moeve gow")

    # --- Fix outdated signup URLs ---
    nafte = db.query(models.EarningOpportunity).filter(
        models.EarningOpportunity.signup_url == "https://mail.nafte.es/tarjeta-cliente/puntos.php"
    ).first()
    if nafte:
        nafte.signup_url = "https://www.nafte.es/"
        print("  Updated: Naftë URL fixed")

    gasoprix = db.query(models.EarningOpportunity).filter(
        models.EarningOpportunity.signup_url == "https://www.gasoprix.com/bases-programa-de-puntos-2025/"
    ).first()
    if gasoprix:
        gasoprix.signup_url = "https://www.gasoprix.com/programa-puntos/"
        print("  Updated: Gasoprix URL fixed")

    # --- Fix Amex Spain URLs (URL structure changed to /es-es/) ---
    amex_url_fixes = {
        "https://www.americanexpress.com/es/tarjetas/platinum/":
            "https://www.americanexpress.com/es-es/tarjetas/tarjetas-de-cargo/tarjeta-platinum/",
        "https://www.americanexpress.com/es/tarjetas/gold/":
            "https://www.americanexpress.com/es-es/tarjetas/tarjetas-de-cargo/tarjeta-gold-card/",
        "https://www.americanexpress.com/es/beneficios/membership-rewards/":
            "https://www.americanexpress.com/es-es/rewards/membership-rewards/index.mtw",
    }
    for old_url, new_url in amex_url_fixes.items():
        # Fix in credit cards
        card = db.query(models.CreditCard).filter(
            models.CreditCard.application_url == old_url
        ).first()
        if card:
            card.application_url = new_url
            print(f"  Updated card URL: {card.name}")
        # Fix in loyalty programs
        prog = db.query(models.LoyaltyProgram).filter(
            models.LoyaltyProgram.website_url == old_url
        ).first()
        if prog:
            prog.website_url = new_url
            print(f"  Updated program URL: {prog.name}")

    # --- Fix Vueling Club URL ---
    vueling = db.query(models.LoyaltyProgram).filter_by(name="Vueling Club").first()
    if vueling and vueling.website_url == "https://www.vueling.com/es/vueling-club":
        vueling.website_url = "https://www.vueling.com/es/vueling-club/que-es-vueling-club"
        print("  Updated: Vueling Club URL")

    # --- Fix Repsol Travel Club URL ---
    travel_club = db.query(models.LoyaltyProgram).filter_by(name="Travel Club (Repsol)").first()
    if travel_club and "repsol.com" in (travel_club.website_url or ""):
        travel_club.website_url = "https://www.repsol.es/particulares/beneficios-clientes/tarjeta-repsol-travel/"
        print("  Updated: Travel Club (Repsol) URL")

    repsol_opp = db.query(models.EarningOpportunity).filter_by(name="Repsol Waylet + Travel Club").first()
    if repsol_opp and "repsol.com" in (repsol_opp.signup_url or ""):
        repsol_opp.signup_url = "https://www.repsol.es/particulares/beneficios-clientes/tarjeta-repsol-travel/"
        print("  Updated: Repsol Waylet opportunity URL")

    # --- Fix Santander Iberia Club card URL ---
    santander_card = db.query(models.CreditCard).filter_by(name="Santander Iberia Club Visa").first()
    if santander_card:
        santander_card.application_url = "https://www.bancosantander.es/en/particulares/tarjetas/credito/plan-iberia-plus"
        print("  Updated: Santander Iberia Club card URL")

    # --- Deprioritize stale puntosviajeros.com (last post Jan 2023) ---
    pv_source = db.query(models.Source).filter_by(url="https://puntosviajeros.com/feed/").first()
    if pv_source and pv_source.priority > 5:
        pv_source.priority = 5
        pv_source.notes = "Blog inactivo desde enero 2023. Contenido histórico útil pero sin actualizaciones."
        print("  Updated: Puntos Viajeros deprioritized (stale since Jan 2023)")

    db.commit()
    print("Fix broken data complete.")
