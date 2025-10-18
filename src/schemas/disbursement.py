from pydantic import BaseModel, Field
from datetime import date

class DisbursementBase(BaseModel):
    plan_id: int
    planned_date: date | None = None
    planned_amount: float | None = Field(None, gt=0)
    actual_date: date | None = None
    actual_amount: float | None = Field(None, gt=0)
    bank_name: str | None = None
    loan_contract_number: str | None = None
    loan_term_months: int | None = Field(None, gt=0)
    loan_interest_rate: float | None = Field(None, ge=0, le=1)
    interest_amount: float | None = Field(None, ge=0)
    interest_due_date: date | None = None
    principal_due_date: date | None = None

class DisbursementCreate(DisbursementBase):
    pass

class DisbursementResponse(DisbursementBase):
    id: int
    class Config:
        from_attributes = True