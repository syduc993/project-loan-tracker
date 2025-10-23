from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schema import Invoice, Supplier
from src.schemas.invoice import InvoiceCreate, InvoiceUpdate



async def db_get_all_invoices(db: AsyncSession):
    """Lấy tất cả hóa đơn kèm thông tin NCC và Kế hoạch."""
    result = await db.execute(
        select(Invoice)
        .options(
            selectinload(Invoice.supplier),
            selectinload(Invoice.plan)
        )
        .order_by(Invoice.issue_date.desc())
    )
    return result.scalars().all()


async def db_create_invoice(db: AsyncSession, invoice: InvoiceCreate):
    new_invoice = Invoice(**invoice.model_dump())
    db.add(new_invoice)
    await db.flush()
    await db.refresh(new_invoice)
    return new_invoice

async def db_get_all_invoices_by_plan_id(db: AsyncSession, plan_id: int):
    result = await db.execute(
        select(Invoice)
        .options(selectinload(Invoice.supplier))
        .where(Invoice.plan_id == plan_id)
        .order_by(Invoice.issue_date.desc())
    )
    return result.scalars().all()

async def db_get_invoice_by_id(db: AsyncSession, invoice_id: int) -> Invoice | None:
    result = await db.execute(
        select(Invoice)
        .options(
            selectinload(Invoice.supplier),
            selectinload(Invoice.plan)
        )
        .where(Invoice.id == invoice_id)
    )
    return result.scalars().first()

async def db_update_invoice(db: AsyncSession, db_invoice: Invoice, invoice_in: InvoiceUpdate) -> Invoice:
    """Cập nhật thông tin hóa đơn."""
    update_data = invoice_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_invoice, key, value)
    
    await db.flush()
    await db.refresh(db_invoice)
    return db_invoice

async def db_delete_invoice(db: AsyncSession, db_invoice: Invoice):
    """Xóa một hóa đơn."""
    await db.delete(db_invoice)
    await db.flush()