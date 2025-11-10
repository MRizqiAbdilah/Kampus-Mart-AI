from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from models.mahasiswa import Mahasiswa
from schemas.auth import LoginMahasiswa, RegisterMahasiswa, Token
from utils.auth_utils import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
def register_user(data: RegisterMahasiswa, db: Session = Depends(get_db)):
    existing_user = db.query(Mahasiswa).filter(Mahasiswa.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(data.password)
    new_user = Mahasiswa(
        nama=data.nama,
        nim=data.nim,
        email=data.email,
        password_hash=hashed_pw,
        jurusan=data.jurusan,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login_user(data: LoginMahasiswa, db: Session = Depends(get_db)):
    user = db.query(Mahasiswa).filter(Mahasiswa.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
