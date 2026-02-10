"""
Modelo de fuentes de información (RSS feeds, redes sociales)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Source(Base):
    """Fuente de información (RSS feed, cuenta social, etc.)"""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)

    # Información básica
    name = Column(String, nullable=False)  # Nombre descriptivo
    source_type = Column(String, nullable=False)  # "rss_feed", "instagram", "twitter", "telegram"
    country = Column(String, nullable=False)  # "ES", "BR", "GI", "INT"

    # URLs
    url = Column(String, nullable=False, unique=True)  # Feed URL o perfil URL
    website_url = Column(String, nullable=True)  # Website principal (opcional)

    # Configuración
    is_active = Column(Boolean, default=True)  # Si está activo para scraping
    priority = Column(Integer, default=5)  # 1-10, mayor = más importante

    # Metadata
    description = Column(String, nullable=True)  # Descripción breve
    notes = Column(String, nullable=True)  # Notas adicionales

    # Estadísticas
    last_scraped = Column(DateTime, nullable=True)  # Última vez que se scrapeo
    scrape_count = Column(Integer, default=0)  # Veces que se ha scrapeado
    alert_count = Column(Integer, default=0)  # Alertas generadas

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Source {self.name} ({self.source_type}) - {self.country}>"
