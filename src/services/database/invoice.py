from . import larkbase_client
from src.schemas.invoice import InvoiceCreate
from src.core.config import settings

def db_create_invoice(invoice: InvoiceCreate):
    fields = {
        "plan_id": invoice.plan_id,
        "supplier_id": invoice.supplier_id,
        "invoice_number": invoice.invoice_number,
        "issue_date": invoice.issue_date.isoformat(),
        "total_value": float(invoice.total_value),
        "status": invoice.status
    }
    record = larkbase_client.create_record(settings.INVOICES_TABLE_ID, fields)
    return {
        "id": record["record_id"],
        "invoice_number": record["fields"]["invoice_number"],
        "issue_date": record["fields"]["issue_date"],
        "total_value": record["fields"]["total_value"],
        "supplier_id": record["fields"]["supplier_id"],
        "status": record["fields"]["status"]
    }

def db_get_all_invoices_by_plan_id(plan_id: int):
    # Lấy invoices
    filter_str = f'CurrentValue.[plan_id] = "{plan_id}"'
    invoices = larkbase_client.get_records(
        settings.INVOICES_TABLE_ID,
        filter_str=filter_str,
        sort=[{"field_name": "issue_date", "desc": True}]
    )
    
    # Lấy suppliers để join
    suppliers = larkbase_client.get_records(settings.SUPPLIERS_TABLE_ID)
    supplier_map = {s["record_id"]: s["fields"] for s in suppliers}
    
    result = []
    for inv in invoices:
        supplier_id = inv["fields"].get("supplier_id")
        supplier_data = None
        if supplier_id and supplier_id in supplier_map:
            supplier_data = {
                "id": supplier_id,
                "name": supplier_map[supplier_id]["name"]
            }
        
        result.append({
            "id": inv["record_id"],
            "invoice_number": inv["fields"]["invoice_number"],
            "issue_date": inv["fields"]["issue_date"],
            "total_value": inv["fields"]["total_value"],
            "supplier_id": supplier_id,
            "status": inv["fields"]["status"],
            "suppliers": supplier_data
        })
    
    return result
