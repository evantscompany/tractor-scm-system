from sqlalchemy.orm import Session
from sqlalchemy import func
# 수정된 부분: tractor_system.app 대신 app.models에서 가져오기
from app.models.manufacturer import Manufacturer
from app.models.tractor import Tractor
from app.schemas.manufacturer import ManufacturerCreate

# 제조사 추가
def create_manufacturer(db: Session, manufacturer: ManufacturerCreate):
    db_manufacturer = Manufacturer(
        name=manufacturer.name,
        country=manufacturer.country,
        contact_info=manufacturer.contact_info
    )
    db.add(db_manufacturer)
    db.commit()
    db.refresh(db_manufacturer)
    return db_manufacturer

# 제조사 목록 조회
def get_manufacturers(db: Session):
    return db.query(Manufacturer).all()

# 제조사 수정
def update_manufacturer(db: Session, manufacturer_id: int, manufacturer: ManufacturerCreate):
    existing = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not existing:
        return None
    existing.name = manufacturer.name
    existing.country = manufacturer.country
    existing.contact_info = manufacturer.contact_info
    db.commit()
    db.refresh(existing)
    return existing

# 제조사 삭제
def delete_manufacturer(db: Session, manufacturer_id: int):
    existing = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not existing:
        return False
    db.delete(existing)
    db.commit()
    return True

# 제조사별 트랙터 숫자를 세는 쿼리
def get_manufacturers_with_counts(db: Session):
    results = db.query(
        Manufacturer.id,
        Manufacturer.name,
        Manufacturer.country,
        func.count(Tractor.id).label("tractor_count")
    ).outerjoin(Tractor, Manufacturer.id == Tractor.manufacturer_id).group_by(Manufacturer.id).all()

    return [
        {
            "id": r.id,
            "name": r.name,
            "country": r.country,
            "tractor_count": r.tractor_count
        }
        for r in results
    ]