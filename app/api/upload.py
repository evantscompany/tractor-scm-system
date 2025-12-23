from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
import io
from datetime import datetime

from app.config import get_db
from app.models.farmer import Farmer
from app.models.tractor import Tractor
from app.models.manufacturer import Manufacturer
from app.models.history import MaintenanceHistory

router = APIRouter(prefix="/upload", tags=["통합 업로드"])

@router.post("/integrated-excel")
async def upload_integrated_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="엑셀 파일만 가능합니다.")

    try:
        contents = await file.read()
        excel = pd.read_excel(io.BytesIO(contents), sheet_name=None)
        
        df_f = excel.get('Farmers')
        df_t = excel.get('Tractors')
        df_h = excel.get('Maintenance')

        if df_f is None or df_t is None:
            raise HTTPException(status_code=400, detail="'Farmers'와 'Tractors' 시트가 필수입니다.")

        # 트랜잭션 시작
        with db.begin():
            # 1. 트랙터 처리 및 맵 생성
            tractor_map = {}
            for _, row in df_t.iterrows():
                sn = str(row.get('serial_number')).strip()
                # 제조사 자동 생성 로직
                m_name = str(row.get('manufacturer_name', '기타')).strip()
                m_obj = db.query(Manufacturer).filter(Manufacturer.name == m_name).first()
                if not m_obj:
                    m_obj = Manufacturer(name=m_name)
                    db.add(m_obj); db.flush()

                new_t = Tractor(
                    serial_number=sn,
                    model=str(row.get('model', 'Unknown')),
                    manufacturer_id=m_obj.id,
                    base_price=float(row.get('base_price', 0)),
                    tax_rate=float(row.get('tax_rate', 0)),
                    price=float(row.get('base_price', 0)) * (1 + float(row.get('tax_rate', 0))/100),
                    current_hours=0.0
                )
                db.add(new_t); db.flush()
                tractor_map[sn] = new_t

            # 2. 농민 등록 (트랙터 필수 체크)
            for _, row in df_f.iterrows():
                f_sn = str(row.get('serial_number')).strip()
                if f_sn not in tractor_map:
                    # 트랙터 없는 농민 발견 시 전체 롤백
                    raise Exception(f"농민 '{row.get('name')}'의 트랙터(S/N:{f_sn})가 목록에 없습니다.")

                new_f = Farmer(
                    name=str(row.get('name')),
                    phone=str(row.get('phone')),
                    land_area=float(row.get('land_area', 0))
                )
                db.add(new_f); db.flush()
                tractor_map[f_sn].farmer_id = new_f.id

            # 3. 정비 이력 및 시간 동기화
            if df_h is not None:
                for _, row in df_h.iterrows():
                    h_sn = str(row.get('tractor_sn')).strip()
                    if h_sn in tractor_map:
                        t_obj = tractor_map[h_sn]
                        h_hours = float(row.get('hours_at_event', 0))
                        db.add(MaintenanceHistory(
                            tractor_id=t_obj.id,
                            category=str(row.get('category')),
                            hours_at_event=h_hours
                        ))
                        # 가동시간 갱신
                        if h_hours > t_obj.current_hours:
                            t_obj.current_hours = h_hours

        return {"status": "success", "message": f"{len(tractor_map)}건 통합 등록 완료"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))