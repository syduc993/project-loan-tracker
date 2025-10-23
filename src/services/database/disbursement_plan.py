from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .schema import DisbursementPlan
from src.schemas.disbursement_plan import DisbursementPlanCreate, DisbursementPlanUpdate

async def db_get_all_disbursement_plans(db: AsyncSession):
    result = await db.execute(
        select(DisbursementPlan).order_by(DisbursementPlan.name)
    )
    return result.scalars().all()

async def db_create_disbursement_plan(db: AsyncSession, plan: DisbursementPlanCreate) -> DisbursementPlan:
    """Tạo một kế hoạch giải ngân mới."""
    new_plan = DisbursementPlan(**plan.model_dump())
    db.add(new_plan)
    await db.flush()
    await db.refresh(new_plan)
    return new_plan

async def db_get_plan_by_id(db: AsyncSession, plan_id: int) -> DisbursementPlan | None:
    """Lấy một kế hoạch theo ID."""
    result = await db.execute(select(DisbursementPlan).where(DisbursementPlan.id == plan_id))
    return result.scalars().first()

async def db_update_plan(db: AsyncSession, db_plan: DisbursementPlan, plan_in: DisbursementPlanUpdate) -> DisbursementPlan:
    """Cập nhật thông tin kế hoạch."""
    update_data = plan_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plan, key, value)
    
    await db.flush()
    await db.refresh(db_plan)
    return db_plan

async def db_delete_plan(db: AsyncSession, db_plan: DisbursementPlan):
    """Xóa một kế hoạch."""
    await db.delete(db_plan)
    await db.flush()