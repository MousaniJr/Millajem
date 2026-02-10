from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .program import LoyaltyProgram


class BalanceBase(BaseModel):
    program_id: int
    points: float
    notes: Optional[str] = None


class BalanceCreate(BalanceBase):
    pass


class BalanceUpdate(BaseModel):
    points: float
    notes: Optional[str] = None


class Balance(BalanceBase):
    id: int
    last_updated: datetime
    program: LoyaltyProgram

    class Config:
        from_attributes = True
