from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Promotion(Base):
    """Promoción de transferencia o compra de puntos"""
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)

    # Promotion info
    title = Column(String)
    description = Column(String, nullable=True)
    promotion_type = Column(String)  # "transfer_bonus", "purchase_bonus", "earning_multiplier"

    # Programs involved
    source_program_id = Column(Integer, ForeignKey("loyalty_programs.id"), nullable=True)
    target_program_id = Column(Integer, ForeignKey("loyalty_programs.id"), nullable=True)

    # Bonus details
    bonus_percentage = Column(Float, nullable=True)  # e.g., 50.0 for 50% bonus
    base_ratio = Column(Float, nullable=True)  # e.g., 2.0 for 2:1
    effective_ratio = Column(Float, nullable=True)  # ratio con bonus incluido

    # Validity
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Source
    source_url = Column(String, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    source_program = relationship("LoyaltyProgram", foreign_keys=[source_program_id])
    target_program = relationship("LoyaltyProgram", foreign_keys=[target_program_id])

    def __repr__(self):
        return f"<Promotion {self.title}>"
