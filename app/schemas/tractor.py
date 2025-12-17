from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.manufacturer import Manufacturer

class TractorBase(BaseModel):
    serial_number: str
    model: str
    release_date: datetime
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

class TractorCreate(TractorBase):
    pass

class Tractor(TractorBase):
    id: int
    manufacturer: Optional[Manufacturer] = None  # 관계를 통해 제조사 상세 정보 포함

    class Config:
        from_attributes = True