from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from models.transaksi import Transaksi

router = APIRouter(prefix="/qris", tags=["Qris"])


@router.post("/confirm/{transaksi_id}")
def confirm_qris(transaksi_id: int, db: Session = Depends(get_db)):
    transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if not transaksi:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")

    if transaksi.stat == "berhasil":
        return {"message": "Transaksi sudah dibayar sebelumnya"}

    transaksi.status = "berhasil"
    db.commit()
    db.refresh(transaksi)
    return {"message": f"Pembayaran QRIS untuk transaksi {transaksi_id} berhasil!"}
