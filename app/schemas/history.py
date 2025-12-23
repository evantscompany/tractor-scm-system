from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#이력 등록 시 받을 데이터

class MaintenanceHistoryCreate(BaseModel):
    tractor_id : int
    category : str   #repair, education, checkup 등
    description : Optional[str] = None
    cost: Optional[float] = 0.0
    hours_at_event: Optional[float]=0.0


class MaintenanceHistory(MaintenanceHistoryCreate):
    id : int
    event_date : datetime

    class Config:
        from_attributes =True