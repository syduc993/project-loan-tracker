# File: src/core/app.py (ĐÃ SỬA LỖI)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Import routers
from src.routes import suppliers, invoices, pages, disbursement_plans, disbursements

# Import đối tượng templates từ file mới
from .templating import templates 

app = FastAPI(title="Project Loan Tracker")

# Xác định đường dẫn thư mục gốc
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 1. Mount thư mục static
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")



# 3. Gắn các API Routers (giữ nguyên)

app.include_router(suppliers.router, prefix="/api/v1/suppliers", tags=["Suppliers"])
app.include_router(invoices.router, prefix="/api/v1/invoices", tags=["Invoices"])
app.include_router(disbursement_plans.router, prefix="/api/v1/plans", tags=["Disbursement Plans"])
app.include_router(disbursements.router, prefix="/api/v1/disbursements", tags=["Disbursements"])


# 4. Gắn Page Router (phục vụ HTML - giữ nguyên)
app.include_router(pages.router, tags=["Web Pages"])