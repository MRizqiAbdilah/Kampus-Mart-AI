from pydantic import BaseModel, EmailStr

class RegisterMahasiswa(BaseModel):
    nama: str
    nim: str
    email: EmailStr
    password: str
    jurusan: str | None = None

class LoginMahasiswa(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
