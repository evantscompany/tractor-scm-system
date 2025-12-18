from pydantic import BaseModel
from typing import Optional,List

#농민 등록시 받을 데이터
class FarmerCreate(BaseModel):
    name : str
    phone : str
    address : Optional[str] = None
    land_area : Optional[float] = 0.0
    main_crop : Optional[str]= None

#API 응답 시 내보낼 데이터(ID 포함)
class Farmer(FarmerCreate):
    id : int
    
    class Config:
        from_attributes = True # SQLAlchemy 모델을 Pydantic 으로 변환 허용