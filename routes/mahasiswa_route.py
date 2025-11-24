from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.mahasiswa import Mahasiswa
from models.kelas import Kelas
from models.matakuliah import Matakuliah
from schemas.mahasiswa import MahasiswaCreate, MahasiswaResponse, MahasiswaUpdate, MahasiswaBase
from typing import List

router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa"])

# -------------------------------------------------------------------
# CREATE MAHASISWA
# -------------------------------------------------------------------

@router.post("/", response_model=MahasiswaResponse)
def create_mahasiswa(mahasiswa: MahasiswaCreate, db: Session = Depends(get_db)):

    # CEK USERNAME DUPLIKAT
    if db.query(Mahasiswa).filter(Mahasiswa.username == mahasiswa.username).first():
        raise HTTPException(status_code=400, detail=f"Username '{mahasiswa.username}' sudah digunakan")

    # CEK EMAIL DUPLIKAT
    if db.query(Mahasiswa).filter(Mahasiswa.email == mahasiswa.email).first():
        raise HTTPException(status_code=400, detail=f"Email '{mahasiswa.email}' sudah terdaftar")

    # CEK NIM DUPLIKAT
    if db.query(Mahasiswa).filter(Mahasiswa.nim == mahasiswa.nim).first():
        raise HTTPException(status_code=400, detail=f"NIM '{mahasiswa.nim}' sudah digunakan")

    # cek kelas

    new_mhs = Mahasiswa(**mahasiswa.dict())
    db.add(new_mhs)
    db.commit()
    db.refresh(new_mhs)

    return new_mhs


# -------------------------------------------------------------------
# GET ALL MAHASISWA
# -------------------------------------------------------------------

@router.get("/", response_model=List[MahasiswaBase])
def get_all_mahasiswa(db: Session = Depends(get_db)):
    mahasiswa_list = db.query(Mahasiswa).all()

    result = []
    for mhs in mahasiswa_list:
        result.append({
            "id": mhs.id,
            "nama": mhs.nama,
            "username": mhs.username,
            "email": mhs.email,
            "nim": mhs.nim,
            "semester": mhs.semester,

            # 🔥 FIELD BARU
            "tahun_masuk": mhs.tahun_masuk,
            "alamat": mhs.alamat,
            "tanggal_lahir": mhs.tanggal_lahir,

            "kelas": mhs.kelas.nama if mhs.kelas else None,

            # "kelas": None if not mhs.kelas else {
            #     "id": mhs.kelas.id,
            #     "nama": mhs.kelas.nama,
            #     "jumlah_mahasiswa": len(mhs.kelas.mahasiswa),
            #     "mahasiswa": [x.nama for x in mhs.kelas.mahasiswa]
            # },

            "matakuliah": [
                {
                    "nama": mk.nama,
                    "sks": mk.sks,
                }
                for mk in mhs.matakuliah
            ],
            "total_sks": sum([mk.sks for mk in mhs.matakuliah])
        })

    return result


# -------------------------------------------------------------------
# GET MAHASISWA BY ID
# -------------------------------------------------------------------

@router.get("/{mahasiswa_id}", response_model=MahasiswaResponse)
def get_mahasiswa(mahasiswa_id: int, db: Session = Depends(get_db)):
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    return {
            "id": mhs.id,
            "username": mhs.username,
            "email": mhs.email,
            "nama": mhs.nama,
            "nim": mhs.nim,
            "semester": mhs.semester,
            "saldo": mhs.saldo,

            # 🔥 FIELD BARU
            "tahun_masuk": mhs.tahun_masuk,
            "alamat": mhs.alamat,
            "tanggal_lahir": mhs.tanggal_lahir,

            "kelas": None if not mhs.kelas else {
                "id": mhs.kelas.id,
                "nama": mhs.kelas.nama,
                "jumlah_mahasiswa": len(mhs.kelas.mahasiswa),
                "mahasiswa": [x.username for x in mhs.kelas.mahasiswa]
            },

            "matakuliah": [
                {
                    "id": mk.id,
                    "nama": mk.nama,
                    "sks": mk.sks,
                    "jumlah_mahasiswa": len(mk.mahasiswa),
                    "mahasiswa": [x.username for x in mk.mahasiswa]
                }
                for mk in mhs.matakuliah
            ],
            "total_sks": sum([mk.sks for mk in mhs.matakuliah])
        }


# -------------------------------------------------------------------
# DELETE MAHASISWA
# -------------------------------------------------------------------

@router.delete("/{mahasiswa_id}")
def delete_mahasiswa(mahasiswa_id: int, db: Session = Depends(get_db)):
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    db.delete(mhs)
    db.commit()
    return {"message": "Mahasiswa deleted successfully"}


# -------------------------------------------------------------------
# SET KELAS
# -------------------------------------------------------------------

@router.put("/{mahasiswa_id}/kelas/{kelas_id}")
def set_kelas(mahasiswa_id: int, kelas_id: int, db: Session = Depends(get_db)):
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    kelas = db.query(Kelas).filter(Kelas.id == kelas_id).first()
    if not kelas:
        raise HTTPException(status_code=404, detail="Kelas not found")

    mhs.kelas_id = kelas_id
    db.commit()

    return {"message": "Kelas berhasil ditambahkan ke mahasiswa"}


# -------------------------------------------------------------------
# AMBIL MATAKULIAH
# -------------------------------------------------------------------

@router.post("/{mahasiswa_id}/matakuliah/{mk_id}")
def ambil_matakuliah(mahasiswa_id: int, mk_id: int, db: Session = Depends(get_db)):
    # Cek mahasiswa
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    # Cek matakuliah
    mk = db.query(Matakuliah).filter(Matakuliah.id == mk_id).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah not found")

    # Cek duplikat
    if mk in mhs.matakuliah:
        raise HTTPException(status_code=400, detail="Matakuliah sudah diambil")

    # Tambahkan
    mhs.matakuliah.append(mk)
    db.commit()
    db.refresh(mhs)

    return {
        "message": "Matakuliah berhasil ditambahkan",
        "mahasiswa_id": mahasiswa_id,
        "matakuliah_diambil": [
            {"id": m.id, "nama": m.nama, "sks": m.sks}
            for m in mhs.matakuliah
        ]
    }

@router.delete("/{mahasiswa_id}/matakuliah/{mk_id}")
def hapus_matakuliah(mahasiswa_id: int, mk_id: int, db: Session = Depends(get_db)):
    # Cek mahasiswa
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    # Cek matakuliah
    mk = db.query(Matakuliah).filter(Matakuliah.id == mk_id).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah not found")

    # Cek apakah matkul ini memang diambil
    if mk not in mhs.matakuliah:
        raise HTTPException(status_code=400, detail="Matakuliah tidak terdaftar pada mahasiswa")

    # Hapus
    mhs.matakuliah.remove(mk)
    db.commit()
    db.refresh(mhs)

    return {
        "message": "Matakuliah berhasil dihapus",
        "mahasiswa_id": mahasiswa_id,
        "matakuliah_diambil": [
            {"id": m.id, "nama": m.nama, "sks": m.sks}
            for m in mhs.matakuliah
        ]
    }



# -------------------------------------------------------------------
# GET SEMUA MATAKULIAH MAHASISWA
# -------------------------------------------------------------------

@router.put("/{mahasiswa_id}")
def update_mahasiswa(mahasiswa_id: int, data_update: MahasiswaUpdate, db: Session = Depends(get_db)):
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")

    # CEK DUPLIKAT
    if data_update.username and data_update.username != mhs.username:
        if db.query(Mahasiswa).filter(Mahasiswa.username == data_update.username).first():
            raise HTTPException(status_code=400, detail="Username sudah digunakan")

    if data_update.email and data_update.email != mhs.email:
        if db.query(Mahasiswa).filter(Mahasiswa.email == data_update.email).first():
            raise HTTPException(status_code=400, detail="Email sudah digunakan")

    if data_update.nim and data_update.nim != mhs.nim:
        if db.query(Mahasiswa).filter(Mahasiswa.nim == data_update.nim).first():
            raise HTTPException(status_code=400, detail="NIM sudah digunakan")

    # UPDATE HANYA YANG DIKIRIM
    update_data = data_update.dict(exclude_unset=True)

    # Tangani kelas_id
    if "kelas_id" in update_data:
        mhs.kelas_id = update_data["kelas_id"]
        del update_data["kelas_id"]

    # Set field yang diupdate
    for key, value in update_data.items():
        setattr(mhs, key, value)

    db.commit()
    db.refresh(mhs)
    if not update_data:
        raise HTTPException(status_code=400, detail="Tidak ada data yang diubah")
    # RETURN HANYA FIELD YANG DIUBAH
    return {
        "id": mhs.id,
        "updated": update_data
    }
