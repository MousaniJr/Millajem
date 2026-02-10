from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..database import Base


class Alert(Base):
    """Alerta de promoción enviada al usuario"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Alert info
    title = Column(String)
    message = Column(String)
    alert_type = Column(String)  # "promo_detected", "bonus_transfer", "purchase_bonus", "error_fare"

    # Priority
    priority = Column(String, default="normal")  # "low", "normal", "high", "urgent"

    # Status
    is_read = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    source_url = Column(String, nullable=True)
    source_type = Column(String, default="rss_blog")  # "rss_blog", "instagram", "twitter", "telegram", "manual"
    source_name = Column(String, nullable=True)  # Nombre específico del blog/cuenta
    related_program = Column(String, nullable=True)  # "Iberia", "Livelo", etc.
    country = Column(String, nullable=True)  # "ES", "BR", "INT"

    # Content
    full_content = Column(String, nullable=True)

    def __repr__(self):
        return f"<Alert {self.title}>"
