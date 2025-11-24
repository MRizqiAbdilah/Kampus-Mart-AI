from pydantic import BaseModel
from typing import List

class KelasBase(BaseModel):
    nama: str

class KelasCreate(KelasBase):
    nama: str

class KelasResponse(BaseModel):
    id: int
    nama: str
    jumlah_mahasiswa: int
    mahasiswa: List[str]

