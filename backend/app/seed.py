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
             website_url="https://www.americanexpress.com/es/beneficios/membership-rewards/",
             notes="1 MR = 1 Avios (Iberia o BA). Mejor ratio de transferencia en España."),
        dict(name="Vueling Club", currency="Puntos Vueling", country="ES", category="airline",
             avios_ratio=None,
             website_url="https://www.vueling.com/es/vueling-club",
             notes="No convierte a Avios directamente. Útil para vuelos domésticos."),

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
            application_url="https://www.americanexpress.com/es/tarjetas/platinum/",
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
            application_url="https://www.americanexpress.com/es/tarjetas/gold/",
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
            name="Cepsa Más — Avios por gasolina",
            category="fuel",
            country="ES",
            loyalty_program_id=iberia_id,
            earning_rate=2.0,
            earning_description="2 Avios por litro de combustible",
            how_to_use="Regístrate en Cepsa Más con tu nº de Iberia Club. Usa la app o tarjeta Cepsa en estaciones.",
            requirements="Socio Iberia Club + tarjeta/app Cepsa Más",
            signup_url="https://www.cepsa.com/es/cepsa-mas",
            notes="Solo estaciones Cepsa. Acumula directamente en Iberia Club.",
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
        dict(
            name="Millas de Cartón",
            source_type="rss_feed",
            country="ES",
            url="https://www.millasdecarton.com/feed/",
            website_url="https://www.millasdecarton.com",
            is_active=True,
            priority=9,
            description="Referencia española en maximización de Avios e Iberia Plus.",
        ),
        dict(
            name="Viajero Astuto",
            source_type="rss_feed",
            country="ES",
            url="https://viajeroastuto.com/feed/",
            website_url="https://viajeroastuto.com",
            is_active=True,
            priority=8,
            description="Guías y estrategias de viajes con puntos en español.",
        ),
        dict(
            name="El Viajero de Millas",
            source_type="rss_feed",
            country="ES",
            url="https://www.elviajeromillas.com/feed/",
            website_url="https://www.elviajeromillas.com",
            is_active=True,
            priority=7,
            description="Noticias y análisis sobre programas de fidelidad en España.",
        ),

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


def run_seed(db: Session):
    """Ejecuta el seed completo si la BD está vacía"""
    # Solo ejecutar si no hay programas (evita duplicados)
    count = db.query(models.LoyaltyProgram).count()
    if count > 0:
        return False  # Ya tiene datos

    print("Seeding database with initial data...")
    program_map = seed_loyalty_programs(db)
    seed_credit_cards(db, program_map)
    seed_earning_opportunities(db, program_map)
    seed_sources(db)
    print(f"Seed complete: {len(program_map)} programs, cards, opportunities, and sources added.")
    return True
