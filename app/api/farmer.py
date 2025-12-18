from fastapi import APIRouter, Depends, HTTPException , File , UploadFile
from sqlalchemy.orm import Session, joinedload # joinedload 추가!
from typing import List

from app.config import get_db
from app.models.farmer import Farmer as FarmerModel
from app.models.tractor import Tractor as TractorModel
from app.schemas.farmer import Farmer as FarmerSchema, FarmerCreate

import pandas as pd # 추가
import io # 추가

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

# ---------------------------------------------------------
# [신규 추가] 2. 엑셀 대량 업로드 (405 에러 해결용)
# ---------------------------------------------------------
@router.post("/upload-excel")
async def upload_farmers_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # 엑셀 파일 읽기
        contents = await file.read()
        # 브로가 만든 random_farmers_master.xlsx를 읽습니다.
        df = pd.read_excel(io.BytesIO(contents))

        success_count = 0
        for _, row in df.iterrows():
            # 1) 농민 데이터 생성 (기존 모델 필드명에 맞춤)
            new_farmer = FarmerModel(
                name=str(row['name']),
                phone=str(row['phone']),
                address=str(row['address']),
                land_area=float(row.get('land_area', 0)),
                main_crop=str(row['main_crop'])
            )
            db.add(new_farmer)
            db.flush()  # 신규 농민 ID(PK)를 즉시 따오기 위해 사용

            # 2) 트랙터 매칭 (기존 코드 로직과 동일)
            # 엑셀 컬럼명 'serial_number'를 사용합니다.
            sn = str(row.get('serial_number', '')).strip()
            if sn:
                target_tractor = db.query(TractorModel).filter(TractorModel.serial_number == sn).first()
                if target_tractor:
                    target_tractor.owner_id = new_farmer.id  # 기존 코드의 필드명 owner_id 확인
                    db.add(target_tractor)
                    success_count += 1

        db.commit()
        return {"message": f"성공적으로 {success_count}명의 농민을 등록하고 트랙터와 연동했습니다."}

    except Exception as e:
        db.rollback()
        print(f"Excel Upload Error: {e}")
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")



# 2. 농민 목록 조회 (여기서 joinedload를 추가해야 목록/모달에서 이력이 보임)
@router.get("/", response_model=List[FarmerSchema])
def read_farmers(skip: int = 0, limit: int = 99999, db: Session = Depends(get_db)):
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