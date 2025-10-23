"""
Helper functions để tính toán lịch trả lãi
"""
from datetime import date, timedelta
from typing import List


def get_next_business_day(target_date: date) -> date:
    """
    Nếu ngày rơi vào thứ 7 (5) hoặc Chủ nhật (6), chuyển sang thứ 2
    
    Args:
        target_date: Ngày cần kiểm tra
    
    Returns:
        Ngày thứ 2 kế tiếp nếu là cuối tuần, nguyên ngày nếu không
    """
    # weekday(): 0=Monday, 1=Tuesday, ..., 5=Saturday, 6=Sunday
    while target_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        target_date += timedelta(days=1)
    return target_date


def generate_interest_payment_dates(
    actual_date: date,
    principal_due_date: date,
    periodic_day: int = 25
) -> List[date]:
    """
    Sinh ra các ngày trả lãi hàng tháng
    
    Logic:
    1. Nếu ngày giải ngân >= 15 → bỏ qua tháng đó, bắt đầu từ tháng sau
    2. Mỗi tháng trả vào ngày `periodic_day` (mặc định 25)
    3. Nếu rơi thứ 7/CN → chuyển sang thứ 2
    4. Tháng cuối: dùng `principal_due_date` thay vì ngày periodic_day
    
    Args:
        actual_date: Ngày thực tế giải ngân
        principal_due_date: Ngày đến hạn trả nợ gốc
        periodic_day: Ngày trả lãi hàng tháng (1-31)
    
    Returns:
        List các ngày trả lãi đã điều chỉnh
    """
    if actual_date >= principal_due_date:
        return []
    
    payment_dates = []
    current_month_start = actual_date.replace(day=1)
    
    # Rule 1: Nếu ngày giải ngân >= 15 → bắt đầu từ tháng sau
    if actual_date.day >= 15:
        # Sang tháng sau
        if current_month_start.month == 12:
            current_month_start = current_month_start.replace(year=current_month_start.year + 1, month=1)
        else:
            current_month_start = current_month_start.replace(month=current_month_start.month + 1)
    
    # Tạo lịch trả lãi từng tháng
    while True:
        # Tạo ngày trả lãi cho tháng hiện tại
        try:
            payment_date = current_month_start.replace(day=periodic_day)
        except ValueError:
            # Tháng không có ngày periodic_day (VD: tháng 2 có 28/29 ngày mà periodic_day=30)
            # → Lấy ngày cuối tháng
            if current_month_start.month == 12:
                next_month = current_month_start.replace(year=current_month_start.year + 1, month=1)
            else:
                next_month = current_month_start.replace(month=current_month_start.month + 1)
            payment_date = next_month - timedelta(days=1)
        
        # Rule 4: Tháng cuối → dùng principal_due_date
        if payment_date.year == principal_due_date.year and payment_date.month == principal_due_date.month:
            payment_date = principal_due_date
            payment_dates.append(payment_date)
            break
        
        # Nếu vượt quá ngày trả nợ gốc → dừng
        if payment_date > principal_due_date:
            break
        
        # Rule 3: Điều chỉnh nếu rơi thứ 7/CN (trừ tháng cuối)
        payment_date = get_next_business_day(payment_date)
        payment_dates.append(payment_date)
        
        # Sang tháng tiếp theo
        if current_month_start.month == 12:
            current_month_start = current_month_start.replace(year=current_month_start.year + 1, month=1)
        else:
            current_month_start = current_month_start.replace(month=current_month_start.month + 1)
    
    return payment_dates