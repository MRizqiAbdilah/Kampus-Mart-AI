from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.matakuliah import Matakuliah
from schemas.matakuliah import MatakuliahCreate, MatakuliahResponse
from typing import List

router = APIRouter(prefix="/matakuliah", tags=["Matakuliah"])

@router.post("/", response_model=MatakuliahCreate)
def create_matakuliah(mk: MatakuliahCreate, db: Session = Depends(get_db)):
    new_mk = Matakuliah(**mk.dict())
    db.add(new_mk)
    db.commit()
    db.refresh(new_mk)
    return new_mk


@router.get("/", response_model=List[MatakuliahResponse])
def get_all_matakuliah(db: Session = Depends(get_db)):
    mk_list = db.query(Matakuliah).all()
    return [
        MatakuliahResponse(
            id=mk.id,
            nama=mk.nama,
            sks=mk.sks,
            jumlah_mahasiswa=len(mk.mahasiswa),
            mahasiswa=[m.nama for m in mk.mahasiswa]
        )
        for mk in mk_list
    ]


@router.get("/{mk_id}", response_model=MatakuliahResponse)
def get_matakuliah(mk_id: int, db: Session = Depends(get_db)):
    mk = db.query(Matakuliah).filter(Matakuliah.id == mk_id).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah not found")


    return MatakuliahResponse(
        id=mk.id,
        nama=mk.nama,
        sks=mk.sks,
        jumlah_mahasiswa=len(mk.mahasiswa),
        mahasiswa=[m.nama for m in mk.mahasiswa]
    )


@router.delete("/{mk_id}")
def delete_matakuliah(mk_id: int, db: Session = Depends(get_db)):
    mk = db.query(Matakuliah).filter(Matakuliah.id == mk_id).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah not found")
    db.delete(mk)
    db.commit()
    return {"message": "Matakuliah deleted successfully"}
