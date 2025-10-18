from . import larkbase_client
from src.schemas.supplier import SupplierCreate
from src.core.config import settings

def db_create_supplier(supplier: SupplierCreate):
    fields = {
        "name": supplier.name,
        "contact_info": supplier.contact_info or ""
    }
    record = larkbase_client.create_record(settings.SUPPLIERS_TABLE_ID, fields)
    return {
        "id": record["record_id"],
        "name": record["fields"]["name"],
        "contact_info": record["fields"].get("contact_info", "")
    }

def db_get_all_suppliers():
    records = larkbase_client.get_records(
        settings.SUPPLIERS_TABLE_ID,
        sort=[{"field_name": "name", "desc": False}]
    )
    return [
        {
            "id": r["record_id"],
            "name": r["fields"]["name"],
            "contact_info": r["fields"].get("contact_info", "")
        }
        for r in records
    ]
