"""
Inicializar fuentes de información en la base de datos
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Source


def init_sources(db: Session):
    """Inicializar todas las fuentes (RSS feeds y redes sociales)"""

    # Verificar si ya hay fuentes
    existing_count = db.query(Source).count()
    if existing_count > 0:
        print(f"Ya existen {existing_count} fuentes en la base de datos")
        return

    sources = []

    # ==================== RSS FEEDS ====================

    # España (2)
    sources.extend([
        {
            "name": "Puntos Viajeros",
            "source_type": "rss_feed",
            "country": "ES",
            "url": "https://puntosviajeros.com/feed/",
            "website_url": "https://puntosviajeros.com",
            "is_active": True,
            "priority": 9,
            "description": "Blog español sobre puntos, Avios e Iberia"
        },
        {
            "name": "Travel-Dealz",
            "source_type": "rss_feed",
            "country": "ES",
            "url": "https://travel-dealz.com/feed/",
            "website_url": "https://travel-dealz.com",
            "is_active": True,
            "priority": 8,
            "description": "Ofertas de vuelos y millas en español"
        },
    ])

    # Brasil (5)
    sources.extend([
        {
            "name": "Melhores Destinos",
            "source_type": "rss_feed",
            "country": "BR",
            "url": "https://www.melhoresdestinos.com.br/feed",
            "website_url": "https://www.melhoresdestinos.com.br",
            "is_active": True,
            "priority": 9,
            "description": "Principal blog de viajes y puntos de Brasil"
        },
        {
            "name": "Passageiro de Primeira",
            "source_type": "rss_feed",
            "country": "BR",
            "url": "https://passageirodeprimeira.com/feed/",
            "website_url": "https://passageirodeprimeira.com",
            "is_active": True,
            "priority": 10,
            "description": "Blog premium brasileño de millasSource y Livelo"
        },
        {
            "name": "Pontos pra Voar",
            "source_type": "rss_feed",
            "country": "BR",
            "url": "https://pontospravoar.com/feed/",
            "website_url": "https://pontospravoar.com",
            "is_active": True,
            "priority": 9,
            "description": "Blog brasileño especializado en Livelo, Smiles, Esfera"
        },
        {
            "name": "Mil Milhas",
            "source_type": "rss_feed",
            "country": "BR",
            "url": "https://www.milmilhas.com.br/blog/feed/",
            "website_url": "https://www.milmilhas.com.br",
            "is_active": True,
            "priority": 7,
            "description": "Blog de Mil Milhas (marketplace de millas)"
        },
        {
            "name": "Blog MaxMilhas",
            "source_type": "rss_feed",
            "country": "BR",
            "url": "https://blog.maxmilhas.com.br/feed/",
            "website_url": "https://blog.maxmilhas.com.br",
            "is_active": True,
            "priority": 7,
            "description": "Blog de MaxMilhas (marketplace de millas)"
        },
    ])

    # UK/Gibraltar (3)
    sources.extend([
        {
            "name": "Head for Points",
            "source_type": "rss_feed",
            "country": "GI",
            "url": "https://www.headforpoints.com/feed/",
            "website_url": "https://www.headforpoints.com",
            "is_active": True,
            "priority": 10,
            "description": "Principal blog UK de Avios, BA e Iberia"
        },
        {
            "name": "InsideFlyer UK",
            "source_type": "rss_feed",
            "country": "GI",
            "url": "https://www.insideflyer.co.uk/feed/",
            "website_url": "https://www.insideflyer.co.uk",
            "is_active": True,
            "priority": 8,
            "description": "Noticias UK de programas de fidelidad"
        },
        {
            "name": "Turning Left for Less",
            "source_type": "rss_feed",
            "country": "GI",
            "url": "https://www.turningleftforless.com/feed/",
            "website_url": "https://www.turningleftforless.com",
            "is_active": True,
            "priority": 8,
            "description": "Blog UK especializado en Avios y vuelos premium"
        },
    ])

    # Internacional (3)
    sources.extend([
        {
            "name": "One Mile at a Time",
            "source_type": "rss_feed",
            "country": "INT",
            "url": "https://onemileatatime.com/feed/",
            "website_url": "https://onemileatatime.com",
            "is_active": True,
            "priority": 8,
            "description": "Blog internacional de Ben Schlappig (muy popular)"
        },
        {
            "name": "The Points Guy",
            "source_type": "rss_feed",
            "country": "INT",
            "url": "https://thepointsguy.com/feed/",
            "website_url": "https://thepointsguy.com",
            "is_active": True,
            "priority": 9,
            "description": "El blog más grande de puntos y millas del mundo"
        },
        {
            "name": "Frequent Miler",
            "source_type": "rss_feed",
            "country": "INT",
            "url": "https://frequentmiler.com/feed/",
            "website_url": "https://frequentmiler.com",
            "is_active": True,
            "priority": 8,
            "description": "Blog técnico estadounidense de millas y puntos"
        },
    ])

    # ==================== INSTAGRAM ====================

    # España (4)
    sources.extend([
        {
            "name": "@puntosviajeros",
            "source_type": "instagram",
            "country": "ES",
            "url": "https://instagram.com/puntosviajeros",
            "is_active": False,  # Manual por defecto
            "priority": 9,
            "description": "Instagram de Puntos Viajeros - promociones Iberia/BA/Amex"
        },
        {
            "name": "@volandoconpuntos",
            "source_type": "instagram",
            "country": "ES",
            "url": "https://instagram.com/volandoconpuntos",
            "is_active": False,
            "priority": 7,
            "description": "Ofertas y consejos de viajes con puntos"
        },
        {
            "name": "@millasymas",
            "source_type": "instagram",
            "country": "ES",
            "url": "https://instagram.com/millasymas",
            "is_active": False,
            "priority": 7,
            "description": "Noticias y promociones de millas"
        },
        {
            "name": "@viajerosporelmundo",
            "source_type": "instagram",
            "country": "ES",
            "url": "https://instagram.com/viajerosporelmundo",
            "is_active": False,
            "priority": 6,
            "description": "Comunidad de viajeros"
        },
    ])

    # Brasil (5)
    sources.extend([
        {
            "name": "@pontospravoar",
            "source_type": "instagram",
            "country": "BR",
            "url": "https://instagram.com/pontospravoar",
            "is_active": False,
            "priority": 9,
            "description": "Instagram principal de Pontos pra Voar"
        },
        {
            "name": "@passageirodeprimeira",
            "source_type": "instagram",
            "country": "BR",
            "url": "https://instagram.com/passageirodeprimeira",
            "is_active": False,
            "priority": 9,
            "description": "Ofertas premium Livelo/Smiles/Esfera"
        },
        {
            "name": "@milhasaereasbr",
            "source_type": "instagram",
            "country": "BR",
            "url": "https://instagram.com/milhasaereasbr",
            "is_active": False,
            "priority": 7,
            "description": "Comunidad brasileña de millas"
        },
        {
            "name": "@voesimples",
            "source_type": "instagram",
            "country": "BR",
            "url": "https://instagram.com/voesimples",
            "is_active": False,
            "priority": 7,
            "description": "Tutoriales y ofertas de millas"
        },
        {
            "name": "@melhoresdestinos",
            "source_type": "instagram",
            "country": "BR",
            "url": "https://instagram.com/melhoresdestinos",
            "is_active": False,
            "priority": 8,
            "description": "Instagram de Melhores Destinos"
        },
    ])

    # Gibraltar/UK (3)
    sources.extend([
        {
            "name": "@headforpoints",
            "source_type": "instagram",
            "country": "GI",
            "url": "https://instagram.com/headforpoints",
            "is_active": False,
            "priority": 9,
            "description": "Instagram de Head for Points UK"
        },
        {
            "name": "@britishairways",
            "source_type": "instagram",
            "country": "GI",
            "url": "https://instagram.com/britishairways",
            "is_active": False,
            "priority": 8,
            "description": "Cuenta oficial de British Airways"
        },
        {
            "name": "@iberia",
            "source_type": "instagram",
            "country": "GI",
            "url": "https://instagram.com/iberia",
            "is_active": False,
            "priority": 8,
            "description": "Cuenta oficial de Iberia"
        },
    ])

    # Internacional (3)
    sources.extend([
        {
            "name": "@thepointsguy",
            "source_type": "instagram",
            "country": "INT",
            "url": "https://instagram.com/thepointsguy",
            "is_active": False,
            "priority": 8,
            "description": "Instagram de The Points Guy"
        },
        {
            "name": "@onemileatatime",
            "source_type": "instagram",
            "country": "INT",
            "url": "https://instagram.com/onemileatatime",
            "is_active": False,
            "priority": 7,
            "description": "Instagram de One Mile at a Time"
        },
        {
            "name": "@frequentmiler",
            "source_type": "instagram",
            "country": "INT",
            "url": "https://instagram.com/frequentmiler",
            "is_active": False,
            "priority": 7,
            "description": "Instagram de Frequent Miler"
        },
    ])

    # ==================== TWITTER/X ====================

    # España (3)
    sources.extend([
        {
            "name": "@puntosviajeros",
            "source_type": "twitter",
            "country": "ES",
            "url": "https://twitter.com/puntosviajeros",
            "is_active": False,
            "priority": 9,
            "description": "Twitter de Puntos Viajeros"
        },
        {
            "name": "@millasymas",
            "source_type": "twitter",
            "country": "ES",
            "url": "https://twitter.com/millasymas",
            "is_active": False,
            "priority": 7,
            "description": "Twitter de Millas y Más"
        },
        {
            "name": "@iberiaclub",
            "source_type": "twitter",
            "country": "ES",
            "url": "https://twitter.com/iberiaclub",
            "is_active": False,
            "priority": 8,
            "description": "Cuenta oficial de Iberia Club (Twitter)"
        },
    ])

    # Brasil (4)
    sources.extend([
        {
            "name": "@pontospravoar",
            "source_type": "twitter",
            "country": "BR",
            "url": "https://twitter.com/pontospravoar",
            "is_active": False,
            "priority": 9,
            "description": "Twitter de Pontos pra Voar"
        },
        {
            "name": "@passageiro1",
            "source_type": "twitter",
            "country": "BR",
            "url": "https://twitter.com/passageiro1",
            "is_active": False,
            "priority": 9,
            "description": "Twitter de Passageiro de Primeira"
        },
        {
            "name": "@smilesgol",
            "source_type": "twitter",
            "country": "BR",
            "url": "https://twitter.com/smilesgol",
            "is_active": False,
            "priority": 8,
            "description": "Cuenta oficial de Smiles GOL"
        },
        {
            "name": "@livelobr",
            "source_type": "twitter",
            "country": "BR",
            "url": "https://twitter.com/livelobr",
            "is_active": False,
            "priority": 8,
            "description": "Cuenta oficial de Livelo"
        },
    ])

    # Gibraltar/UK (5)
    sources.extend([
        {
            "name": "@headforpoints",
            "source_type": "twitter",
            "country": "GI",
            "url": "https://twitter.com/headforpoints",
            "is_active": False,
            "priority": 9,
            "description": "Twitter de Head for Points"
        },
        {
            "name": "@british_airways",
            "source_type": "twitter",
            "country": "GI",
            "url": "https://twitter.com/british_airways",
            "is_active": False,
            "priority": 8,
            "description": "Cuenta oficial de British Airways"
        },
        {
            "name": "@iberia",
            "source_type": "twitter",
            "country": "GI",
            "url": "https://twitter.com/iberia",
            "is_active": False,
            "priority": 8,
            "description": "Cuenta oficial de Iberia (Twitter)"
        },
        {
            "name": "@aviosclub",
            "source_type": "twitter",
            "country": "GI",
            "url": "https://twitter.com/aviosclub",
            "is_active": False,
            "priority": 7,
            "description": "Comunidad de Avios collectors"
        },
        {
            "name": "@insideflyer_uk",
            "source_type": "twitter",
            "country": "GI",
            "url": "https://twitter.com/insideflyer_uk",
            "is_active": False,
            "priority": 7,
            "description": "Twitter de InsideFlyer UK"
        },
    ])

    # Internacional (3)
    sources.extend([
        {
            "name": "@thepointsguy",
            "source_type": "twitter",
            "country": "INT",
            "url": "https://twitter.com/thepointsguy",
            "is_active": False,
            "priority": 8,
            "description": "Twitter de The Points Guy"
        },
        {
            "name": "@onemileatatime",
            "source_type": "twitter",
            "country": "INT",
            "url": "https://twitter.com/onemileatatime",
            "is_active": False,
            "priority": 7,
            "description": "Twitter de One Mile at a Time"
        },
        {
            "name": "@awardwallet",
            "source_type": "twitter",
            "country": "INT",
            "url": "https://twitter.com/awardwallet",
            "is_active": False,
            "priority": 7,
            "description": "Twitter de AwardWallet (tracking app)"
        },
    ])

    # Insertar todas las fuentes
    for source_data in sources:
        source = Source(**source_data)
        db.add(source)

    db.commit()

    # Contar por tipo
    rss_count = len([s for s in sources if s["source_type"] == "rss_feed"])
    instagram_count = len([s for s in sources if s["source_type"] == "instagram"])
    twitter_count = len([s for s in sources if s["source_type"] == "twitter"])

    print(f"Inicializadas {len(sources)} fuentes:")
    print(f"  - RSS Feeds: {rss_count}")
    print(f"  - Instagram: {instagram_count}")
    print(f"  - Twitter: {twitter_count}")


def main():
    db = SessionLocal()
    try:
        init_sources(db)
        print("Fuentes inicializadas correctamente")
    finally:
        db.close()


if __name__ == "__main__":
    main()
