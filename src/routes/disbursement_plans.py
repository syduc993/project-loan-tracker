from fastapi import APIRouter
from typing import List
from src.schemas.disbursement_plan import DisbursementPlanResponse
import src.plan_service as plan_service

router = APIRouter()

@router.get("", response_model=List[DisbursementPlanResponse])
def get_all_disbursement_plans():
    """
    API endpoint để lấy tất cả các kế hoạch giải ngân.
    Đây là API mà main.js sẽ gọi đầu tiên.
    """
    return plan_service.get_all_plans()