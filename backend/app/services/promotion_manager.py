"""
Gestor de promociones - coordina scraping y almacenamiento
"""
from sqlalchemy.orm import Session
from typing import List, Dict
from ..models import Alert
from .rss_scraper import RSSFeedScraper
from datetime import datetime, timedelta


class PromotionManager:
    """Gestor de promociones y alertas"""

    def __init__(self, db: Session):
        self.db = db
        self.scraper = RSSFeedScraper()

    def is_duplicate(self, title: str, source_url: str, hours: int = 48) -> bool:
        """Verificar si una alerta ya existe (últimas X horas)"""
        cutoff_date = datetime.utcnow() - timedelta(hours=hours)

        existing = self.db.query(Alert).filter(
            Alert.title == title,
            Alert.source_url == source_url,
            Alert.created_at >= cutoff_date
        ).first()

        return existing is not None

    def create_alert_from_entry(self, entry: Dict) -> Alert:
        """Crear una alerta a partir de una entrada scrapeada"""
        alert = Alert(
            title=entry["title"],
            message=entry["message"],
            alert_type=entry["alert_type"],
            priority=entry["priority"],
            source_url=entry["source_url"],
            related_program=entry["related_program"],
            country=entry["country"],
            full_content=entry["full_content"],
        )
        return alert

    def scan_and_save_promotions(self, min_relevance: int = 50) -> Dict:
        """Escanear feeds y guardar nuevas promociones"""
        print(f"Escaneando feeds RSS (relevancia mínima: {min_relevance})...")

        # Scrapear todos los feeds
        entries = self.scraper.scrape_all_feeds(min_relevance=min_relevance)

        new_alerts = 0
        duplicates = 0
        errors = 0

        for entry in entries:
            try:
                # Verificar si ya existe
                if self.is_duplicate(entry["title"], entry["source_url"]):
                    duplicates += 1
                    continue

                # Crear y guardar alerta
                alert = self.create_alert_from_entry(entry)
                self.db.add(alert)
                new_alerts += 1

            except Exception as e:
                print(f"Error guardando alerta: {e}")
                errors += 1

        # Commit todas las alertas
        if new_alerts > 0:
            self.db.commit()

        return {
            "scanned_entries": len(entries),
            "new_alerts": new_alerts,
            "duplicates": duplicates,
            "errors": errors,
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_top_promotions(self, limit: int = 10, country: str = None) -> List[Alert]:
        """Obtener las mejores promociones recientes"""
        query = self.db.query(Alert).filter(Alert.priority.in_(["high", "urgent"]))

        if country:
            query = query.filter(Alert.country == country)

        # Últimos 7 días
        cutoff = datetime.utcnow() - timedelta(days=7)
        query = query.filter(Alert.created_at >= cutoff)

        return query.order_by(Alert.created_at.desc()).limit(limit).all()

    def manual_scan_feed(self, feed_name: str, min_relevance: int = 40) -> Dict:
        """Escanear manualmente un feed específico"""
        entries = self.scraper.scrape_feed_by_name(feed_name, min_relevance)

        new_alerts = 0
        for entry in entries:
            if not self.is_duplicate(entry["title"], entry["source_url"]):
                alert = self.create_alert_from_entry(entry)
                self.db.add(alert)
                new_alerts += 1

        if new_alerts > 0:
            self.db.commit()

        return {
            "feed_name": feed_name,
            "new_alerts": new_alerts,
            "total_entries": len(entries)
        }
