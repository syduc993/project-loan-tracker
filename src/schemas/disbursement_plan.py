from pydantic import BaseModel

class DisbursementPlanBase(BaseModel):
    name: str
    description: str | None = None

class DisbursementPlanCreate(DisbursementPlanBase):
    pass

class DisbursementPlanResponse(DisbursementPlanBase):
    id: int
    class Config:
        from_attributes = True