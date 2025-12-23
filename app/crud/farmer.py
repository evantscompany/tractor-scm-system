from sqlalchemy.orm import Session, joinedload
from app.models.farmer import Farmer
from app.models.tractor import Tractor
from app.models.history import MaintenanceHistory  # 이력 모델도 필요 시 로드하기 위해 추가
from app.schemas.farmer import FarmerCreate

# 1. 농민 등록 (기존 로직 유지)
def create_farmer(db: Session, farmer: FarmerCreate):
    db_farmer = Farmer(
        name=farmer.name,
        phone=farmer.phone,
        address=farmer.address,
        land_area=farmer.land_area,
        main_crop=farmer.main_crop
    )
    db.add(db_farmer)
    db.flush()

    if farmer.serial_number:
        tractor = db.query(Tractor).filter(Tractor.serial_number == farmer.serial_number).first()
        if tractor:
            tractor.farmer_id = db_farmer.id
    
    db.commit()
    db.refresh(db_farmer)
    return db_farmer

# 2. 농민 목록 조회 [중요 수정: joinedload 추가]
def get_farmers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Farmer)\
        .options(
            joinedload(Farmer.tractors)  # 농민 가져올 때 트랙터도 같이 가져와!
            .joinedload(Tractor.histories) # 트랙터 안에 정비 이력도 싹 다 가져와!
        )\
        .offset(skip).limit(limit).all()

# 3. 특정 농민 상세 조회 [중요 수정: joinedload 추가]
def get_farmer(db: Session, farmer_id: int):
    return db.query(Farmer)\
        .options(
            joinedload(Farmer.tractors)
            .joinedload(Tractor.histories)
        )\
        .filter(Farmer.id == farmer_id).first()