from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy.orm import Session

import pandas as pd

import io

from datetime import datetime



from app.config import get_db

from app.schemas.tractor import Tractor as TractorSchema, TractorCreate

from app.crud import tractor as tractor_crud

from app.models.manufacturer import Manufacturer

from app.models.tractor import Tractor



router = APIRouter(

    prefix="/tractors",

    tags=["트랙터 관리"]

)



# --- [기존 기능] 기본 CRUD ---



@router.post("/", response_model=TractorSchema, summary="트랙터 개별 등록")

def create_tractor(tractor: TractorCreate, db: Session = Depends(get_db)):

    return tractor_crud.create_tractor(db, tractor)



@router.get("/", response_model=list[TractorSchema], summary="트랙터 목록 조회")

def read_tractors(db: Session = Depends(get_db)):

    return tractor_crud.get_tractors(db)



@router.put("/{tractor_id}", response_model=TractorSchema, summary="트랙터 수정")

def edit_tractor(tractor_id: int, tractor: TractorCreate, db: Session = Depends(get_db)):

    updated = tractor_crud.update_tractor(db, tractor_id, tractor)

    if not updated:

        raise HTTPException(status_code=404, detail="Tractor not found")

    return updated



@router.delete("/{tractor_id}", summary="트랙터 삭제")

def remove_tractor(tractor_id: int, db: Session = Depends(get_db)):

    deleted = tractor_crud.delete_tractor(db, tractor_id)

    if not deleted:

        raise HTTPException(status_code=404, detail="Tractor not found")

    return {"ok": True, "message": "Tractor deleted"}





# --- [새 기능] 엑셀 대량 업로드 (디버깅 로그 포함) ---



@router.post("/upload-excel")

async def upload_tractor_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):

    print(f"\n[시작] 파일명: {file.filename}")

    contents = await file.read()

    df = pd.read_excel(io.BytesIO(contents))

   

    # 컬럼명의 앞뒤 공백 제거 (실수 방지)

    df.columns = [c.strip() for c in df.columns]

    print(f"[체크] 엑셀 컬럼들: {df.columns.tolist()}")



    success_count = 0

    for index, row in df.iterrows():

        try:

            # 1. 제조사 처리 (manufacturer_name 컬럼 확인)

            m_name = str(row.get('manufacturer_name', '기타')).strip()

            manufacturer = db.query(Manufacturer).filter(Manufacturer.name == m_name).first()

            if not manufacturer:

                manufacturer = Manufacturer(name=m_name, country="Unknown")

                db.add(manufacturer)

                db.flush()



            # 2. 시리얼 번호 확인

            s_num = str(row.get('serial_number', '')).strip()

            if not s_num or s_num == 'nan':

                print(f"[{index}행] 시리얼 번호가 없어 건너뜁니다.")

                continue



            # 3. 중복 체크

            if db.query(Tractor).filter(Tractor.serial_number == s_num).first():

                continue



            # 4. 트랙터 저장

            new_tractor = Tractor(

                serial_number=s_num,

                model=str(row.get('model', 'Unknown')),

                horsepower=int(row.get('horsepower', 0)) if pd.notnull(row.get('horsepower')) else 0,

                manufacturer_id=manufacturer.id,

                release_date=pd.to_datetime(row.get('release_date')) if pd.notnull(row.get('release_date')) else datetime.now(),

                arrival_date=pd.to_datetime(row.get('arrival_date')) if pd.notnull(row.get('arrival_date')) else datetime.now()

            )

            db.add(new_tractor)

            success_count += 1

        except Exception as e:

            print(f"[{index}행 오류]: {e}")



    db.commit()

    print(f"[완료] 총 {success_count}개 저장됨.")

    return {"message": f"{success_count}개 등록 완료"}
