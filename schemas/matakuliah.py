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

    class Config:
        from_attributes = True
