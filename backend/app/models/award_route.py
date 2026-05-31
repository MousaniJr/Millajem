from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class AwardRoute(Base):
    """Referencia de emisión para un viaje objetivo."""
    __tablename__ = "award_routes"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String, index=True, nullable=False)
    origin = Column(String, index=True, nullable=False)
    destination = Column(String, index=True, nullable=False)
    region = Column(String, index=True, nullable=True)
    cabin = Column(String, index=True, nullable=False)

    program_id = Column(Integer, ForeignKey("loyalty_programs.id"), nullable=False)
    program = relationship("LoyaltyProgram")
    operating_airlines = Column(String, nullable=True)
    alliance = Column(String, nullable=True)
    table_type = Column(String, nullable=True)  # fixed, dynamic, partner
    booking_channel = Column(String, nullable=True)  # web, call_center, whatsapp

    points_one_way = Column(Float, nullable=True)
    taxes_estimate = Column(Float, nullable=True)
    taxes_currency = Column(String, nullable=True)
    baggage_included = Column(Boolean, default=False)
    change_policy = Column(String, nullable=True)
    cancellation_policy = Column(String, nullable=True)
    stopover_allowed = Column(Boolean, default=False)
    upgrade_allowed = Column(Boolean, default=False)
    family_booking_notes = Column(String, nullable=True)
    recommended_booking_window = Column(String, nullable=True)

    source_url = Column(String, nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    confidence = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<AwardRoute {self.route_name} {self.cabin}>"
