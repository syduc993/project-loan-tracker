# File: src/core/templating.py

from fastapi.templating import Jinja2Templates
from pathlib import Path

# Xác định đường dẫn thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Khởi tạo đối tượng templates ở đây
templates = Jinja2Templates(directory=BASE_DIR / "templates")