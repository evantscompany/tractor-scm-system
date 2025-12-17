from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config import Base

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    country = Column(String(64))
    contact_info = Column(String(128))

    # 다른 파일의 Tractor를 문자열로 참조
    tractors = relationship("Tractor", back_populates="manufacturer")