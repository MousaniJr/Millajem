"""
Modelo de fuentes de informacion (RSS feeds, webs oficiales, redes sociales)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Source(Base):
    """Fuente de informacion (RSS feed, cuenta social, landing promo, etc.)"""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)

    # Informacion basica
    name = Column(String, nullable=False)  # Nombre descriptivo
    source_type = Column(String, nullable=False)  # rss_feed, official_web, promo_landing, instagram, twitter, telegram
    country = Column(String, nullable=False)  # ES, BR, GI, INT

    # URLs
    url = Column(String, nullable=False, unique=True)  # Feed URL o pagina objetivo
    website_url = Column(String, nullable=True)  # Website principal (opcional)

    # Configuracion
    is_active = Column(Boolean, default=True)  # Si esta activo para scraping/seguimiento
    priority = Column(Integer, default=5)  # 1-10, mayor = mas importante

    # Metadata
    description = Column(String, nullable=True)  # Descripcion breve
    notes = Column(String, nullable=True)  # Notas adicionales
    last_verified_at = Column(DateTime, nullable=True)

    # Estadisticas
    last_scraped = Column(DateTime, nullable=True)  # Ultima vez que se scrapeo
    scrape_count = Column(Integer, default=0)  # Veces que se ha scrapeado
    alert_count = Column(Integer, default=0)  # Alertas generadas

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Source {self.name} ({self.source_type}) - {self.country}>"
