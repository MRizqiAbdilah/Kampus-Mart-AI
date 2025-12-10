from schemas.kelas import KelasUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.kelas import Kelas
from schemas.kelas import KelasCreate, KelasResponse
from typing import List

router = APIRouter(prefix="/kelas", tags=["Kelas"])

@router.post("/", response_model=KelasCreate)
def create_kelas(kelas: KelasCreate, db: Session = Depends(get_db)):
    new_kelas = Kelas(**kelas.dict())
    db.add(new_kelas)
    db.commit()
    db.refresh(new_kelas)
    return new_kelas


@router.get("/", response_model=List[KelasResponse])
def get_all_kelas(db: Session = Depends(get_db)):
    kelas_list = db.query(Kelas).all()

    return [
        KelasResponse(
            id=k.id, # type: ignore[arg-type]
            nama=k.nama,
            jumlah_mahasiswa=len(k.mahasiswa), #type: ignore
            mahasiswa=[m.nama for m in k.mahasiswa]  # <-- tampilkan nama
        )
        for k in kelas_list
    ]


@router.get("/{kelas_id}", response_model=KelasResponse)
def get_kelas(kelas_id: int, db: Session = Depends(get_db)):
    kelas = db.query(Kelas).filter(Kelas.id == kelas_id).first()
    if not kelas:
        raise HTTPException(status_code=404, detail="Kelas not found")

    return KelasResponse(
        id=kelas.id, # type: ignore[arg-type]
        nama=kelas.nama,
        jumlah_mahasiswa=len(kelas.mahasiswa), #type: ignore
        mahasiswa=[m.nama for m in kelas.mahasiswa]
    )

@router.put("/{kelas_id}")
def update_kelas(kelas_id: int, data_update: KelasUpdate, db: Session = Depends(get_db)):
    kelas = db.query(Kelas).filter(Kelas.id == kelas_id).first()
    if not kelas:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    # UPDATE HANYA YANG DIKIRIM
    update_data = data_update.model_dump(exclude_unset=True)

    # Set field yang diupdate
    for key, value in update_data.items():
        setattr(kelas, key, value)

    db.commit()
    db.refresh(kelas)
    if not update_data:
        raise HTTPException(status_code=400, detail="Tidak ada data yang diubah")
        
    # RETURN HANYA FIELD YANG DIUBAH
    return {
        "id": kelas.id,
        "updated": update_data
    }

@router.delete("/{kelas_id}")
def delete_kelas(kelas_id: int, db: Session = Depends(get_db)):
    kelas = db.query(Kelas).filter(Kelas.id == kelas_id).first()
    if not kelas:
        raise HTTPException(status_code=404, detail="Kelas not found")
    db.delete(kelas)
    db.commit()
    return {"message": "Kelas deleted successfully"}
