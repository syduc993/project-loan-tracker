from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from src.core.app import templates

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