from datetime import datetime

from pydantic import BaseModel


class SaldoBase(BaseModel):
    jumlah: float


class SaldoCreate(SaldoBase):
    pass


class SaldoResponse(SaldoBase):
    id: int
    mahasiswa_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
