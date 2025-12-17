from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal, get_db
from app.schemas.manufacturer import Manufacturer, ManufacturerCreate
from app.crud.manufacturer import (
    create_manufacturer,
    get_manufacturers,
    update_manufacturer,
    delete_manufacturer,
    get_manufacturers_with_counts,
)


router = APIRouter(
    prefix="/manufacturers",
    tags=["제조사 관리"]  # Swagger 메뉴 그룹 이름
)
# 제조사 등록
@router.post("/", response_model=Manufacturer,
             summary="제조사 등록",
             description="새로운 제조사를 DB에 등록합니다")
def add_manufacturer(manufacturer: ManufacturerCreate, db: Session = Depends(get_db)):
    return create_manufacturer(db, manufacturer)

# 제조사 목록 조회
@router.get("/", response_model=list[Manufacturer],

            summary="제조사 목록 조회",

            description="등록된 모든 제조사를 조회합니다")

def list_manufacturers(db: Session = Depends(get_db)):

    return get_manufacturers(db)



# 제조사 수정

@router.put("/{manufacturer_id}", response_model=Manufacturer,

            summary="제조사 수정",

            description="특정 제조사의 정보를 수정합니다")

def edit_manufacturer(manufacturer_id: int, manufacturer: ManufacturerCreate, db: Session = Depends(get_db)):

    updated = update_manufacturer(db, manufacturer_id, manufacturer)

    if not updated:

        raise HTTPException(status_code=404, detail="Manufacturer not found")

    return updated



# 제조사 삭제

@router.delete("/{manufacturer_id}",

               summary="제조사 삭제",

               description="특정 제조사를 DB에서 삭제합니다")

def remove_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):

    deleted = delete_manufacturer(db, manufacturer_id)

    if not deleted:

        raise HTTPException(status_code=404, detail="Manufacturer not found")

    return {"ok": True, "message": "Manufacturer deleted"}



# 제조사별 트랙터 개수 조회

@router.get("/with-tractors",

            summary="제조사별 트랙터 개수 조회",

            description="각 제조사별로 등록된 트랙터 개수를 조회합니다")

def list_manufacturers_with_counts(db: Session = Depends(get_db)):

    return get_manufacturers_with_counts(db)
