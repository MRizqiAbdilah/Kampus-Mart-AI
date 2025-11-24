from pydantic import BaseModel
from typing import List, Optional

class MatakuliahBase(BaseModel):
    nama: str
    sks: Optional[int] = None

class MatakuliahCreate(MatakuliahBase):
    nama: str
    sks: int = 2

class MatakuliahResponse(MatakuliahBase):
    id:int
    jumlah_mahasiswa: int
    mahasiswa: List[str]  # ← LIST NAMA

    class Config:
        from_attributes = True
