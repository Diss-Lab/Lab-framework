from pydantic import BaseModel
from typing import Optional
import datetime

class UsageLogBase(BaseModel):
    resource_type: str  # "equipment" or "material"
    resource_id: int
    action: str  # start_use/end_use/consume/maintenance
    quantity_used: Optional[float] = None
    duration_minutes: Optional[int] = None
    purpose: Optional[str] = None
    notes: Optional[str] = None
    issues_reported: Optional[str] = None
    project_name: Optional[str] = None
    auto_recorded: Optional[bool] = False

class UsageLogCreate(UsageLogBase):
    pass

class UsageLogRead(UsageLogBase):
    id: int
    user_id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
