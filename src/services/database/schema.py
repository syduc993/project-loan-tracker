from sqlalchemy import Column, BigInteger, Text, Date, Numeric, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .base import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    contact_info = Column(Text)
    created_at = Column(Date, server_default=func.now())
    
    # Relationship
    invoices = relationship("Invoice", back_populates="supplier")


class DisbursementPlan(Base):
    __tablename__ = "disbursement_plans"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    periodic_interest_day = Column(Integer, default=25)  # ← THÊM DÒNG NÀY
    created_at = Column(Date, server_default=func.now())
    actual_date = Column(Date)              # Ngày thực tế vay
    principal_due_date = Column(Date)       # Ngày đáo hạn
    bank_name = Column(Text)                # (Nên thêm cả thông tin ngân hàng ở đây)
    loan_contract_number = Column(Text)     # (Và số hợp đồng)

    # Relationships
    invoices = relationship("Invoice", back_populates="plan", cascade="all, delete-orphan")
    disbursements = relationship("Disbursement", back_populates="plan", cascade="all, delete-orphan")


class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    plan_id = Column(BigInteger, ForeignKey("disbursement_plans.id", ondelete="CASCADE"))
    supplier_id = Column(BigInteger, ForeignKey("suppliers.id", ondelete="SET NULL"))
    invoice_number = Column(Text, nullable=False)
    issue_date = Column(Date, nullable=False)
    total_value = Column(Numeric(15, 2), nullable=False)
    status = Column(Text, default="Chưa thanh toán")
    created_at = Column(Date, server_default=func.now())
    
    # Relationships
    plan = relationship("DisbursementPlan", back_populates="invoices")
    supplier = relationship("Supplier", back_populates="invoices")


class Disbursement(Base):
    __tablename__ = "disbursements"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    plan_id = Column(BigInteger, ForeignKey("disbursement_plans.id", ondelete="CASCADE"))
    
    interest_due_date = Column(Date)  # Ngày phải trả lãi (quan trọng nhất)
    interest_amount = Column(Numeric(15, 2)) # Số tiền lãi (tính sau)
    actual_date = Column(Date) # Có thể dùng cột này để lưu NGÀY THỰC TẾ ĐÃ TRẢ
    
    created_at = Column(Date, server_default=func.now())
    
    # Relationships
    plan = relationship("DisbursementPlan", back_populates="disbursements")