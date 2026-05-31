from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database import Base


class EarningOpportunity(Base):
    """Oportunidad para ganar puntos (shopping portals, fuel, dining, etc.)"""
    __tablename__ = "earning_opportunities"

    id = Column(Integer, primary_key=True, index=True)

    # Informacion basica
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
    how_to_use = Column(String)  # Instrucciones de como usarlo
    requirements = Column(String, nullable=True)  # "Tarjeta Iberia", "Socio Iberia Club"

    # URLs
    signup_url = Column(String, nullable=True)
    more_info_url = Column(String, nullable=True)
    source_url = Column(String, nullable=True)  # Fuente de validacion principal

    # Vigencia y verificacion
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    last_verified_at = Column(DateTime, nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True)
    notes = Column(String, nullable=True)

    # Ranking / calidad de dato
    recommendation_score = Column(Integer, default=50)  # 0-100
    confidence = Column(String, nullable=True)  # "official", "inferred", "stale"

    def __repr__(self):
        return f"<EarningOpportunity {self.name}>"
