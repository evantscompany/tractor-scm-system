from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session, joinedload
import pandas as pd
import io
from app.config import get_db
from app.models.tractor import Tractor
from app.models.manufacturer import Manufacturer

router = APIRouter(prefix="/tractors", tags=["tractors"])

# 1. 조회 기능 (제조사 포함)
@router.get("/")
def get_tractors(db: Session = Depends(get_db)):
    return db.query(Tractor).options(joinedload(Tractor.manufacturer)).all()

# 2. 엑셀 업로드 기능 (에러 방지 문법 적용)
@router.post("/upload/")
@router.post("/upload-excel")
async def upload_tractors(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
        
        for _, row in df.iterrows():
            # 제조사 이름 가져오기
            m_name = str(row.get('manufacturer_name', row.get('제조사', '기타')))
            
            # 제조사 DB 확인 및 생성
            m_obj = db.query(Manufacturer).filter(Manufacturer.name == m_name).first()
            if not m_obj:
                m_obj = Manufacturer(name=m_name)
                db.add(m_obj)
                db.flush() 

            # 트랙터 객체 생성 (괄호와 콤마 위치를 확인하세요!)
            new_tractor = Tractor(
                serial_number=str(row.get('serial_number', row.get('시리얼번호'))),
                model=str(row.get('model', row.get('모델명'))),
                manufacturer_id=m_obj.id, 
                horsepower=int(row.get('horsepower', 0)),
                base_price=float(row.get('base_price', 0)),
                tax_rate=float(row.get('tax_rate', 0)),
                price=float(row.get('base_price', 0)) * (1 + float(row.get('tax_rate', 0))/100),
                location=str(row.get('location', 'KOREA')),
                status=str(row.get('status', 'STOCK'))
            ) # 여기서 괄호가 정확히 닫혀야 합니다.
            db.add(new_tractor)
        
        db.commit()
        return {"message": "업로드 성공"}
    except Exception as e:
        db.rollback()
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 3. 삭제 기능
@router.delete("/{tractor_id}")
def delete_tractor(tractor_id: int, db: Session = Depends(get_db)):
    target = db.query(Tractor).filter(Tractor.id == tractor_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="대상을 찾을 수 없음")
    db.delete(target)
    db.commit()
    return {"message": "삭제 성공"}

# 기존 코드 맨 아래에 추가
@router.put("/{tractor_id}")
def update_tractor(tractor_id: int, update_data: dict, db: Session = Depends(get_db)):
    # 1. 대상 찾기
    tractor = db.query(Tractor).filter(Tractor.id == tractor_id).first()
    if not tractor:
        raise HTTPException(status_code=404, detail="수정할 대상을 찾을 수 없음")

    # 2. 데이터 업데이트 (제조사 포함)
    for key, value in update_data.items():
        if hasattr(tractor, key):
            setattr(tractor, key, value)
    
    # 3. 가격 자동 재계산 (공급가나 관세가 바뀌었을 때를 대비)
    tractor.price = float(tractor.base_price) * (1 + float(tractor.tax_rate) / 100)

    db.commit()
    db.refresh(tractor)
    return tractor

# 1.5 신규 직접 등록 기능 추가
@router.post("/")
def create_tractor(data: dict, db: Session = Depends(get_db)):
    try:
        # 가격 자동 계산
        base_price = float(data.get('base_price', 0))
        tax_rate = float(data.get('tax_rate', 0))
        calculated_price = base_price * (1 + tax_rate / 100)

        new_tractor = Tractor(
            serial_number=data.get('serial_number'),
            model=data.get('model'),
            manufacturer_id=int(data.get('manufacturer_id')),
            horsepower=int(data.get('horsepower', 0)),
            base_price=base_price,
            tax_rate=tax_rate,
            price=calculated_price,
            location=data.get('location', 'KOREA'),
            status=data.get('status', 'STOCK')
        )
        db.add(new_tractor)
        db.commit()
        db.refresh(new_tractor)
        return new_tractor
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"등록 실패: {str(e)}")