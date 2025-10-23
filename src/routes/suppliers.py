from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate
from src.services.database import supplier as supplier_db
from src.services.database.base import get_db_session

router = APIRouter()

@router.post("/", response_model=SupplierResponse, status_code=201)
async def create_new_supplier(
    supplier: SupplierCreate,
    db: AsyncSession = Depends(get_db_session)
):
    try:
        return await supplier_db.db_create_supplier(db, supplier)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[SupplierResponse])
async def read_all_suppliers(db: AsyncSession = Depends(get_db_session)):
    return await supplier_db.db_get_all_suppliers(db)

@router.get("/{supplier_id}", response_model=SupplierResponse)
async def read_supplier_by_id(supplier_id: int, db: AsyncSession = Depends(get_db_session)):
    """API để lấy thông tin chi tiết của 1 nhà cung cấp."""
    db_supplier = await supplier_db.db_get_supplier_by_id(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.put("/{supplier_id}", response_model=SupplierResponse)
async def update_existing_supplier(
    supplier_id: int,
    supplier_in: SupplierUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """API để cập nhật thông tin nhà cung cấp."""
    db_supplier = await supplier_db.db_get_supplier_by_id(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    return await supplier_db.db_update_supplier(db, db_supplier=db_supplier, supplier_in=supplier_in)

@router.delete("/{supplier_id}", status_code=204)
async def delete_existing_supplier(supplier_id: int, db: AsyncSession = Depends(get_db_session)):
    """API để xóa nhà cung cấp."""
    db_supplier = await supplier_db.db_get_supplier_by_id(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    await supplier_db.db_delete_supplier(db, db_supplier=db_supplier)
    # Status 204 No Content không trả về body
    return None

# --- KẾT THÚC PHẦN BỔ SUNG ---