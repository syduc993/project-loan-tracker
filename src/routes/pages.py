# File: src/routes/pages.py (ĐÃ SỬA LỖI)

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
# Sửa dòng import này: thay vì từ src.core.app, hãy import từ file mới
from src.core.templating import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Trang chủ - Quản lý Hóa đơn"
        }
    )