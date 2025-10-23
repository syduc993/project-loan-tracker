from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceWithSupplierResponse, InvoiceUpdate, InvoiceDetailResponse
from src.services.database import invoice as invoice_db
from src.services.database.base import get_db_session

router = APIRouter()


@router.get("/", response_model=List[InvoiceDetailResponse])
async def read_all_invoices(db: AsyncSession = Depends(get_db_session)):
    """Lấy danh sách tất cả hóa đơn."""
    return await invoice_db.db_get_all_invoices(db)

@router.post("/", response_model=InvoiceResponse, status_code=201)
async def create_new_invoice(
    invoice: InvoiceCreate,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        return await invoice_db.db_create_invoice(db, invoice)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/plan/{plan_id}", response_model=List[InvoiceWithSupplierResponse])
async def read_invoices_for_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    return await invoice_db.db_get_all_invoices_by_plan_id(db, plan_id)

@router.get("/{invoice_id}", response_model=InvoiceDetailResponse)
async def read_invoice_by_id(invoice_id: int, db: AsyncSession = Depends(get_db_session)):
    """API để lấy thông tin chi tiết của 1 hóa đơn."""
    db_invoice = await invoice_db.db_get_invoice_by_id(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice

@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_existing_invoice(
    invoice_id: int,
    invoice_in: InvoiceUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """API để cập nhật thông tin hóa đơn."""
    db_invoice = await invoice_db.db_get_invoice_by_id(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return await invoice_db.db_update_invoice(db, db_invoice=db_invoice, invoice_in=invoice_in)

@router.delete("/{invoice_id}", status_code=204)
async def delete_existing_invoice(invoice_id: int, db: AsyncSession = Depends(get_db_session)):
    """API để xóa hóa đơn."""
    db_invoice = await invoice_db.db_get_invoice_by_id(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    await invoice_db.db_delete_invoice(db, db_invoice=db_invoice)
    return None