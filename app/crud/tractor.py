from sqlalchemy.orm import Session
# 경로 수정: tractor_system.app.crud -> app.models (실제 테이블 클래스는 models에 있음)
from app.models.tractor import Tractor
from app.schemas.tractor import TractorCreate

def create_tractor(db: Session, tractor: TractorCreate):
    # model_dump를 통해 모든 필드(base_price, location 등)를 포함하여 저장
    db_tractor = Tractor(**tractor.model_dump())
    db.add(db_tractor)
    db.commit()
    db.refresh(db_tractor)
    return db_tractor

def get_tractors(db: Session):
    return db.query(Tractor).all()

# app/crud/tractor.py (수정 부분)

def update_tractor(db: Session, tractor_id: int, tractor_data: dict):
    db_tractor = db.query(Tractor).filter(Tractor.id == tractor_id).first()
    if not db_tractor:
        return None

    # 업데이트할 수 있는 실제 DB 컬럼 목록만 정의합니다.
    # 'histories', 'manufacturer', 'farmer' 등 관계 필드는 여기서 제외해야 합니다!
    allowed_fields = [
        "name", "model_number", "serial_number", 
        "manufacturer_id", "farmer_id", "current_hours"
    ]

    for key, value in tractor_data.items():
        if key in allowed_fields:
            setattr(db_tractor, key, value)

    try:
        db.commit()
        db.refresh(db_tractor)
        return db_tractor
    except Exception as e:
        db.rollback()
        print(f"Update Error: {e}")
        raise e

def delete_tractor(db: Session, tractor_id: int):
    db_tractor = db.query(Tractor).filter(Tractor.id == tractor_id).first()
    if db_tractor:
        db.delete(db_tractor)
        db.commit()
        return True
    return False