from sqlalchemy.orm import Session
from app.models.history import MaintenanceHistory
from app.models.tractor import Tractor
from app.schemas.history import MaintenanceHistoryCreate

def create_history(db:Session, history : MaintenanceHistoryCreate):
    #1. 이력생성
    db_history= MaintenanceHistory(**history.model_dump())
    db.add(db_history)

    #2. 트랙터의 현재 가동시간 (current_hours) 업데이트
    #이력에 적힌 시간이 기존 시간보다 크다면 최신으로 갱신

    db_tractor = db.query(Tractor).filter(Tractor.id==history.tractor_id).first()
    if db_tractor and history.hours_at_event > db_tractor.current_hours:
        db_tractor.current_hours = history.hours_at_event

    db.commit()
    db.refresh(db_history)
    return db_history

def get_history_by_tractor(db: Session, tractor_id: int):
    return db.query(MaintenanceHistory).filter(MaintenanceHistory.tractor_id ==tractor_id).all()


