from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

# Lớp cơ sở chứa các trường chung của một hóa đơn
class InvoiceBase(BaseModel):
    plan_id: int
    supplier_id: int
    invoice_number: str
    issue_date: date
    total_value: float

# Schema dùng để TẠO MỚI một hóa đơn (dữ liệu đầu vào)
class InvoiceCreate(InvoiceBase):
    pass # Kế thừa tất cả các trường từ InvoiceBase





# Schema dùng để TRẢ VỀ sau khi tạo mới hoặc lấy một hóa đơn
class InvoiceResponse(InvoiceBase):
    id: int
    status: str

    # Cấu hình để Pydantic có thể đọc dữ liệu từ object SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class SupplierResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str

class InvoiceWithSupplierResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    invoice_number: str
    issue_date: date
    total_value: float
    supplier_id: int
    status: str
    # Mối quan hệ này cho phép trả về thông tin của nhà cung cấp kèm theo hóa đơn
    supplier: Optional[SupplierResponse] = None

class InvoiceUpdate(BaseModel):
    plan_id: int | None = None         # Bổ sung cho phép sửa plan_id nếu cần
    supplier_id: int | None = None
    invoice_number: str | None = None
    issue_date: date | None = None
    total_value: float | None = None
    status: str | None = None


# Schema rút gọn cho Supplier khi hiển thị trong Invoice
class SupplierRef(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

# Schema rút gọn cho Plan khi hiển thị trong Invoice
class PlanRef(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

# Schema Invoice đầy đủ thông tin cho trang danh sách
class InvoiceDetailResponse(InvoiceResponse):
    supplier: Optional[SupplierRef] = None
    plan: Optional[PlanRef] = None