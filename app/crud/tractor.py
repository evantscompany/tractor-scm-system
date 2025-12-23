from sqlalchemy.orm import Session, joinedload
from app.models.tractor import Tractor
from app.schemas.tractor import TractorCreate

def create_tractor(db: Session, tractor: TractorCreate):
    db_tractor = Tractor(**tractor.model_dump())
    db.add(db_tractor)
    db.commit()
    db.refresh(db_tractor)
    return db_tractor

def get_tractors(db: Session):
    # 중복된 쿼리문을 제거하고 joinedload를 하나로 묶었습니다.
    return db.query(Tractor).options(
        joinedload(Tractor.histories),     # 정비 이력 (매출 계산의 핵심!)
        joinedload(Tractor.manufacturer),  # 제조사 정보
        joinedload(Tractor.owner)          # 소유주 정보
    ).all()

def update_tractor(db: Session, tractor_id: int, tractor_data: dict):
    db_tractor = db.query(Tractor).filter(Tractor.id == tractor_id).first()
    if not db_tractor:
        return None

    # 업데이트 가능한 필드 목록 (기존 DB 컬럼명에 맞춰 유지)
    allowed_fields = [
        "serial_number", "model", "horsepower", "manufacturer_id", 
        "farmer_id", "current_hours", "base_price", "tax_rate", 
        "price", "location", "status"
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