from pydantic import BaseModel
from typing import List, Optional

class MatakuliahBase(BaseModel):
    id: int
    nama: str
    sks: Optional[int] = None

class MatakuliahCreate(BaseModel):
    nama: str
    sks: Optional[int] = 2


class MatakuliahResponse(BaseModel):
    id: int
    nama: str
    sks: int
    jumlah_mahasiswa: int
    mahasiswa: List[dict]

    class Config:
        from_attributes = True

class MatakuliahUpdate(BaseModel):
    nama: str
    sks: int = 2