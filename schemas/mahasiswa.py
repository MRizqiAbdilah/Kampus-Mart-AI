from pydantic import BaseModel


class MahasiswaBase(BaseModel):
    nama: str
    nim: str
    jurusan: str


class MahasiswaCreate(MahasiswaBase):
    pass


class MahasiswaResponse(MahasiswaBase):
    id: int
    saldo: float  # ✅ Tambahan field saldo

    class Config:
        orm_mode = True
