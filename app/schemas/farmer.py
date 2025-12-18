from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 1. 정비 이력을 담을 상세 스키마 (TractorInFarmer보다 위에 있어야 함)
class MaintenanceInFarmer(BaseModel):
    id: int
    category: str
    description: Optional[str] = None
    hours_at_event: Optional[float] = None
    event_date: Optional[datetime] = None

    class Config:
        from_attributes = True

# 2. 농민 정보에 포함될 트랙터 스키마 (여기에 histories 추가!)
class TractorInFarmer(BaseModel):
    id: int
    serial_number: str
    model: str
    current_hours: float
    # [핵심] 정비 이력 목록을 추가합니다.
    histories: List[MaintenanceInFarmer] = [] 
    
    class Config:
        from_attributes = True

# 3. 농민 등록 시 받을 데이터
class FarmerCreate(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None
    land_area: Optional[float] = 0.0
    main_crop: Optional[str] = None
    serial_number: Optional[str] = None 

# 4. API 응답 시 내보낼 데이터 (최종)
class Farmer(FarmerCreate):
    id: int
    # 이제 이 tractors[] 안의 각 트랙터는 histories[]를 품고 나갑니다.
    tractors: List[TractorInFarmer] = []

    class Config:
        from_attributes = True