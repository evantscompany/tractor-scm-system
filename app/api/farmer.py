from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config import get_db
from app.schemas.farmer import Farmer, FarmerCreate
from app.crud import farmer as farmer_crud

router = APIRouter(prefix="/farmers", tags=["Farmers"])

@router.post("/", response_model=Farmer)
def create_new_farmer(farmer: FarmerCreate, db: Session = Depends(get_db)):
    return farmer_crud.create_farmer(db=db, farmer=farmer)

@router.get("/", response_model=List[Farmer])
def read_farmers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return farmer_crud.get_farmers(db, skip=skip, limit=limit)