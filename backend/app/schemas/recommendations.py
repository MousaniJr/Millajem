from pydantic import BaseModel
from typing import Optional
from .program import LoyaltyProgram


class CreditCardBase(BaseModel):
    name: str
    bank: str
    country: str
    card_network: str
    base_earning_rate: float
    bonus_categories: Optional[str] = None
    annual_fee: float
    currency: str
    first_year_fee: Optional[float] = None
    welcome_bonus: Optional[int] = None
    welcome_bonus_requirement: Optional[str] = None
    minimum_income: Optional[int] = None
    is_available: bool
    application_url: Optional[str] = None
    image_url: Optional[str] = None
    notes: Optional[str] = None
    recommendation_score: int


class CreditCard(CreditCardBase):
    id: int
    loyalty_program: Optional[LoyaltyProgram] = None

    class Config:
        from_attributes = True


class EarningOpportunityBase(BaseModel):
    name: str
    category: str
    country: str
    earning_rate: float
    earning_description: str
    how_to_use: str
    requirements: Optional[str] = None
    signup_url: Optional[str] = None
    more_info_url: Optional[str] = None
    is_active: bool
    notes: Optional[str] = None
    recommendation_score: int


class EarningOpportunity(EarningOpportunityBase):
    id: int
    loyalty_program: Optional[LoyaltyProgram] = None

    class Config:
        from_attributes = True
