"""
Script para inicializar la base de datos con programas de fidelidad básicos
"""
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from .models import LoyaltyProgram


def init_loyalty_programs(db: Session):
    """Inicializar programas de fidelidad"""

    # Verificar si ya hay datos
    if db.query(LoyaltyProgram).count() > 0:
        print("Los programas ya están inicializados")
        return

    programs = [
        # España - Avios
        {
            "name": "Iberia Club",
            "currency": "Avios",
            "country": "ES",
            "category": "airline",
            "avios_ratio": 1.0,
            "website_url": "https://www.iberia.com",
            "login_url": "https://www.iberia.com/es/login/",
            "notes": "Programa principal para España. Transferencias gratuitas 1:1 con BA, Qatar, Vueling"
        },
        {
            "name": "British Airways Executive Club",
            "currency": "Avios",
            "country": "UK",
            "category": "airline",
            "avios_ratio": 1.0,
            "website_url": "https://www.britishairways.com/",
            "login_url": "https://www.britishairways.com/travel/login/execclub/_gf/es_es",
            "notes": "BA Household Account para compartir Avios. Útil para vuelos desde Gibraltar"
        },
        {
            "name": "Vueling Club",
            "currency": "Avios",
            "country": "ES",
            "category": "airline",
            "avios_ratio": 1.0,
            "website_url": "https://www.vueling.com/",
            "notes": "Low-cost con Avios. Ideal para Europa"
        },
        {
            "name": "Qatar Privilege Club",
            "currency": "Avios",
            "country": "QA",
            "category": "airline",
            "avios_ratio": 1.0,
            "website_url": "https://www.qatarairways.com/privilegeclub",
            "notes": "QSuite business class, mejores redenciones a Asia/Middle East"
        },
        # España - Otros
        {
            "name": "TAP Miles&Go",
            "currency": "Miles",
            "country": "PT",
            "category": "airline",
            "avios_ratio": None,
            "website_url": "https://www.flytap.com/es-es/miles-and-go",
            "notes": "Star Alliance. Ya tienes cuenta"
        },
        # España - Transferibles
        {
            "name": "American Express Membership Rewards (ES)",
            "currency": "MR Points",
            "country": "ES",
            "category": "transfer",
            "avios_ratio": 1.0,
            "website_url": "https://www.americanexpress.com/es/",
            "notes": "1 MR = 1 Avios. Tarjeta Gold/Platinum recomendada"
        },
        # Brasil - Principales
        {
            "name": "Livelo",
            "currency": "Pontos",
            "country": "BR",
            "category": "transfer",
            "avios_ratio": 3.5,  # Sin bonus, 3.5:1 via Smiles
            "website_url": "https://www.livelo.com.br/",
            "notes": "Principal programa brasileño. Transferible a airlines 1:1 con bonos. Ya tienes cuenta"
        },
        {
            "name": "Esfera",
            "currency": "Pontos",
            "country": "BR",
            "category": "transfer",
            "avios_ratio": 2.0,  # Mejor ratio BR->Avios
            "website_url": "https://www.esfera.com.vc/",
            "notes": "MEJOR RATIO a Iberia: 2:1. Ideal para acumular y transferir a Avios"
        },
        {
            "name": "Smiles",
            "currency": "Miles",
            "country": "BR",
            "category": "airline",
            "avios_ratio": None,
            "website_url": "https://www.smiles.com.br/",
            "notes": "GOL + Star Alliance. Buen sweet spots a Europa"
        },
        {
            "name": "Latam Pass",
            "currency": "Pontos",
            "country": "BR",
            "category": "airline",
            "avios_ratio": None,
            "website_url": "https://www.latamairlines.com/br/pt/latam-pass",
            "notes": "Oneworld. Vuelos LATAM a Brasil"
        },
        # Hoteles
        {
            "name": "Accor Live Limitless",
            "currency": "Points",
            "country": "INT",
            "category": "hotel",
            "avios_ratio": 1.0,  # 2000 ALL = 2000 Avios
            "website_url": "https://all.accor.com/",
            "notes": "MEJOR conversión a Avios de hoteles: 1:1"
        },
        {
            "name": "Marriott Bonvoy",
            "currency": "Points",
            "country": "INT",
            "category": "hotel",
            "avios_ratio": 2.4,  # 60,000 Marriott = 25,000 Avios
            "website_url": "https://www.marriott.com/loyalty.mi",
            "notes": "60K Marriott = 25K Avios (ratio 2.4:1)"
        },
    ]

    for program_data in programs:
        program = LoyaltyProgram(**program_data)
        db.add(program)

    db.commit()
    print(f"{len(programs)} programas de fidelidad inicializados")


def main():
    """Main initialization function"""
    print("Inicializando base de datos...")

    # Crear tablas
    init_db()
    print("Tablas creadas")

    # Crear sesión
    db = SessionLocal()
    try:
        # Inicializar programas
        init_loyalty_programs(db)
        print("Datos iniciales cargados")
    finally:
        db.close()


if __name__ == "__main__":
    main()
