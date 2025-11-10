from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.mahasiswa import Mahasiswa
from schemas.mahasiswa import MahasiswaCreate, MahasiswaResponse
from typing import List

router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa"])

@router.post("/", response_model=MahasiswaResponse)
def create_mahasiswa(mahasiswa: MahasiswaCreate, db: Session = Depends(get_db)):
    new_mhs = Mahasiswa(**mahasiswa.dict())
    db.add(new_mhs)
    db.commit()
    db.refresh(new_mhs)
    return new_mhs

@router.get("/", response_model=List[MahasiswaResponse])
def get_all_mahasiswa(db: Session = Depends(get_db)):
    return db.query(Mahasiswa).all()

@router.get("/{mahasiswa_id}", response_model=MahasiswaResponse)
def get_mahasiswa(mahasiswa_id: int, db: Session = Depends(get_db)):
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")
    return mhs

@router.delete("/{mahasiswa_id}")
def delete_mahasiswa(mahasiswa_id: int, db: Session = Depends(get_db)):
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")
    db.delete(mhs)
    db.commit()
    return {"message": "Mahasiswa deleted successfully"}
