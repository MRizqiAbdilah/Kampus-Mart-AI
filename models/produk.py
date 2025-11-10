from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Produk(Base):
    __tablename__ = "produk"

    id = Column(Integer, primary_key=True, index=True)
    nama_produk = Column(String, nullable=False)
    deskripsi = Column(String)
    harga = Column(Float, nullable=False)
    penjual_id = Column(Integer, ForeignKey("mahasiswa.id"), nullable=False)

    penjual = relationship("Mahasiswa", backref="produk_dijual")
