from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.matakuliah import Matakuliah
from schemas.matakuliah import MatakuliahCreate, MatakuliahResponse, MatakuliahUpdate
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
    for mhs in mk_list:
        for m in mhs.mahasiswa:
            print(m.nama)
            
    return [
        MatakuliahResponse(
            id=mk.id, # type: ignore[arg-type]
            nama=mk.nama,
            sks=mk.sks, # type: ignore[arg-type]
            jumlah_mahasiswa=len(mk.mahasiswa), # type: ignore[arg-type]
            mahasiswa=[{
                "nama": m.nama,
                "semester": m.semester
            } for m in mk.mahasiswa]
        )
        for mk in mk_list
    ]


@router.get("/{mk_id}", response_model=MatakuliahResponse)
def get_matakuliah(mk_id: int, db: Session = Depends(get_db)):
    mk = db.query(Matakuliah).filter(Matakuliah.id == mk_id).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah not found")


    return MatakuliahResponse(
        id=mk.id, # type: ignore[arg-type]
        nama=mk.nama,
        sks=mk.sks, # type: ignore[arg-type]
        jumlah_mahasiswa=len(mk.mahasiswa), # type: ignore[arg-type]
        mahasiswa=[{
                "nama": m.nama,
                "semester": m.semester
            } for m in mk.mahasiswa]
    )

@router.put("/{mk_id}")
def update_matakuliah(mk_id: int, data_update: MatakuliahUpdate, db: Session = Depends(get_db)):
    matakuliah = db.query(Matakuliah).filter(Matakuliah.id == mk_id).first()
    if not matakuliah:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    # UPDATE HANYA YANG DIKIRIM
    update_data = data_update.model_dump(exclude_unset=True)

    # Set field yang diupdate
    for key, value in update_data.items():
        setattr(matakuliah, key, value)

    db.commit()
    db.refresh(matakuliah)
    if not update_data:
        raise HTTPException(status_code=400, detail="Tidak ada data yang diubah")
        
    # RETURN HANYA FIELD YANG DIUBAH
    return {
        "id": matakuliah.id,
        "updated": update_data
    }

@router.delete("/{mk_id}")
def delete_matakuliah(mk_id: int, db: Session = Depends(get_db)):
    mk = db.query(Matakuliah).filter(Matakuliah.id == mk_id).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah not found")
    db.delete(mk)
    db.commit()
    return {"message": "Matakuliah deleted successfully"}
