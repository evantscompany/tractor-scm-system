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

def update_tractor(db: Session, tractor_id: int, tractor_data: TractorCreate):
    db_tractor = db.query(Tractor).filter(Tractor.id == tractor_id).first()
    if db_tractor:
        # 값이 명시적으로 전달된 필드만 업데이트 (부분 업데이트 대응)
        update_data = tractor_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tractor, key, value)
        db.commit()
        db.refresh(db_tractor)
    return db_tractor

def delete_tractor(db: Session, tractor_id: int):
    db_tractor = db.query(Tractor).filter(Tractor.id == tractor_id).first()
    if db_tractor:
        db.delete(db_tractor)
        db.commit()
        return True
    return False