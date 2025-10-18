from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Import routers
from src.routes import suppliers, invoices, pages, disbursement_plans, disbursements

app = FastAPI(title="Project Loan Tracker")

# Xác định đường dẫn thư mục gốc
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 1. Mount thư mục static
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 2. Cấu hình Jinja2Templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# 3. Gắn các API Routers (thêm các router còn thiếu)
app.include_router(suppliers.router, prefix="/api/v1/suppliers", tags=["Suppliers"])
app.include_router(invoices.router, prefix="/api/v1/invoices", tags=["Invoices"])
app.include_router(disbursement_plans.router, prefix="/api/v1/plans", tags=["Disbursement Plans"])
app.include_router(disbursements.router, prefix="/api/v1/disbursements", tags=["Disbursements"])


# 4. Gắn Page Router (phục vụ HTML)
app.include_router(pages.router, tags=["Web Pages"])