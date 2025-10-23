from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.disbursement import DisbursementResponse, DisbursementCreate, DisbursementUpdate
from src.services.database import disbursement as disbursement_db
from src.services.database.base import get_db_session

router = APIRouter()

@router.get("/plan/{plan_id}", response_model=List[DisbursementResponse])
async def get_disbursements_for_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    return await disbursement_db.db_get_disbursements_by_plan_id(db, plan_id)

@router.post("/", response_model=DisbursementResponse, status_code=201)
async def create_new_disbursement(
    disbursement: DisbursementCreate,
    db: AsyncSession = Depends(get_db_session)
):
    return await disbursement_db.db_create_disbursement(db, disbursement)

@router.get("/{disbursement_id}", response_model=DisbursementResponse)
async def read_disbursement_by_id(disbursement_id: int, db: AsyncSession = Depends(get_db_session)):
    """API để lấy thông tin chi tiết của 1 lần giải ngân."""
    db_disbursement = await disbursement_db.db_get_disbursement_by_id(db, disbursement_id=disbursement_id)
    if db_disbursement is None:
        raise HTTPException(status_code=404, detail="Disbursement not found")
    return db_disbursement

@router.put("/{disbursement_id}", response_model=DisbursementResponse)
async def update_existing_disbursement(
    disbursement_id: int,
    disbursement_in: DisbursementUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """API để cập nhật thông tin giải ngân."""
    db_disbursement = await disbursement_db.db_get_disbursement_by_id(db, disbursement_id=disbursement_id)
    if db_disbursement is None:
        raise HTTPException(status_code=404, detail="Disbursement not found")
    
    return await disbursement_db.db_update_disbursement(db, db_disbursement=db_disbursement, disbursement_in=disbursement_in)

@router.delete("/{disbursement_id}", status_code=204)
async def delete_existing_disbursement(disbursement_id: int, db: AsyncSession = Depends(get_db_session)):
    """API để xóa một lần giải ngân."""
    db_disbursement = await disbursement_db.db_get_disbursement_by_id(db, disbursement_id=disbursement_id)
    if db_disbursement is None:
        raise HTTPException(status_code=404, detail="Disbursement not found")
    
    await disbursement_db.db_delete_disbursement(db, db_disbursement=db_disbursement)
    return None