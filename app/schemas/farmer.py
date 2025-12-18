from pydantic import BaseModel
from typing import Optional, List

# --- 트랙터 정보를 담기 위한 간이 스키마 (순환 참조 방지용) ---
class TractorInFarmer(BaseModel):
    id: int
    serial_number: str
    model: str
    current_hours: float
    # 트랙터 모델 안에 이력이 있다면 그것도 포함되도록 하려면 
    # 나중에 이 부분을 더 확장할 수 있습니다.
    
    class Config:
        from_attributes = True

# 1. 농민 등록 시 받을 데이터
class FarmerCreate(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None
    land_area: Optional[float] = 0.0
    main_crop: Optional[str] = None
    serial_number: Optional[str] = None 
     

# 2. API 응답 시 내보낼 데이터
class Farmer(FarmerCreate):
    id: int
    # [중요] 이 농민이 소유한 트랙터 목록을 포함시킵니다.
    # 이 필드가 있어야 프론트엔드에서 f.tractors를 읽을 수 있습니다.
    tractors: List[TractorInFarmer] = []

    class Config:
        from_attributes = True