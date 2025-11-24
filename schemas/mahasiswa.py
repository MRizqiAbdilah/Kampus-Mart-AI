from typing import List, Optional
from datetime import date
from pydantic import BaseModel, EmailStr
from .kelas import KelasResponse
from .matakuliah import MatakuliahResponse, MatakuliahBase


class MahasiswaBase(BaseModel):
    id: int
    nama: str
    username: str
    email: EmailStr
    nim: str
    semester: int | None = None

    # 🔥 FIELD BARU
    tahun_masuk: Optional[int] = None
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None

    kelas: Optional[str] = None
    matakuliah: Optional[List[MatakuliahBase]] = []

    total_sks: Optional[int]

    class Config:
        from_attributes = True


class MahasiswaCreate(MahasiswaBase):
    # Bisa langsung diwariskan, tapi tetap boleh eksplisit
    username: str
    email: EmailStr
    nama: str
    nim: str
    semester: Optional[int] = 1

    # 🔥 FIELD BARU (ikut diwariskan otomatis)
    tahun_masuk: Optional[int] = 2025
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None


class MahasiswaResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    nama: str
    nim: str
    semester: int | None = None
    saldo: float

    # 🔥 FIELD BARU
    tahun_masuk: Optional[int] = None
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None

    kelas: Optional[KelasResponse] = None
    matakuliah: Optional[List[MatakuliahResponse]] = []

    total_sks: Optional[int]

    class Config:
        from_attributes = True

class MahasiswaUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nama: Optional[str] = None
    nim: Optional[str] = None
    semester: Optional[int] = None

    tahun_masuk: Optional[int] = None
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None

    kelas_id: Optional[int] = None


