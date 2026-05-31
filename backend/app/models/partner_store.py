from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class PartnerStore(Base):
    """Tienda o partner de portal donde se pueden acumular puntos."""
    __tablename__ = "partner_stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    portal_name = Column(String, index=True, nullable=False)
    loyalty_program_id = Column(Integer, ForeignKey("loyalty_programs.id"), nullable=True)
    loyalty_program = relationship("LoyaltyProgram")

    base_rate = Column(Float, default=0)
    promo_rate = Column(Float, nullable=True)
    rate_unit = Column(String, default="per_currency")  # per_currency, per_booking, fixed_bonus
    supports_gift_card = Column(Boolean, default=False)
    supports_stacking = Column(Boolean, default=False)
    stacking_notes = Column(String, nullable=True)

    url = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    confidence = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<PartnerStore {self.name} via {self.portal_name}>"
