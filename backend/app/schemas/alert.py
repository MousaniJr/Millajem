from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertBase(BaseModel):
    title: str
    message: str
    alert_type: str
    priority: str = "normal"
    source_url: Optional[str] = None
    source_type: str = "rss_blog"
    source_name: Optional[str] = None
    related_program: Optional[str] = None
    country: Optional[str] = None
    confidence: Optional[str] = None
    last_verified_at: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    detected_bonus_percentage: Optional[float] = None
    full_content: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    is_read: bool
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True
