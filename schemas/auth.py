from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class RegisterMahasiswa(BaseModel):
    nama: str
    username: str
    nim: str
    email: EmailStr
    password: str

    # 🔥 Tambahan baru (opsional)
    tahun_masuk: Optional[int] = 2025
    alamat: Optional[str] = None
    tanggal_lahir: Optional[date] = None


class LoginMahasiswa(BaseModel):
    identifier: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
