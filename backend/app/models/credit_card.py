from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class CreditCard(Base):
    """Tarjeta de crédito para acumular puntos"""
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)

    # Información básica
    name = Column(String, index=True)  # "American Express Gold España"
    bank = Column(String)  # "American Express", "Santander", "Itaú"
    country = Column(String)  # "ES", "BR", "GI"
    card_network = Column(String)  # "Amex", "Visa", "Mastercard"

    # Programa de fidelidad asociado
    loyalty_program_id = Column(Integer, ForeignKey("loyalty_programs.id"))
    loyalty_program = relationship("LoyaltyProgram")

    # Earning rate
    base_earning_rate = Column(Float)  # Puntos por EUR/BRL/GBP (ej: 1.0 = 1 punto por moneda)
    bonus_categories = Column(String, nullable=True)  # JSON string: {"restaurants": 2.0, "travel": 3.0}

    # Costes
    annual_fee = Column(Float)  # Cuota anual
    currency = Column(String)  # "EUR", "BRL", "GBP"
    first_year_fee = Column(Float, nullable=True)  # Si es diferente (ej: gratis primer año)

    # Beneficios
    welcome_bonus = Column(Integer, nullable=True)  # Puntos de bienvenida
    welcome_bonus_requirement = Column(String, nullable=True)  # "Gasta 3000 EUR en 3 meses"

    # Requisitos
    minimum_income = Column(Integer, nullable=True)  # Ingreso mínimo anual
    is_available = Column(Boolean, default=True)  # Si está disponible actualmente

    # URLs y metadata
    application_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    # Ranking (para ordenar recomendaciones)
    recommendation_score = Column(Integer, default=50)  # 0-100

    def __repr__(self):
        return f"<CreditCard {self.name}>"
