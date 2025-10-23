# File: src/schemas/disbursement.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime # <-- Thêm 'datetime' vào đây
from decimal import Decimal


class DisbursementBase(BaseModel):
    plan_id: int
    planned_date: Optional[date] = None
    planned_amount: Optional[Decimal] = None
    actual_date: Optional[date] = None
    actual_amount: Optional[Decimal] = None
    bank_name: Optional[str] = None
    loan_contract_number: Optional[str] = None
    loan_term_months: Optional[int] = None
    loan_interest_rate: Optional[float] = None
    interest_amount: Optional[Decimal] = None
    interest_due_date: Optional[date] = None
    principal_due_date: Optional[date] = None
    parent_disbursement_id: Optional[int] = None


class DisbursementCreate(DisbursementBase):
    pass


class DisbursementUpdate(BaseModel):
    planned_date: Optional[date] = None
    planned_amount: Optional[Decimal] = None
    actual_date: Optional[date] = None
    actual_amount: Optional[Decimal] = None
    bank_name: Optional[str] = None
    loan_contract_number: Optional[str] = None
    loan_term_months: Optional[int] = None
    loan_interest_rate: Optional[float] = None
    interest_amount: Optional[Decimal] = None
    interest_due_date: Optional[date] = None
    principal_due_date: Optional[date] = None
    parent_disbursement_id: Optional[int] = None


class DisbursementResponse(DisbursementBase):
    id: int
    # SỬA DÒNG NÀY: Chuyển từ 'date' sang 'datetime'
    created_at: datetime 

    class Config:
        from_attributes = True


class GenerateInterestScheduleRequest(BaseModel):
    """Request để tạo lịch trả lãi"""
    disbursement_id: int
    periodic_interest_day: Optional[int] = Field(None, ge=1, le=31, description="Ngày trả lãi hàng tháng (1-31). Nếu null thì lấy từ plan")


class GenerateInterestScheduleResponse(BaseModel):
    """Response sau khi tạo lịch trả lãi"""
    success: bool
    message: str
    schedules_created: int
    schedule_dates: list[date]