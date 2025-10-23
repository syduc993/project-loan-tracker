from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.disbursement_plan import DisbursementPlanResponse, DisbursementPlanCreate, DisbursementPlanUpdate
from src.schemas.disbursement import GenerateInterestScheduleResponse
from src.services.database import disbursement_plan as plan_db
from src.services.database.base import get_db_session
from src.services.database.disbursement import generate_interest_schedule, delete_interest_schedule

router = APIRouter()

@router.get("", response_model=List[DisbursementPlanResponse])
async def get_all_disbursement_plans(db: AsyncSession = Depends(get_db_session)):
    return await plan_db.db_get_all_disbursement_plans(db)

@router.post("", response_model=DisbursementPlanResponse, status_code=201)
async def create_new_disbursement_plan(
    plan: DisbursementPlanCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """API để tạo kế hoạch mới."""
    return await plan_db.db_create_disbursement_plan(db, plan)

@router.post("/{plan_id}/generate-interest-schedule", response_model=GenerateInterestScheduleResponse)
async def create_interest_schedule_for_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Tạo lịch trả lãi tự động cho toàn bộ Kế hoạch."""
    result = await generate_interest_schedule(db=db, plan_id=plan_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return GenerateInterestScheduleResponse(**result)

@router.delete("/{plan_id}/interest-schedule")
async def remove_interest_schedule_for_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Xóa tất cả lịch trả lãi của một Kế hoạch."""
    result = await delete_interest_schedule(db=db, plan_id=plan_id)
    return result


@router.get("/{plan_id}", response_model=DisbursementPlanResponse)
async def read_plan_by_id(plan_id: int, db: AsyncSession = Depends(get_db_session)):
    """API để lấy thông tin chi tiết của 1 kế hoạch."""
    db_plan = await plan_db.db_get_plan_by_id(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Disbursement plan not found")
    return db_plan

@router.put("/{plan_id}", response_model=DisbursementPlanResponse)
async def update_existing_plan(
    plan_id: int,
    plan_in: DisbursementPlanUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """API để cập nhật thông tin kế hoạch."""
    db_plan = await plan_db.db_get_plan_by_id(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Disbursement plan not found")
    
    return await plan_db.db_update_plan(db, db_plan=db_plan, plan_in=plan_in)

@router.delete("/{plan_id}", status_code=204)
async def delete_existing_plan(plan_id: int, db: AsyncSession = Depends(get_db_session)):
    """API để xóa kế hoạch."""
    db_plan = await plan_db.db_get_plan_by_id(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Disbursement plan not found")
    
    await plan_db.db_delete_plan(db, db_plan=db_plan)
    return None