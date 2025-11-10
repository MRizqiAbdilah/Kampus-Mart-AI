from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from database.base import Base


class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    pembeli_id = Column(Integer, ForeignKey("mahasiswa.id"), nullable=False)
    produk_id = Column(Integer, ForeignKey("produk.id"), nullable=False)
    jumlah = Column(Integer, nullable=False)
    total_harga = Column(Float, nullable=False)
    tanggal_transaksi = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending")  # pending | berhasil | gagal
    metode_pembayaran = Column(String, default="Saldo")  # Saldo | QRIS

    pembeli = relationship("Mahasiswa", foreign_keys=[pembeli_id])
    produk = relationship("Produk", backref="transaksi_produk")
