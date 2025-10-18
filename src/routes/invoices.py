from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceWithSupplierResponse
from src.services import invoice_service

router = APIRouter()

@router.post("/", response_model=InvoiceResponse, status_code=201)
def create_new_invoice(invoice: InvoiceCreate):
    try:
        return invoice_service.create_invoice(invoice)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Sửa lại endpoint này để khớp với frontend
@router.get("/plan/{plan_id}", response_model=List[InvoiceWithSupplierResponse])
def read_invoices_for_plan(plan_id: int):
    return invoice_service.get_all_invoices_by_plan_id(plan_id)