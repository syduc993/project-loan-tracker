from src.services.database import supplier as supplier_db
from src.schemas.supplier import SupplierCreate

def create_supplier(supplier: SupplierCreate):
    return supplier_db.db_create_supplier(supplier)

def get_all_suppliers():
    return supplier_db.db_get_all_suppliers()