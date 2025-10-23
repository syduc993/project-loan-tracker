from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Base class cho ORM models
Base = declarative_base()

# --- BẮT ĐẦU PHẦN SỬA LỖI ---

# 1. Lấy URL từ file config ra một biến tạm
db_url = settings.DATABASE_URL

# 2. Kiểm tra xem biến DATABASE_URL có được thiết lập hay không
if not db_url:
    raise ValueError("Lỗi: Biến DATABASE_URL chưa được thiết lập trong file .env")

# 3. Kiểm tra và tự động sửa chuỗi kết nối để sử dụng driver asyncpg
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    logger.info("Chuỗi kết nối đã được tự động cấu hình để sử dụng driver asyncpg.")

# --- KẾT THÚC PHẦN SỬA LỖI ---


# Tạo async engine với chuỗi kết nối đã được xử lý
engine = create_async_engine(
    db_url,  # <-- Sử dụng biến db_url đã được sửa
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False,
    future=True
)

# Session factory (Phần này giữ nguyên)
AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    """Dependency để inject database session vào routes"""
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()