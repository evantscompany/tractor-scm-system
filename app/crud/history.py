from sqlalchemy.orm import Session
from app.models.history import MaintenanceHistory
from app.models.tractor import Tractor
from app.schemas.history import MaintenanceHistoryCreate

# 1. 이력 생성 함수
def create_history(db: Session, history: MaintenanceHistoryCreate):
    db_history = MaintenanceHistory()
    db_history.tractor_id = history.tractor_id
    db_history.category = history.category
    db_history.description = history.description
    db_history.cost = float(history.cost or 0)
    db_history.hours_at_event = float(history.hours_at_event or 0)

    db.add(db_history)

    # 트랙터 가동시간 업데이트
    db_tractor = db.query(Tractor).filter(Tractor.id == history.tractor_id).first()
    if db_tractor:
        new_hours = float(history.hours_at_event or 0)
        if new_hours > (db_tractor.current_hours or 0):
            db_tractor.current_hours = new_hours

    db.commit()
    db.refresh(db_history)
    return db_history

# 2. 이력 조회 함수 (이 부분이 없어서 에러가 난 것입니다!)
def get_history_by_tractor(db: Session, tractor_id: int):
    return db.query(MaintenanceHistory)\
             .filter(MaintenanceHistory.tractor_id == tractor_id)\
             .order_by(MaintenanceHistory.id.desc())\
             .all()