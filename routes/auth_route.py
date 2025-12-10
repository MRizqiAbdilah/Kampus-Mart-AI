from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from models.mahasiswa import Mahasiswa
from schemas.auth import LoginMahasiswa, RegisterMahasiswa, Token
from utils.auth_utils import create_access_token, hash_password, verify_password
from sqlalchemy import or_


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
def register_user(data: RegisterMahasiswa, db: Session = Depends(get_db)):
    existing_email = db.query(Mahasiswa).filter(Mahasiswa.email == data.email).first()
    existing_username = db.query(Mahasiswa).filter(Mahasiswa.username == data.username).first()
    existing_nim = db.query(Mahasiswa).filter(Mahasiswa.nim == data.nim).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    if existing_nim:
        raise HTTPException(status_code=400, detail="Nim already registered")

    hashed_pw = hash_password(data.password)
    new_user = Mahasiswa(
        nama=data.nama,
        username=data.username,
        nim=data.nim,
        email=data.email,
        password_hash=hashed_pw,
        # 🔥 Tambahan baru (opsional)
        tahun_masuk=data.tahun_masuk,
        alamat= data.alamat,
        tanggal_lahir= data.tanggal_lahir
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_user(data: LoginMahasiswa, db: Session = Depends(get_db)):
    user = db.query(Mahasiswa).filter(
        or_(
            Mahasiswa.email == data.identifier,
            Mahasiswa.username == data.identifier  # input bisa email atau username
        )
    ).first()

    if not user or not verify_password(data.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}