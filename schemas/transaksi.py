from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


# --- model dasar yang sudah kamu punya ---
class TransaksiBase(BaseModel):
    produk_id: int
    jumlah: int


class TransaksiCreate(TransaksiBase):
    pass


class TransaksiResponse(TransaksiBase):
    id: int
    pembeli_id: int
    total_harga: float
    tanggal_transaksi: datetime

    class Config:
        from_attributes = True


# --- tambahan baru untuk QRIS response ---
class QRISResponse(BaseModel):
    message: str
    transaksi_id: int
    total_harga: float
    qris_data: str
    qris_image_base64: str
