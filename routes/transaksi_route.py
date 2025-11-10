import base64
from io import BytesIO
from typing import Union

import qrcode
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database.database import get_db
from models.mahasiswa import Mahasiswa
from models.produk import Produk
from models.transaksi import Transaksi
from schemas.transaksi import QRISResponse, TransaksiCreate, TransaksiResponse

router = APIRouter(prefix="/transaksi", tags=["Transaksi"])


# 🟢 1. Buat Transaksi Baru
@router.post("/", response_model=Union[TransaksiResponse, QRISResponse])
def create_transaksi(
    request: Request, transaksi: TransaksiCreate, db: Session = Depends(get_db)
):
    user_email = request.state.user_email
    user = db.query(Mahasiswa).filter(Mahasiswa.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    produk = db.query(Produk).filter(Produk.id == transaksi.produk_id).first()
    if not produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    if produk.penjual_id == user.id:
        raise HTTPException(status_code=400, detail="Tidak bisa membeli produk sendiri")

    total_harga = produk.harga * transaksi.jumlah

    # 🧠 Cek metode pembayaran otomatis
    if user.saldo >= total_harga:
        # Langsung potong saldo
        user.saldo -= total_harga
        metode = "Saldo"
        status = "berhasil"
    else:
        metode = "QRIS"
        status = "pending"

    new_transaksi = Transaksi(
        pembeli_id=user.id,
        produk_id=produk.id,
        jumlah=transaksi.jumlah,
        total_harga=total_harga,
        status=status,
        metode_pembayaran=metode,
    )

    db.add(new_transaksi)
    db.commit()
    db.refresh(new_transaksi)

    # 🧾 Generate QRIS jika saldo tidak cukup
    if metode == "QRIS":
        qris_data = f"QRIS-PAY-{new_transaksi.id}-{total_harga}"
        qr = qrcode.make(qris_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        return {
            "message": "Silakan scan QRIS untuk menyelesaikan pembayaran",
            "transaksi_id": new_transaksi.id,
            "total_harga": total_harga,
            "qris_data": qris_data,
            "qris_image_base64": qr_base64,
        }

    return new_transaksi


# 🟢 2. Konfirmasi Pembayaran QRIS
@router.post("/qris/confirm/{transaksi_id}", response_model=TransaksiResponse)
def confirm_qris(transaksi_id: int, db: Session = Depends(get_db)):
    transaksi = db.query(Transaksi).filter(Transaksi.id == transaksi_id).first()
    if not transaksi:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")

    if transaksi.status == "berhasil":
        raise HTTPException(status_code=400, detail="Transaksi sudah dikonfirmasi")

    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id == transaksi.pembeli_id).first()
    if not mahasiswa:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")

    # Anggap QRIS sudah dibayar → update status
    transaksi.status = "berhasil"

    db.commit()
    db.refresh(transaksi)

    return transaksi


# 🟢 3. Lihat Riwayat Transaksi Mahasiswa
@router.get("/{mahasiswa_id}", response_model=list[TransaksiResponse])
def get_transaksi_by_mahasiswa(mahasiswa_id: int, db: Session = Depends(get_db)):
    transaksi = db.query(Transaksi).filter(Transaksi.pembeli_id == mahasiswa_id).all()
    return transaksi
