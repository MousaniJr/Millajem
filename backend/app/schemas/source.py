"""
Schemas Pydantic para fuentes de informacion
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SourceBase(BaseModel):
    """Schema base para Source"""
    name: str
    source_type: str  # rss_feed, official_web, promo_landing, instagram, twitter, telegram
    country: str  # ES, BR, GI, INT
    url: str
    website_url: Optional[str] = None
    is_active: bool = True
    priority: int = 5  # 1-10
    description: Optional[str] = None
    notes: Optional[str] = None
    last_verified_at: Optional[datetime] = None


class SourceCreate(SourceBase):
    """Schema para crear Source"""
    pass


class SourceUpdate(BaseModel):
    """Schema para actualizar Source (todos los campos opcionales)"""
    name: Optional[str] = None
    source_type: Optional[str] = None
    country: Optional[str] = None
    url: Optional[str] = None
    website_url: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    last_verified_at: Optional[datetime] = None


class Source(SourceBase):
    """Schema completo de Source (con ID y timestamps)"""
    id: int
    last_scraped: Optional[datetime] = None
    scrape_count: int = 0
    alert_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
