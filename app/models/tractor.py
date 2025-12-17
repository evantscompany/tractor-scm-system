from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.config import Base
from datetime import datetime

class Tractor(Base):
    __tablename__ = "tractors"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False, default=datetime.now)
    arrival_date = Column(DateTime, nullable=False, default=datetime.now)
    
    tax_rate = Column(Float, default=0.0)
    base_price = Column(Float, default=0.0)
    price = Column(Float, nullable=True)
    horsepower = Column(Integer, nullable=True)
    location = Column(String, default="KOREA")
    status = Column(String, default="STOCK")

    # 외래키는 테이블 이름인 "manufacturers.id"를 바라봅니다.
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
    # 관계 설정은 클래스 이름인 "Manufacturer"를 문자열로 바라봅니다.
    manufacturer = relationship("Manufacturer", back_populates="tractors")