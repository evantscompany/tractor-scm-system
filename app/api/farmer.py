from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload # joinedload 추가!
from typing import List

from app.config import get_db
from app.models.farmer import Farmer as FarmerModel
from app.models.tractor import Tractor as TractorModel
from app.schemas.farmer import Farmer as FarmerSchema, FarmerCreate

router = APIRouter(prefix="/farmers", tags=["Farmers"])

# 1. 농민 등록 (기존과 동일)
@router.post("/", response_model=FarmerSchema)
def create_farmer(farmer_in: FarmerCreate, db: Session = Depends(get_db)):
    new_farmer = FarmerModel(
        name=farmer_in.name,
        phone=farmer_in.phone,
        address=farmer_in.address,
        land_area=farmer_in.land_area,
        main_crop=farmer_in.main_crop
    )
    db.add(new_farmer)
    db.flush()

    if farmer_in.serial_number:
        target_tractor = db.query(TractorModel).filter(TractorModel.serial_number == farmer_in.serial_number).first()
        if target_tractor:
            target_tractor.owner_id = new_farmer.id
            db.add(target_tractor)
        else:
            db.rollback()
            raise HTTPException(status_code=400, detail="입력하신 시리얼 번호의 트랙터가 없습니다.")

    db.commit()
    db.refresh(new_farmer)
    return new_farmer

# 2. 농민 목록 조회 (여기서 joinedload를 추가해야 목록/모달에서 이력이 보임)
@router.get("/", response_model=List[FarmerSchema])
def read_farmers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(FarmerModel).options(
        joinedload(FarmerModel.tractors).joinedload(TractorModel.histories) # 중첩 로딩 적용
    ).offset(skip).limit(limit).all()

# 3. 상세 조회 (모델명 변수 불일치 수정)
@router.get("/{farmer_id}")
def get_farmer_detail(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.query(FarmerModel).options(
        joinedload(FarmerModel.tractors).joinedload(TractorModel.histories)
    ).filter(FarmerModel.id == farmer_id).first()
    
    if not farmer:
        raise HTTPException(status_code=404, detail="농민을 찾을 수 없음")
    return farmer