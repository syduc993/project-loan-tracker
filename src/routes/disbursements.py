from fastapi import APIRouter
from typing import List
from src.schemas.disbursement import DisbursementResponse, DisbursementCreate
from src.services.database import disbursement as disbursement_db

router = APIRouter()

# THAY ĐỔI: Endpoint lấy theo plan_id
@router.get("/plan/{plan_id}", response_model=List[DisbursementResponse])
def get_disbursements_for_plan(plan_id: int):
    return disbursement_db.db_get_disbursements_by_plan_id(plan_id)

@router.post("/", response_model=DisbursementResponse, status_code=201)
def create_new_disbursement(disbursement: DisbursementCreate):
    return disbursement_db.db_create_disbursement(disbursement)