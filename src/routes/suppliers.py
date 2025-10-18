from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.supplier import SupplierCreate, SupplierResponse
from src.services import supplier_service

router = APIRouter()

@router.post("/", response_model=SupplierResponse, status_code=201)
def create_new_supplier(supplier: SupplierCreate):
    try:
        return supplier_service.create_supplier(supplier)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[SupplierResponse])
def read_all_suppliers():
    return supplier_service.get_all_suppliers()