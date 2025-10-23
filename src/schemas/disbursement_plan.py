from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date # Thêm 'date' vào đây

class DisbursementPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    periodic_interest_day: int = Field(default=25, ge=1, le=31)
    actual_date: Optional[date] = None
    principal_due_date: Optional[date] = None
    bank_name: Optional[str] = None
    loan_contract_number: Optional[str] = None


class DisbursementPlanCreate(DisbursementPlanBase):
    pass

class DisbursementPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    periodic_interest_day: Optional[int] = Field(None, ge=1, le=31)
    actual_date: Optional[date] = None
    principal_due_date: Optional[date] = None
    bank_name: Optional[str] = None
    loan_contract_number: Optional[str] = None

class DisbursementPlanResponse(DisbursementPlanBase):
    id: int
    created_at: datetime  

    class Config:
        from_attributes = True