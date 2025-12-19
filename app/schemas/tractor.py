from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.manufacturer import Manufacturer
# history.py 파일에 정의된 스키마 사용
from app.schemas.history import MaintenanceHistory

class FarmerInTractor(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class TractorBase(BaseModel):
    serial_number: str
    model: str
    release_date: Optional[datetime] = None
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
    owner_id: Optional[int] = None # DB 컬럼명 (owner_id)

class TractorCreate(TractorBase):
    pass

class Tractor(TractorBase):
    id: int
    current_hours: float = 0.0
    manufacturer: Optional[Manufacturer] = None 
    
    # [중요] 모델의 relationship 이름이 'owner'이므로 여기도 owner여야 데이터가 담깁니다.
    owner: Optional[FarmerInTractor] = None 
    
    # [핵심] 대시보드 매출용 정비 이력
    histories: List[MaintenanceHistory] = [] 

    class Config:
        from_attributes = True