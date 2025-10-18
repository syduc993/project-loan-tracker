from src.services.database import disbursement_plan as plan_db

def get_all_plans():
    return plan_db.db_get_all_disbursement_plans()