from sqlalchemy import Column , Integer , String , Float
from sqlalchemy.orm import relationship
from app.config import Base

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True,nullable = False)
    phone = Column(String,nullable = False)
    address = Column(String)
    land_area = Column(Float)
    main_crop = Column(String)

    tractors = relationship("Tractor",back_populates="owner")