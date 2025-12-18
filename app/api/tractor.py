from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session, joinedload
import pandas as pd
import io
from app.config import get_db
from app.models.tractor import Tractor
from app.models.manufacturer import Manufacturer
from app.models.farmer import Farmer
from app.models.history import MaintenanceHistory

router = APIRouter(prefix="/tractors", tags=["tractors"])

# 1. 조회 기능 (제조사 포함)
@router.get("/")
def get_tractors(db: Session = Depends(get_db)):
    return db.query(Tractor).options(
        joinedload(Tractor.manufacturer), #제조사
        joinedload(Tractor.owner) #소유주
        ).all()

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

    # --- [정비 이력 자동 생성 로직] ---
    # 프론트엔드에서 'maintenance_description' 이라는 키로 내용을 보낸다고 가정합니다.
    m_desc = update_data.get('maintenance_description')
    
    if m_desc:
        new_history = MaintenanceHistory(
            tractor_id=tractor.id,
            category=update_data.get('category', '일반정비'), # 카테고리 기본값
            description=m_desc,
            cost=float(update_data.get('cost', 0)),
            hours_at_event=float(update_data.get('hours_at_event', 0))
        )
        db.add(new_history)
    # ------------------------------



    # 2. 데이터 업데이트 (제조사 포함)
    for key, value in update_data.items():
        if hasattr(tractor, key) and key not in ['maintenance_description', 'category', 'cost', 'hours_at_event']:
            setattr(tractor, key, value)
    
    # 3. 가격 자동 재계산 (공급가나 관세가 바뀌었을 때를 대비)
    tractor.price = float(tractor.base_price) * (1 + float(tractor.tax_rate) / 100)

    db.commit()
    db.refresh(tractor)
    return tractor

# 1.5 신규 직접 등록 기능 추가
# 1.5 신규 직접 등록 기능 (보완 완료)
@router.post("/")
def create_tractor(data: dict, db: Session = Depends(get_db)):
    try:
        # 1. 데이터 추출 (프론트엔드 키값 확인)
        sn = data.get('serial_number')
        model = data.get('model')
        m_id = data.get('manufacturer_id')

        # 2. 필수값 검증
        if not sn or not model or not m_id:
            return HTTPException(status_code=400, detail="시리얼번호, 모델명, 제조사는 필수입니다.")

        # 3. 숫자 변환 (비어있으면 0으로 처리해서 에러 방지)
        def to_float(val):
            try: return float(val) if val else 0.0
            except: return 0.0

        def to_int(val):
            try: return int(val) if val else 0
            except: return 0

        base_price = to_float(data.get('base_price'))
        tax_rate = to_float(data.get('tax_rate'))
        calculated_price = base_price * (1 + tax_rate / 100)

        # 4. DB 객체 생성
        new_tractor = Tractor(
            serial_number=str(sn),
            model=str(model),
            manufacturer_id=to_int(m_id),
            horsepower=to_int(data.get('horsepower')),
            base_price=base_price,
            tax_rate=tax_rate,
            price=calculated_price,
            location=data.get('location', 'KOREA'),
            status=data.get('status', 'STOCK'),
            # 소유주(농민) 정보가 넘어온다면 추가
            owner_id=data.get('farmer_id') if data.get('farmer_id') else None
        )
        
        db.add(new_tractor)
        db.commit()
        db.refresh(new_tractor)
        return new_tractor

    except Exception as e:
        db.rollback()
        print(f"--- 등록 에러 상세 내용 ---")
        print(f"Error Type: {type(e)}")
        print(f"Message: {str(e)}")
        raise HTTPException(status_code=400, detail=f"등록 실패: {str(e)}")