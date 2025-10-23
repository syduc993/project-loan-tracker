from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .schema import Supplier
from src.schemas.supplier import SupplierCreate, SupplierUpdate

async def db_create_supplier(db: AsyncSession, supplier: SupplierCreate):
    new_supplier = Supplier(**supplier.model_dump())
    db.add(new_supplier)
    await db.flush()
    await db.refresh(new_supplier)
    return new_supplier

async def db_get_all_suppliers(db: AsyncSession):
    result = await db.execute(select(Supplier).order_by(Supplier.id))
    return result.scalars().all()

async def db_get_supplier_by_id(db: AsyncSession, supplier_id: int) -> Supplier | None:
    """Lấy một nhà cung cấp theo ID."""
    result = await db.execute(select(Supplier).where(Supplier.id == supplier_id))
    return result.scalars().first()

async def db_update_supplier(db: AsyncSession, db_supplier: Supplier, supplier_in: SupplierUpdate) -> Supplier:
    """Cập nhật thông tin nhà cung cấp."""
    update_data = supplier_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_supplier, key, value)
    
    await db.flush()
    await db.refresh(db_supplier)
    return db_supplier

async def db_delete_supplier(db: AsyncSession, db_supplier: Supplier):
    """Xóa một nhà cung cấp."""
    await db.delete(db_supplier)
    await db.flush()