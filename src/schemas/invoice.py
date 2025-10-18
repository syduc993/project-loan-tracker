from pydantic import BaseModel
from datetime import date
from .supplier import SupplierResponse

class InvoiceBase(BaseModel):
    invoice_number: str
    issue_date: date
    total_value: float
    supplier_id: int
    status: str = "Chưa thanh toán"

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: int

    class Config:
        from_attributes = True

class InvoiceWithSupplierResponse(InvoiceResponse):
    suppliers: SupplierResponse | None = None