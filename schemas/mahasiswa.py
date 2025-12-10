from pydantic.fields import Field
from schemas.matakuliah import MatakuliahCreate
from schemas.kelas import KelasBase
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, EmailStr
from .kelas import KelasResponse, KelasMahasiswa
from .matakuliah import MatakuliahResponse, MatakuliahBase

# ============================================================
# BASE MODEL (untuk inheritance)
# ============================================================
class MahasiswaBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    nama: str
    nim: int
    semester: Optional[int] = None

    tahun_masuk: Optional[int] = None
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None

    kelas: Optional[KelasMahasiswa] = None
    matakuliah: List[MatakuliahBase] = Field(default_factory=list)

    total_sks: Optional[int] = None

    class Config:
        from_attributes = True


# ============================================================
# CREATE
# ============================================================
class MahasiswaCreate(BaseModel):
    username: str
    email: EmailStr
    nama: str
    nim: int
    semester: Optional[int] = 1

    tahun_masuk: Optional[int] = 2025
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None

    # RELASI
    kelas: Optional[int] = None                # ID kelas
    matakuliah: List[MatakuliahBase] = Field(default_factory=list)

    class Config:
        from_attributes = True


# ============================================================
# RESPONSE MODEL
# ============================================================
class MahasiswaResponse(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    nama: str
    nim: int
    semester: Optional[int] = None
    saldo: Optional[float] = None

    tahun_masuk: Optional[int] = None
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None

    # Kelas (extended details)
    kelas: Optional[KelasResponse] = None

    # Matakuliah (extended details)
    matakuliah: List[MatakuliahResponse] = Field(default_factory=list)

    total_sks: Optional[int] = None

    class Config:
        from_attributes = True


# ============================================================
# UPDATE
# ============================================================
class MahasiswaUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nama: Optional[str] = None
    nim: Optional[int] = None
    semester: Optional[int] = None

    tahun_masuk: Optional[int] = None
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None

    kelas_id: Optional[int] = None

    class Config:
        from_attributes = True