from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models.mahasiswa import Mahasiswa

router = APIRouter(prefix="/me", tags=["User"])

@router.get("/")
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_email = getattr(request.state, "user_email", None)
    if not user_email:
        return {"error": "User tidak ditemukan"}

    user = db.query(Mahasiswa).filter(Mahasiswa.email == user_email).first()
    if not user:
        return {"error": "User tidak ditemukan di database"}

    return {
        "id": user.id,
        "nama": user.nama,
        "nim": user.nim,
        "email": user.email,
    }
