from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.manufacturer import Manufacturer
# 브로의 history.py 파일에서 정의된 클래스를 가져옵니다.
from app.schemas.history import MaintenanceHistory

# 1. 트랙터 조회 시 농민 정보를 담을 스키마
class FarmerInTractor(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True

# 2. 트랙터 기본 구조
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
    owner: Optional[int] = None 

class TractorCreate(TractorBase):
    pass

# 3. 최종 반환용 트랙터 스키마 (대시보드 매출 해결사)
class Tractor(TractorBase):
    id: int
    current_hours: float = 0.0
    manufacturer: Optional[Manufacturer] = None 
    
    # [핵심] Dashboard.js가 t.histories를 찾으므로 리스트 이름을 histories로 유지합니다.
    # history.py의 MaintenanceHistory 스키마를 리스트 형태로 담습니다.
    histories: List[MaintenanceHistory] = [] 
    
    # 농민 정보 연동
    farmer: Optional[FarmerInTractor] = None 

    class Config:
        from_attributes = True