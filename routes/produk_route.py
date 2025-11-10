from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database.database import get_db
from models.produk import Produk
from schemas.produk import ProdukCreate, ProdukResponse
from typing import List

router = APIRouter(prefix="/produk", tags=["Produk"])

@router.post("/", response_model=ProdukResponse)
def create_produk(request: Request, produk: ProdukCreate, db: Session = Depends(get_db)):
    penjual_id = getattr(request.state, "user_id", None)
    if not penjual_id:
        raise HTTPException(status_code=401, detail="User belum login")

    new_produk = Produk(
        **produk.dict(),
        penjual_id=penjual_id
    )

    db.add(new_produk)
    db.commit()
    db.refresh(new_produk)
    return new_produk


@router.get("/", response_model=List[ProdukResponse])
def get_all_produk(db: Session = Depends(get_db)):
    return db.query(Produk).all()
