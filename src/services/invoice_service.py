from src.services.database import invoice as invoice_db
from src.schemas.invoice import InvoiceCreate

def create_invoice(invoice: InvoiceCreate):
    return invoice_db.db_create_invoice(invoice)

def get_all_invoices_by_plan_id(plan_id: int):
    # Sửa lại hàm này
    return invoice_db.db_get_all_invoices_by_plan_id(plan_id)