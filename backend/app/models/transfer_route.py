from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class TransferRoute(Base):
    """Ruta de transferencia entre programas con bonos base o temporales."""
    __tablename__ = "transfer_routes"

    id = Column(Integer, primary_key=True, index=True)
    source_program_id = Column(Integer, ForeignKey("loyalty_programs.id"), nullable=False)
    target_program_id = Column(Integer, ForeignKey("loyalty_programs.id"), nullable=False)
    source_program = relationship("LoyaltyProgram", foreign_keys=[source_program_id])
    target_program = relationship("LoyaltyProgram", foreign_keys=[target_program_id])

    base_ratio = Column(Float, nullable=False)  # source points needed for 1 target point
    typical_bonus_min = Column(Float, nullable=True)
    typical_bonus_max = Column(Float, nullable=True)
    current_bonus = Column(Float, nullable=True)
    bonus_end_date = Column(DateTime, nullable=True)

    source_url = Column(String, nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    confidence = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<TransferRoute {self.source_program_id}->{self.target_program_id}>"
