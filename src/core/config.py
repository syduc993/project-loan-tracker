from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LARK_APP_ID: str
    LARK_APP_SECRET: str
    LARK_BASE_ID: str  # ID của Larkbase (bascnxxxxxxxxxx)
    
    # Table IDs cho các bảng
    SUPPLIERS_TABLE_ID: str
    DISBURSEMENT_PLANS_TABLE_ID: str
    INVOICES_TABLE_ID: str
    DISBURSEMENTS_TABLE_ID: str

    class Config:
        env_file = ".env"

settings = Settings()
