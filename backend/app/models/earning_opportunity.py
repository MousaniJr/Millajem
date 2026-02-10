from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base


class EarningOpportunity(Base):
    """Oportunidad para ganar puntos (shopping portals, fuel, dining, etc.)"""
    __tablename__ = "earning_opportunities"

    id = Column(Integer, primary_key=True, index=True)

    # Información básica
    name = Column(String, index=True)  # "Cepsa 2 Avios", "Cabify Iberia", "Livelo Shopping"
    category = Column(String)  # "fuel", "rideshare", "shopping_portal", "dining", "hotels"
    country = Column(String)  # "ES", "BR", "INT"

    # Programa asociado
    loyalty_program_id = Column(Integer, ForeignKey("loyalty_programs.id"))
    loyalty_program = relationship("LoyaltyProgram")

    # Earning
    earning_rate = Column(Float)  # Puntos por EUR/BRL gastado
    earning_description = Column(String)  # "2 Avios por litro", "1 punto por EUR"

    # Detalles
    how_to_use = Column(String)  # Instrucciones de cómo usarlo
    requirements = Column(String, nullable=True)  # "Tarjeta Iberia", "Socio Iberia Club"

    # URLs
    signup_url = Column(String, nullable=True)
    more_info_url = Column(String, nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True)
    notes = Column(String, nullable=True)

    # Ranking
    recommendation_score = Column(Integer, default=50)  # 0-100

    def __repr__(self):
        return f"<EarningOpportunity {self.name}>"
