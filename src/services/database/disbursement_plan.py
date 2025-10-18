from . import larkbase_client
from src.core.config import settings

def db_get_all_disbursement_plans():
    records = larkbase_client.get_records(
        settings.DISBURSEMENT_PLANS_TABLE_ID,
        sort=[{"field_name": "name", "desc": False}]
    )
    return [
        {
            "id": r["record_id"],
            "name": r["fields"]["name"],
            "description": r["fields"].get("description", "")
        }
        for r in records
    ]
