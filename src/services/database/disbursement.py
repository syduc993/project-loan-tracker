from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .schema import Disbursement, DisbursementPlan  # Import cả hai
from src.schemas.disbursement import DisbursementCreate, DisbursementUpdate
from src.utils.interest_calculator import generate_interest_payment_dates
from datetime import date
from typing import List, Optional

# ==============================================================================
# HÀM TẠO LỊCH TRẢ LÃI TỰ ĐỘNG (ĐÃ VIẾT LẠI THEO LOGIC MỚI)
# ==============================================================================

async def generate_interest_schedule(
    db: AsyncSession,
    plan_id: int  # <-- THAY ĐỔI: Dùng plan_id
) -> dict:
    """
    Tạo lịch trả lãi tự động cho một Kế Hoạch Giải Ngân
    
    Args:
        db: Database session
        plan_id: ID của Kế Hoạch (DisbursementPlan)
    
    Returns:
        dict với thông tin kết quả
    """
    
    # 1. Lấy thông tin Kế Hoạch (Plan)
    result = await db.execute(
        select(DisbursementPlan).where(DisbursementPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    
    if not plan:
        return {
            "success": False,
            "message": f"Không tìm thấy Kế hoạch (plan) với id={plan_id}",
            "schedules_created": 0,
            "schedule_dates": []
        }
    
    # 2. Kiểm tra các trường bắt buộc TRÊN PLAN
    if not plan.actual_date or not plan.principal_due_date:
        return {
            "success": False,
            "message": "Kế hoạch này phải có 'Ngày thực tế vay' và 'Ngày đáo hạn (trả gốc)'",
            "schedules_created": 0,
            "schedule_dates": []
        }
    
    # 3. Lấy ngày trả lãi định kỳ từ plan
    periodic_interest_day = plan.periodic_interest_day
    
    # 4. Xóa các dòng trả lãi cũ (nếu có) để tạo lại
    old_schedules_result = await db.execute(
        select(Disbursement).where(Disbursement.plan_id == plan_id)
    )
    old_schedules = old_schedules_result.scalars().all()
    
    count_deleted = 0
    for old_schedule in old_schedules:
        await db.delete(old_schedule)
        count_deleted += 1
    
    # 5. Tính toán các ngày trả lãi
    payment_dates = generate_interest_payment_dates(
        actual_date=plan.actual_date,
        principal_due_date=plan.principal_due_date,
        periodic_day=periodic_interest_day
    )
    
    if not payment_dates:
        return {
            "success": False,
            "message": "Không thể tạo lịch trả lãi (ngày vay >= ngày trả nợ gốc)",
            "schedules_created": 0,
            "schedule_dates": []
        }
    
    # 6. Tạo các dòng disbursement (lịch lãi)
    # Giả định schema.py đã được sửa, bảng Disbursement giờ RẤT đơn giản
    created_schedules = []
    for payment_date in payment_dates:
        new_schedule = Disbursement(
            plan_id=plan.id,
            interest_due_date=payment_date, # Dùng cột mới `interest_due_date`
            interest_amount=None,           # Tiền lãi sẽ được cập nhật sau
            actual_date=None                # Ngày thực trả sẽ được cập nhật sau
        )
        db.add(new_schedule)
        created_schedules.append(new_schedule)
    
    await db.commit() # Commit để lưu các thay đổi
    
    return {
        "success": True,
        "message": f"Đã xóa {count_deleted} lịch cũ. Đã tạo {len(payment_dates)} kỳ trả lãi mới thành công.",
        "schedules_created": len(payment_dates),
        "schedule_dates": payment_dates
    }

# ==============================================================================
# HÀM XÓA LỊCH (CŨNG ĐƯỢC VIẾT LẠI THEO LOGIC MỚI)
# ==============================================================================

async def delete_interest_schedule(db: AsyncSession, plan_id: int) -> dict: # <-- THAY ĐỔI
    """
    Xóa tất cả lịch trả lãi của một Kế Hoạch
    
    Args:
        db: Database session
        plan_id: ID của Kế Hoạch (DisbursementPlan)
    
    Returns:
        dict với thông tin kết quả
    """
    result = await db.execute(
        select(Disbursement).where(Disbursement.plan_id == plan_id) # <-- THAY ĐỔI
    )
    schedules = result.scalars().all()
    
    count = len(schedules)
    for schedule in schedules:
        await db.delete(schedule)
    
    await db.commit()
    
    return {
        "success": True,
        "message": f"Đã xóa {count} kỳ trả lãi",
        "schedules_deleted": count
    }


# ==============================================================================
# CÁC HÀM CRUD CƠ BẢN (ĐÃ CẬP NHẬT THEO LOGIC MỚI)
# ==============================================================================

async def db_create_disbursement(db: AsyncSession, disbursement: DisbursementCreate):
    """
    Tạo một dòng lịch sử trả lãi (thường là thủ công, không dùng hàm tự động)
    LƯU Ý: schema `DisbursementCreate` cần được cập nhật
    """
    # Hàm này giờ sẽ nhận schema create mới
    # (schema.py cho DisbursementCreate cũng cần được sửa)
    new_disbursement = Disbursement(**disbursement.model_dump())
    db.add(new_disbursement)
    await db.flush()
    await db.refresh(new_disbursement)
    return new_disbursement

async def db_get_disbursements_by_plan_id(db: AsyncSession, plan_id: int):
    """Lấy tất cả các kỳ trả lãi của một kế hoạch."""
    result = await db.execute(
        select(Disbursement)
        .where(Disbursement.plan_id == plan_id)
        .order_by(Disbursement.interest_due_date) # Sắp xếp theo ngày trả lãi
    )
    return result.scalars().all()

async def db_get_disbursement_by_id(db: AsyncSession, disbursement_id: int) -> Disbursement | None:
    """Lấy một kỳ trả lãi theo ID."""
    result = await db.execute(select(Disbursement).where(Disbursement.id == disbursement_id))
    return result.scalars().first()

async def db_update_disbursement(db: AsyncSession, db_disbursement: Disbursement, disbursement_in: DisbursementUpdate) -> Disbursement:
    """
    Cập nhật thông tin một kỳ trả lãi (ví dụ: cập nhật số tiền đã trả)
    LƯU Ý: schema `DisbursementUpdate` cần được cập nhật
    """
    update_data = disbursement_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_disbursement, key, value)
    
    await db.flush()
    await db.refresh(db_disbursement)
    return db_disbursement

async def db_delete_disbursement(db: AsyncSession, db_disbursement: Disbursement):
    """Xóa một kỳ trả lãi cụ thể."""
    await db.delete(db_disbursement)
    await db.flush()