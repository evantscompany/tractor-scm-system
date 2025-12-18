from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config import Base

class MaintenanceHistory(Base):
    __tablename__ = "maintenance_histories"

    id= Column(Integer, primary_key=True, index=True)
    tractor_id = Column(Integer,ForeignKey("tractors.id"))

    category = Column(String, nullable=False)
    description = Column(String)
    cost= Column(Float,default=0.0)         #발생비용
    hours_at_event = Column(Float)          #당시 가동 시간
    event_date = Column(DateTime(timezone=True), server_default=func.now())

    tractor = relationship("Tractor", back_populates="histories")
