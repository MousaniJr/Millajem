"""
Script para inicializar tarjetas y earning opportunities
Basado en la investigación del documento INVESTIGACION_MILLAJEM.md
"""
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from .models import CreditCard, EarningOpportunity, LoyaltyProgram
import json


def init_credit_cards(db: Session):
    """Inicializar tarjetas de crédito"""

    # Verificar si ya hay datos
    if db.query(CreditCard).count() > 0:
        print("Las tarjetas ya están inicializadas")
        return

    # Obtener IDs de programas
    amex_es = db.query(LoyaltyProgram).filter(LoyaltyProgram.name == "American Express Membership Rewards (ES)").first()
    iberia = db.query(LoyaltyProgram).filter(LoyaltyProgram.name == "Iberia Club").first()

    cards = [
        # ESPAÑA - PREMIUM
        {
            "name": "American Express Platinum España",
            "bank": "American Express",
            "country": "ES",
            "card_network": "Amex",
            "loyalty_program_id": amex_es.id if amex_es else None,
            "base_earning_rate": 1.0,  # 1 MR = 1 Avios
            "bonus_categories": json.dumps({"travel": 1.0, "restaurants": 1.0}),
            "annual_fee": 780.0,
            "currency": "EUR",
            "first_year_fee": 390.0,  # 50% descuento primer año
            "welcome_bonus": 120000,  # 60K + 60K tras gasto
            "welcome_bonus_requirement": "60K al obtenerla + 60K tras gastar 10,000 EUR en 3 meses",
            "minimum_income": 50000,
            "is_available": True,
            "application_url": "https://www.americanexpress.com/es/tarjetas-credito/the-platinum-card/",
            "notes": "Acceso Priority Pass, seguro viaje, protección compras. Mejor para alto gasto.",
            "recommendation_score": 85
        },
        {
            "name": "American Express Gold España",
            "bank": "American Express",
            "country": "ES",
            "card_network": "Amex",
            "loyalty_program_id": amex_es.id if amex_es else None,
            "base_earning_rate": 1.0,
            "bonus_categories": json.dumps({"restaurants": 1.0, "supermarkets": 1.0}),
            "annual_fee": 132.0,
            "currency": "EUR",
            "first_year_fee": 0.0,  # Gratis 6 meses
            "welcome_bonus": 20000,
            "welcome_bonus_requirement": "Tras primer gasto",
            "minimum_income": None,
            "is_available": True,
            "application_url": "https://www.americanexpress.com/es/tarjetas-credito/gold-card/",
            "notes": "MEJOR OPCIÓN para España. 1 MR = 1 Avios. Gratis 6 meses. Ideal gasto 2K-5K/mes.",
            "recommendation_score": 95  # MÁS RECOMENDADA
        },

        # ESPAÑA - COBRANDING IBERIA
        {
            "name": "Iberia Visa Infinite (Santander)",
            "bank": "Santander",
            "country": "ES",
            "card_network": "Visa",
            "loyalty_program_id": iberia.id if iberia else None,
            "base_earning_rate": 0.5,  # 0.5 Avios por EUR
            "bonus_categories": json.dumps({"iberia_flights": 2.0}),  # 2 Avios/EUR en Iberia
            "annual_fee": 48.0,
            "currency": "EUR",
            "first_year_fee": 0.0,
            "welcome_bonus": None,  # Variable según promoción
            "welcome_bonus_requirement": "Gasta 700 EUR en 30 días",
            "minimum_income": None,
            "is_available": True,
            "application_url": "https://www.iberiacards.es/",
            "notes": "200 Avios/mes fijos tras gasto mínimo. Complementaria a Amex.",
            "recommendation_score": 70
        },

        # GIBRALTAR - POTENCIAL
        {
            "name": "HSBC Premier World Elite Mastercard (Gibraltar)",
            "bank": "HSBC",
            "country": "GI",
            "card_network": "Mastercard",
            "loyalty_program_id": iberia.id if iberia else None,  # Asumiendo que gana Avios
            "base_earning_rate": 1.5,  # 1.5 Avios por GBP
            "bonus_categories": None,
            "annual_fee": 0.0,  # Incluida en HSBC Premier
            "currency": "GBP",
            "first_year_fee": 0.0,
            "welcome_bonus": None,
            "welcome_bonus_requirement": "Requiere HSBC Premier (£50K saldo o £75K ingreso)",
            "minimum_income": 75000,  # GBP
            "is_available": False,  # PENDIENTE VERIFICAR
            "application_url": None,
            "notes": "PENDIENTE CONFIRMAR: Visitar HSBC Gibraltar para verificar disponibilidad. Si disponible, mejor tarjeta GBP->Avios.",
            "recommendation_score": 90  # SI disponible
        },

        # BRASIL - PREMIUM
        {
            "name": "Santander Unique Infinite (Brasil)",
            "bank": "Santander",
            "country": "BR",
            "card_network": "Mastercard",
            "loyalty_program_id": None,  # Transfiere a Esfera
            "base_earning_rate": 2.2,  # 2.2 pontos por BRL
            "bonus_categories": None,
            "annual_fee": 1188.0,  # BRL/año
            "currency": "BRL",
            "first_year_fee": None,
            "welcome_bonus": 50000,
            "welcome_bonus_requirement": "Variable según promoción",
            "minimum_income": None,
            "is_available": True,
            "application_url": None,
            "notes": "Transfiere a Esfera 1:1. Con Esfera->Iberia 2:1 = 1.1 Avios/BRL efectivo.",
            "recommendation_score": 80
        },
        {
            "name": "Itaú Personnalité Mastercard Black (Brasil)",
            "bank": "Itaú",
            "country": "BR",
            "card_network": "Mastercard",
            "loyalty_program_id": None,
            "base_earning_rate": 2.1,
            "bonus_categories": None,
            "annual_fee": 1188.0,
            "currency": "BRL",
            "first_year_fee": None,
            "welcome_bonus": None,
            "welcome_bonus_requirement": None,
            "minimum_income": None,
            "is_available": True,
            "application_url": None,
            "notes": "Puntos Itaú -> Livelo o aerolíneas. Requiere cuenta Personnalité.",
            "recommendation_score": 75
        },
    ]

    for card_data in cards:
        card = CreditCard(**card_data)
        db.add(card)

    db.commit()
    print(f"{len(cards)} tarjetas inicializadas")


def init_earning_opportunities(db: Session):
    """Inicializar earning opportunities"""

    if db.query(EarningOpportunity).count() > 0:
        print("Las earning opportunities ya están inicializadas")
        return

    # Obtener IDs de programas
    iberia = db.query(LoyaltyProgram).filter(LoyaltyProgram.name == "Iberia Club").first()
    livelo = db.query(LoyaltyProgram).filter(LoyaltyProgram.name == "Livelo").first()
    esfera = db.query(LoyaltyProgram).filter(LoyaltyProgram.name == "Esfera").first()

    opportunities = [
        # ESPAÑA - COMBUSTIBLE
        {
            "name": "Cepsa 2 Avios",
            "category": "fuel",
            "country": "ES",
            "loyalty_program_id": iberia.id if iberia else None,
            "earning_rate": 2.0,  # Avios por litro
            "earning_description": "2 Avios por litro de combustible",
            "how_to_use": "Vincular tarjeta Iberia Club a cuenta Cepsa. Repostar en estaciones Cepsa.",
            "requirements": "Socio Iberia Club",
            "signup_url": "https://www.cepsa.es/",
            "more_info_url": "https://puntosviajeros.com/cepsa-avios/",
            "is_active": True,
            "notes": "Si repostas 40L/mes = 80 Avios/mes = 960 Avios/año",
            "recommendation_score": 85
        },

        # ESPAÑA - RIDESHARE
        {
            "name": "Cabify x Iberia",
            "category": "rideshare",
            "country": "ES",
            "loyalty_program_id": iberia.id if iberia else None,
            "earning_rate": 1.0,
            "earning_description": "1 Avios por EUR gastado",
            "how_to_use": "Vincular cuenta Cabify con Iberia Club desde la app Cabify",
            "requirements": "Socio Iberia Club",
            "signup_url": "https://cabify.com/",
            "more_info_url": None,
            "is_active": True,
            "notes": "Trayectos urbanos. Si gastas 50 EUR/mes = 600 Avios/año",
            "recommendation_score": 70
        },

        # ESPAÑA - SHOPPING PORTAL
        {
            "name": "Iberia Shopping",
            "category": "shopping_portal",
            "country": "ES",
            "loyalty_program_id": iberia.id if iberia else None,
            "earning_rate": 1.0,  # Variable según tienda
            "earning_description": "Hasta 5 Avios por EUR según tienda",
            "how_to_use": "Acceder a Iberia Shopping desde web/app Iberia. Comprar en tiendas afiliadas.",
            "requirements": "Socio Iberia Club",
            "signup_url": "https://shopping.iberia.com/",
            "more_info_url": None,
            "is_active": True,
            "notes": "Cientos de tiendas: Amazon, Booking, El Corte Inglés, etc.",
            "recommendation_score": 75
        },

        # BRASIL - SHOPPING
        {
            "name": "Livelo Shopping",
            "category": "shopping_portal",
            "country": "BR",
            "loyalty_program_id": livelo.id if livelo else None,
            "earning_rate": 1.5,  # Variable
            "earning_description": "1-5 pontos por BRL según tienda",
            "how_to_use": "Comprar a través del portal Livelo Shopping",
            "requirements": "Cuenta Livelo",
            "signup_url": "https://www.livelo.com.br/",
            "more_info_url": None,
            "is_active": True,
            "notes": "Cientos de lojas: Americanas, Magazine Luiza, Netshoes, etc.",
            "recommendation_score": 80
        },

        # BRASIL - SUPERMERCADOS
        {
            "name": "Pão de Açúcar (Grupo Éxito)",
            "category": "supermarket",
            "country": "BR",
            "loyalty_program_id": livelo.id if livelo else None,
            "earning_rate": 1.0,
            "earning_description": "1 ponto Livelo por BRL gastado",
            "how_to_use": "Vincular tarjeta de crédito participante o usar Cartão Pão de Açúcar",
            "requirements": None,
            "signup_url": None,
            "more_info_url": None,
            "is_active": True,
            "notes": "Compra diaria. Si gastas R$1000/mes = 12K pontos/año",
            "recommendation_score": 75
        },

        # BRASIL - DROGARIA
        {
            "name": "Droga Raia / Drogasil",
            "category": "pharmacy",
            "country": "BR",
            "loyalty_program_id": livelo.id if livelo else None,
            "earning_rate": 1.0,
            "earning_description": "1-2 pontos Livelo por BRL",
            "how_to_use": "Programa Sempre Bem. Vincular con Livelo.",
            "requirements": None,
            "signup_url": None,
            "more_info_url": None,
            "is_active": True,
            "notes": "Medicamentos, cosméticos, higiene",
            "recommendation_score": 70
        },

        # HOTELES - INTERNACIONAL
        {
            "name": "Accor Live Limitless",
            "category": "hotels",
            "country": "INT",
            "loyalty_program_id": db.query(LoyaltyProgram).filter(LoyaltyProgram.name == "Accor Live Limitless").first().id,
            "earning_rate": 10.0,  # Varía por nivel
            "earning_description": "10-20 puntos por EUR gastado (según nivel)",
            "how_to_use": "Reservar directamente en Accor.com o app con tu número de socio",
            "requirements": "Registro gratuito",
            "signup_url": "https://all.accor.com/",
            "more_info_url": None,
            "is_active": True,
            "notes": "MEJOR conversión hoteles->Avios 1:1. Marcas: Ibis, Novotel, Sofitel, Fairmont.",
            "recommendation_score": 90
        },
    ]

    for opp_data in opportunities:
        opp = EarningOpportunity(**opp_data)
        db.add(opp)

    db.commit()
    print(f"{len(opportunities)} earning opportunities inicializadas")


def main():
    """Main initialization function"""
    print("Inicializando recomendaciones...")

    # Crear tablas
    init_db()
    print("Tablas actualizadas")

    # Crear sesión
    db = SessionLocal()
    try:
        # Inicializar tarjetas
        init_credit_cards(db)

        # Inicializar earning opportunities
        init_earning_opportunities(db)

        print("Recomendaciones inicializadas correctamente")
    finally:
        db.close()


if __name__ == "__main__":
    main()
