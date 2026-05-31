from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoyaltyProgramBase(BaseModel):
    name: str
    currency: str
    country: str
    category: str
    avios_ratio: Optional[float] = None
    ratio_confidence: Optional[str] = None
    ratio_source_url: Optional[str] = None
    ratio_last_verified_at: Optional[datetime] = None
    website_url: Optional[str] = None
    login_url: Optional[str] = None
    is_enrolled: bool = False
    notes: Optional[str] = None


class LoyaltyProgramCreate(LoyaltyProgramBase):
    pass


class LoyaltyProgram(LoyaltyProgramBase):
    id: int

    class Config:
        from_attributes = True
