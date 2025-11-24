import base64
import io

import qrcode
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.database import get_db
from models.mahasiswa import Mahasiswa
from models.saldo import Saldo
from schemas.saldo import SaldoCreate, SaldoResponse

router = APIRouter(prefix="/saldo", tags=["Saldo"])


# 🟢 1. Top Up Saldo (manual)
@router.post("/topup", response_model=SaldoResponse)
def topup_saldo(mahasiswa_id: int, data: SaldoCreate, db: Session = Depends(get_db)):
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mahasiswa:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")

    saldo = Saldo(mahasiswa_id=mahasiswa.id, jumlah=data.jumlah, status="pending")
    db.add(saldo)
    db.commit()
    db.refresh(saldo)
    return saldo


# 🟢 1B. Top Up Saldo via QRIS (simulasi)
@router.post("/topup/qris")
def topup_saldo_qris(
    mahasiswa_id: int, data: SaldoCreate, db: Session = Depends(get_db)
):
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mahasiswa:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")

    # buat transaksi saldo baru dengan status pending
    saldo = Saldo(mahasiswa_id=mahasiswa.id, jumlah=data.jumlah, status="pending")
    db.add(saldo)
    db.commit()
    db.refresh(saldo)

    # simulasi kode QRIS unik (biasanya dikirim ke frontend)
    qris_data = (
        f"QRIS|MID123456|MAHASISWA-{mahasiswa.id}|TXN-{saldo.id}|AMOUNT-{data.jumlah}"
    )
    qr = qrcode.make(qris_data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "message": "QRIS generated successfully",
        "saldo_id": saldo.id,
        "mahasiswa_id": mahasiswa.id,
        "username": mahasiswa.username,
        "jumlah": data.jumlah,
        "status_pembayaran": saldo.status,
        "qris_data": qris_data,
        "qr_image_base64": f"data:image/png;base64,{qr_base64}",
    }


# 🟢 2. Simulasi Callback Konfirmasi QRIS
@router.post("/qris/confirm/{saldo_id}")
def confirm_qris_payment(saldo_id: int, db: Session = Depends(get_db)):
    saldo = db.query(Saldo).filter(Saldo.id == saldo_id).first()
    if not saldo:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")

    if saldo.status == "confirmed":
        raise HTTPException(status_code=400, detail="Transaksi sudah dikonfirmasi")

    saldo.status = "confirmed"
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == saldo.mahasiswa_id).first()
    if not mahasiswa:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")

    # tambahkan saldo mahasiswa
    mahasiswa.saldo += saldo.jumlah
    db.commit()

    return {
        "message": "Pembayaran QRIS berhasil dikonfirmasi",
        "saldo_id": saldo.id,
        "status": saldo.status,
        "total_saldo": mahasiswa.saldo,
    }


# 🟢 3. Lihat Semua Transaksi Mahasiswa
@router.get("/{mahasiswa_id}", response_model=list[SaldoResponse])
def get_saldo_history(mahasiswa_id: int, db: Session = Depends(get_db)):
    transaksi = db.query(Saldo).filter(Saldo.mahasiswa_id == mahasiswa_id).all()
    return transaksi


# 🟢 4. Total Saldo Mahasiswa
@router.get("/mahasiswa/{mahasiswa_id}/total")
def get_total_saldo(mahasiswa_id: int, db: Session = Depends(get_db)):
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mahasiswa:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")

    return {"mahasiswa_id": mahasiswa.id, "saldo": mahasiswa.saldo}
