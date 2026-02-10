from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Balance(Base):
    """Saldo en un programa de fidelidad"""
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("loyalty_programs.id"))

    # Balance info
    points = Column(Float)  # Cantidad de puntos/millas/avios
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Metadata
    notes = Column(String, nullable=True)

    # Relationship
    program = relationship("LoyaltyProgram")

    def __repr__(self):
        return f"<Balance {self.program.name}: {self.points:,.0f}>"
