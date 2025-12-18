from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config import get_db
from app.schemas.history import MaintenanceHistory,MaintenanceHistoryCreate
from app.crud import history as history_crud

router = APIRouter(prefix='/history', tags=["Maintenance History"])

@router.post("/",response_model=MaintenanceHistory)
def create_maintenance_log(history: MaintenanceHistoryCreate, db:Session = Depends(get_db)):
    return history_crud.create_history(db=db,history=history)

@router.get("/tractor/{tractor_id}", response_model=List[MaintenanceHistory])
def read_history_by_tractor(tractor_id: int, db: Session = Depends(get_db)):
    return history_crud.get_history_by_tractor(db, tractor_id=tractor_id)

# ... 기존 코드 아래에 추가 ...

@router.delete("/{history_id}")
def delete_maintenance_log(history_id: int, db: Session = Depends(get_db)):
    # 1. 모델에서 직접 해당 ID를 찾습니다.
    # (주의: history_crud 파일 상단에 MaintenanceHistory 모델이 import 되어 있어야 합니다)
    from app.models.history import MaintenanceHistory as MaintenanceHistoryModel
    
    db_history = db.query(MaintenanceHistoryModel).filter(MaintenanceHistoryModel.id == history_id).first()
    
    if not db_history:
        raise HTTPException(status_code=404, detail="삭제할 이력을 찾을 수 없습니다.")
    
    # 2. 삭제 실행
    db.delete(db_history)
    db.commit()
    
    return {"message": "이력이 삭제되었습니다.", "id": history_id}