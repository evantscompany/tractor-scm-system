from sqlalchemy.orm import Session
from app.models.farmer import Farmer
from app.schemas.farmer import FarmerCreate

#농민 등록

def create_farmer(db : Session, farmer : FarmerCreate):
    db_farmer=Farmer(
        name=farmer.name,
        phone = farmer.phone,
        address=farmer.address,
        land_area = farmer.land_area,
        main_crop=farmer.main_crop
    )
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer

#농민 목록 조회

def get_farmers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Farmer).offset(skip).limit(limit).all()

# 특정 농민 상세 조회
def get_farmer(db: Session, farmer_id: int):
    return db.query(Farmer).filter(Farmer.id == farmer_id).first()
