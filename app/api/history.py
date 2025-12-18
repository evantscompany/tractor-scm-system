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