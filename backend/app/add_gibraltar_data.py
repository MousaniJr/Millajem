"""
Script para añadir datos de Gibraltar
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import EarningOpportunity, LoyaltyProgram


def add_gibraltar_opportunities(db: Session):
    """Añadir earning opportunities de Gibraltar"""

    # Verificar si ya existen
    existing = db.query(EarningOpportunity).filter(EarningOpportunity.country == "GI").count()
    if existing > 0:
        print(f"Ya existen {existing} opportunities de Gibraltar")
        return

    # Obtener programas
    iberia = db.query(LoyaltyProgram).filter(LoyaltyProgram.name == "Iberia Club").first()
    ba = db.query(LoyaltyProgram).filter(LoyaltyProgram.name == "British Airways Executive Club").first()

    opportunities = [
        # GIBRALTAR - Combustible
        {
            "name": "Cepsa Gibraltar (verificar)",
            "category": "fuel",
            "country": "GI",
            "loyalty_program_id": iberia.id if iberia else None,
            "earning_rate": 2.0,
            "earning_description": "2 Avios por litro (si aplica programa Cepsa)",
            "how_to_use": "VERIFICAR: Repostar en Cepsa Gibraltar y comprobar si acepta programa Avios español",
            "requirements": "Socio Iberia Club + tarjeta Cepsa",
            "signup_url": None,
            "more_info_url": None,
            "is_active": True,
            "notes": "PENDIENTE CONFIRMAR en estación. Combustible más barato que España por impuestos. Doble beneficio si aplica Avios.",
            "recommendation_score": 85
        },
        {
            "name": "GO Card (Gib Oil)",
            "category": "fuel",
            "country": "GI",
            "loyalty_program_id": None,
            "earning_rate": 0.0,  # Programa local, no Avios
            "earning_description": "Descuentos en combustible (NO Avios)",
            "how_to_use": "Solicitar GO Card en estaciones Gib Oil",
            "requirements": None,
            "signup_url": None,
            "more_info_url": None,
            "is_active": True,
            "notes": "Programa local de fidelidad Gibraltar. No gana Avios pero ahorra dinero.",
            "recommendation_score": 60
        },

        # GIBRALTAR - Vuelos
        {
            "name": "British Airways GIB-LHR",
            "category": "flights",
            "country": "GI",
            "loyalty_program_id": ba.id if ba else None,
            "earning_rate": 7.0,  # Base earning
            "earning_description": "7-9 Avios por GBP gastada (según status)",
            "how_to_use": "Volar BA desde Gibraltar. Vincular número Executive Club al reservar.",
            "requirements": "Socio BA Executive Club",
            "signup_url": "https://www.britishairways.com/",
            "more_info_url": None,
            "is_active": True,
            "notes": "GIB-LHR: 7,250 Avios off-peak one-way. Tasas mínimas. Ganas 7-9 Avios/GBP en vuelo pagado.",
            "recommendation_score": 90
        },

        # GIBRALTAR - Shopping (sin IVA)
        {
            "name": "Main Street Gibraltar (Sin IVA)",
            "category": "shopping",
            "country": "GI",
            "loyalty_program_id": None,
            "earning_rate": 0.0,  # No gana puntos pero ahorra 20%
            "earning_description": "~20% ahorro vs España (sin IVA)",
            "how_to_use": "Comprar en tiendas Main Street Gibraltar (M&S, etc.)",
            "requirements": None,
            "signup_url": None,
            "more_info_url": None,
            "is_active": True,
            "notes": "NO gana Avios directamente pero ahorra 20% por ausencia IVA. Usar Amex España para ganar 1 Avios/EUR (verificar comisión FX).",
            "recommendation_score": 75
        },

        # GIBRALTAR - Supermercados
        {
            "name": "Morrisons Gibraltar",
            "category": "supermarket",
            "country": "GI",
            "loyalty_program_id": None,
            "earning_rate": 0.0,
            "earning_description": "No tiene programa fidelidad en GIB",
            "how_to_use": "Pagar con tarjeta que gane puntos (Amex España o HSBC si disponible)",
            "requirements": None,
            "signup_url": None,
            "more_info_url": None,
            "is_active": True,
            "notes": "Morrisons More Card NO disponible en Gibraltar. Usar tarjeta recompensas para compras diarias.",
            "recommendation_score": 65
        },
        {
            "name": "Eroski Gibraltar",
            "category": "supermarket",
            "country": "GI",
            "loyalty_program_id": None,
            "earning_rate": 0.0,
            "earning_description": "VERIFICAR si acepta Eroski Club Card",
            "how_to_use": "Comprobar si la Eroski Club Card española funciona en Gibraltar",
            "requirements": "Eroski Club Card (gratis)",
            "signup_url": None,
            "more_info_url": None,
            "is_active": True,
            "notes": "PENDIENTE VERIFICAR. Si acepta Club Card, puedes acumular descuentos/puntos.",
            "recommendation_score": 70
        },

        # AEROPUERTOS CERCANOS
        {
            "name": "Vuelos desde Málaga (AGP)",
            "category": "flights",
            "country": "GI",  # Categoria GI por proximidad
            "loyalty_program_id": iberia.id if iberia else None,
            "earning_rate": 1.0,  # Variable según vuelo
            "earning_description": "Gana Avios en Iberia/BA/Vueling desde Málaga",
            "how_to_use": "Alternativa a GIB. 130km (1h45). BA, Iberia, Vueling disponibles.",
            "requirements": "Socio Iberia/BA",
            "signup_url": None,
            "more_info_url": None,
            "is_active": True,
            "notes": "AGP tiene 85+ destinos Ryanair, 21+ easyJet. Mucha más conectividad que GIB. Considerar para viajes largos.",
            "recommendation_score": 80
        },
    ]

    for opp_data in opportunities:
        opp = EarningOpportunity(**opp_data)
        db.add(opp)

    db.commit()
    print(f"{len(opportunities)} Gibraltar opportunities añadidas")


def main():
    db = SessionLocal()
    try:
        add_gibraltar_opportunities(db)
        print("Gibraltar data añadido correctamente")
    finally:
        db.close()


if __name__ == "__main__":
    main()
