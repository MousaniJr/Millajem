from sqlalchemy import Column, Integer, String, Float
from ..database import Base


class LoyaltyProgram(Base):
    """Programa de fidelidad (Iberia Club, Livelo, etc.)"""
    __tablename__ = "loyalty_programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # "Iberia Club", "Livelo", etc.
    currency = Column(String)  # "Avios", "Pontos", "Miles"
    country = Column(String)  # "ES", "BR", "GI"
    category = Column(String)  # "airline", "hotel", "transfer", "shopping"

    # Transfer rates (to Avios)
    avios_ratio = Column(Float, nullable=True)  # Ratio de conversión a Avios (null si no aplica)

    # URLs
    website_url = Column(String, nullable=True)
    login_url = Column(String, nullable=True)

    # Metadata
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<LoyaltyProgram {self.name} ({self.currency})>"
