from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..services.promotion_manager import PromotionManager
from ..services.rss_scraper import RSSFeedScraper
from ..services.social_scraper import SocialMediaScraper, SOCIAL_MEDIA_SETUP_GUIDE

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.post("/scan")
def scan_promotions(
    min_relevance: int = Query(50, ge=0, le=100),
    db: Session = Depends(get_db)
):
    """Escanear manualmente todos los feeds RSS y guardar promociones"""
    manager = PromotionManager(db)
    result = manager.scan_and_save_promotions(min_relevance=min_relevance)
    return result


@router.post("/scan/{feed_name}")
def scan_specific_feed(
    feed_name: str,
    min_relevance: int = Query(40, ge=0, le=100),
    db: Session = Depends(get_db)
):
    """Escanear un feed específico"""
    manager = PromotionManager(db)
    result = manager.manual_scan_feed(feed_name, min_relevance)
    return result


@router.get("/feeds")
def list_available_feeds():
    """Listar feeds RSS disponibles"""
    scraper = RSSFeedScraper()
    return {
        "spanish_feeds": scraper.SPANISH_FEEDS,
        "brazilian_feeds": scraper.BRAZILIAN_FEEDS,
        "total": len(scraper.feeds)
    }


@router.get("/top")
def get_top_promotions(
    limit: int = Query(10, ge=1, le=50),
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener las mejores promociones recientes"""
    manager = PromotionManager(db)
    alerts = manager.get_top_promotions(limit=limit, country=country)

    return [
        {
            "id": alert.id,
            "title": alert.title,
            "message": alert.message,
            "alert_type": alert.alert_type,
            "priority": alert.priority,
            "source_url": alert.source_url,
            "related_program": alert.related_program,
            "country": alert.country,
            "created_at": alert.created_at.isoformat(),
            "is_read": alert.is_read,
            "is_favorite": alert.is_favorite,
        }
        for alert in alerts
    ]


@router.get("/social-accounts")
def get_social_media_accounts(country: Optional[str] = None):
    """Obtener cuentas de redes sociales recomendadas para seguir"""
    scraper = SocialMediaScraper()
    recommendations = scraper.get_manual_social_recommendations()

    if country:
        recommendations = [r for r in recommendations if r["country"] == country]

    return {
        "recommendations": recommendations,
        "setup_guide": SOCIAL_MEDIA_SETUP_GUIDE,
        "total": len(recommendations)
    }
