from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List
from app.schemas.manufacturer import Manufacturer

# 1. 트랙터 조회 시 농민의 이름과 연락처만 살짝 담아줄 스키마
class FarmerInTractor(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class TractorBase(BaseModel):
    serial_number: str
    model: str
    release_date: Optional[datetime] = None # datetime 오류 방지를 위해 Optional 권장
    arrival_date: Optional[datetime] = None
    price: Optional[float] = None
    tax_rate: float = 0.0
    base_price: float = 0.0
    location: str = "KOREA"
    status: str = "STOCK"
    export_date: Optional[datetime] = None
    
    attachment_type: Optional[str] = None
    horsepower: Optional[int] = None
    manufacturer_id: int
    owner: Optional[int] = None # DB의 외래키 값

class TractorCreate(TractorBase):
    pass

class Tractor(TractorBase):
    id: int
    current_hours: float = 0.0 # 가동시간도 표시하기 위해 추가
    manufacturer: Optional[Manufacturer] = None 
    
    # 2. [핵심] 이 트랙터의 주인(농민) 정보를 포함시킵니다.
    # 모델(models/tractor.py)의 relationship 이름이 'farmer'라면 이대로 쓰시면 됩니다.
    farmer: Optional[FarmerInTractor] = None 
    histories: List[MaintenanceHistorySchema]=[]
    class Config:
        from_attributes = True

class MaintenanceHistorySchema(BaseModel):
    id: int
    category: str
    description: Optional[str] = None
    hours_at_event: Optional[float] = None
    event_date: Optional[datetime] = None

    class Config:
        from_attributes = True