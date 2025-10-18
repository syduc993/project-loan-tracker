from . import larkbase_client
from src.schemas.disbursement import DisbursementCreate
from src.core.config import settings

def db_create_disbursement(disbursement: DisbursementCreate):
    fields = {
        "plan_id": disbursement.plan_id,
        "planned_date": disbursement.planned_date.isoformat() if disbursement.planned_date else None,
        "planned_amount": float(disbursement.planned_amount) if disbursement.planned_amount else None,
        "actual_date": disbursement.actual_date.isoformat() if disbursement.actual_date else None,
        "actual_amount": float(disbursement.actual_amount) if disbursement.actual_amount else None,
        "bank_name": disbursement.bank_name,
        "loan_contract_number": disbursement.loan_contract_number,
        "loan_term_months": disbursement.loan_term_months,
        "loan_interest_rate": disbursement.loan_interest_rate,
        "interest_amount": float(disbursement.interest_amount) if disbursement.interest_amount else None,
        "interest_due_date": disbursement.interest_due_date.isoformat() if disbursement.interest_due_date else None,
        "principal_due_date": disbursement.principal_due_date.isoformat() if disbursement.principal_due_date else None
    }
    
    # Loại bỏ các field None
    fields = {k: v for k, v in fields.items() if v is not None}
    
    record = larkbase_client.create_record(settings.DISBURSEMENTS_TABLE_ID, fields)
    return _convert_disbursement_record(record)

def db_get_disbursements_by_plan_id(plan_id: int):
    filter_str = f'CurrentValue.[plan_id] = "{plan_id}"'
    records = larkbase_client.get_records(
        settings.DISBURSEMENTS_TABLE_ID,
        filter_str=filter_str,
        sort=[{"field_name": "actual_date", "desc": False}]
    )
    return [_convert_disbursement_record(r) for r in records]

def _convert_disbursement_record(record):
    fields = record["fields"]
    return {
        "id": record["record_id"],
        "plan_id": fields.get("plan_id"),
        "planned_date": fields.get("planned_date"),
        "planned_amount": fields.get("planned_amount"),
        "actual_date": fields.get("actual_date"),
        "actual_amount": fields.get("actual_amount"),
        "bank_name": fields.get("bank_name"),
        "loan_contract_number": fields.get("loan_contract_number"),
        "loan_term_months": fields.get("loan_term_months"),
        "loan_interest_rate": fields.get("loan_interest_rate"),
        "interest_amount": fields.get("interest_amount"),
        "interest_due_date": fields.get("interest_due_date"),
        "principal_due_date": fields.get("principal_due_date")
    }
