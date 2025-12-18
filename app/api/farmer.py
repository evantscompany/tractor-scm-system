from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db
# 1. 모델과 스키마를 명확히 구분해서 임포트
from app.models.farmer import Farmer as FarmerModel
from app.models.tractor import Tractor as TractorModel
from app.schemas.farmer import Farmer as FarmerSchema, FarmerCreate

router = APIRouter(prefix="/farmers", tags=["Farmers"])

@router.post("/", response_model=FarmerSchema)
def create_farmer(farmer_in: FarmerCreate, db: Session = Depends(get_db)):
    # 1. 농민 생성 (Model 사용)
    new_farmer = FarmerModel(
        name=farmer_in.name,
        phone=farmer_in.phone,
        address=farmer_in.address,
        land_area=farmer_in.land_area,
        main_crop=farmer_in.main_crop
    )
    db.add(new_farmer)
    db.flush()  # DB에 임시 반영하여 new_farmer.id를 생성받음

    # 2. 트랙터 연동
    if farmer_in.serial_number:
        # 트랙터 테이블에서 해당 S/N을 찾음
        target_tractor = db.query(TractorModel).filter(TractorModel.serial_number == farmer_in.serial_number).first()
        
        if target_tractor:
            # 트랙터의 owner_id를 방금 만든 농민 ID로 업데이트
            target_tractor.owner_id = new_farmer.id
            db.add(target_tractor)
        else:
            db.rollback()
            raise HTTPException(status_code=400, detail="입력하신 시리얼 번호의 트랙터가 없습니다.")

    db.commit()
    db.refresh(new_farmer)
    return new_farmer

@router.get("/", response_model=List[FarmerSchema])
def read_farmers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(FarmerModel).offset(skip).limit(limit).all()